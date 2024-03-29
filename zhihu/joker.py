from pathlib import Path
from typing import Dict, List, Optional
import os

import certifi
import urllib3
import json
from bs4 import BeautifulSoup, NavigableString

from .config import ACCESS_TOKEN, AUTHOR_NAME
from utils import get_latest_url, set_latest_url

WORK_PATH = Path(os.path.dirname(os.path.abspath(__file__)))


def get_joke_url() -> str:
    QUERY_URL = (
        "https://www.zhihu.com/api/v4/"
        "columns/c_1315712092947886080/items"
    )
    http = urllib3.PoolManager(
        cert_reqs="CERT_REQUIRED", ca_certs=certifi.where()
    )
    response = http.request('GET', QUERY_URL).data
    url = json.loads(response)['data'][0]['url']
    return url


def dom2node(dom_node) -> Dict:
    '''
    Generate Node from DOM node.
    :param dom: BeautifulSoup node.
    return: Dict, telegraph node.
    '''
    node = dict()
    if dom_node is NavigableString:
        return str(dom_node)
    node['tag'] = dom_node.name
    if dom_node.name == 'blockquote':
        node['tag'] = 'p'
    if dom_node.name == 'br':
        nn = dom_node.find_next_sibling()
        if nn and nn.name == 'a' and \
                'member_mention' in nn.attrs['class']:
            return '\n\n'
        else:
            return '\n'
    node['attrs'] = dom_node.attrs
    if len(dom_node) > 0:
        node['children'] = [dom2node(n) for n in dom_node]
    return node


def extract_joker_nodes_from_url(url: str) -> List:
    article_id = url.split('/')[-1]
    http = urllib3.PoolManager(
        cert_reqs="CERT_REQUIRED", ca_certs=certifi.where()
    )
    response = http.request('GET', url)
    soup = BeautifulSoup(
        response.data.decode('utf-8').replace('<br/><br/>', '<br/>'),
        features="html.parser"
    )
    init_data = soup.find("script", {"id": "js-initialData"})
    ctnt = json.loads(init_data.text)
    ctnt = ctnt["initialState"]["entities"]["articles"][article_id]["content"]
    nodes = BeautifulSoup(ctnt, features="html.parser")
    contents = list()
    for n in nodes:
        contents.append(dom2node(n))
    return contents


def create_paragraph(joke_url: str) -> str:
    """
    create paragrap page and return the url.
    """
    publish_url = 'https://api.telegra.ph/createPage'
    fields = {
        'path': '瞎扯/如何正确地吐槽/Blabla',
        'return_content': 'true',
        'access_token': ACCESS_TOKEN,
        'title': '',
        'author_name': AUTHOR_NAME,
        'content': list()
    }

    title = "瞎扯 · 如何正确地吐槽 / Blabla"

    fields['content'] = json.dumps(extract_joker_nodes_from_url(joke_url))
    fields['title'] = title

    http = urllib3.PoolManager(
        cert_reqs="CERT_REQUIRED",
        ca_certs=certifi.where()
    )
    response = http.request('POST', publish_url, fields=fields)
    response = response.data.decode('utf-8')
    response = json.loads(response)
    return response['result']['url']


def publish_zhihu_jokes() -> Optional[str]:
    fn = WORK_PATH / "latest_url"
    latest_url = get_latest_url(fn)
    joke_url = get_joke_url()

    if joke_url == latest_url:
        print(joke_url)
        return None
    set_latest_url(fn, joke_url)
    return create_paragraph(joke_url)
