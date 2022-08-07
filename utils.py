import certifi
import urllib3
import json
from typing import Dict, List
from bs4 import BeautifulSoup, NavigableString, Tag


def get_joker_url() -> str:
    # QUERY_URL = 'https://zhuanlan.zhihu.com/api/columns/c_1085975047386050560/' \
    #             +'articles?include=data%5B*%5D.admin_closed_comment%2Ccomment_count' \
    #             +'%2Csuggest_edit%2Cis_title_image_full_screen%2Ccan_comment' \
    #             +'%2Cupvoted_followees%2Ccan_open_tipjar%2Ccan_tip%2Cvoteup_count' \
    #             +'%2Cvoting%2Ctopics%2Creview_info%2Cauthor.is_following%2Cis_labeled%2Clabel_info'
    # QUERY_URL = "https://www.zhihu.com/column/c_1315712092947886080"
    QUERY_URL = "https://www.zhihu.com/api/v4/columns/c_1315712092947886080/items"
    http = urllib3.PoolManager(cert_reqs="CERT_REQUIRED", ca_certs=certifi.where())
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
    if type(dom_node) == NavigableString:
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
    http = urllib3.PoolManager(cert_reqs="CERT_REQUIRED", ca_certs=certifi.where())
    response = http.request('GET', url)
    soup = BeautifulSoup(
        response.data.decode('utf-8').replace('<br/><br/>', '<br/>'),
        features="html.parser"
    )
    init_data = soup.find("script", {"id": "js-initialData"})
    ctnt = json.loads(init_data.text)["initialState"]["entities"]["articles"][article_id]["content"]
    nodes = BeautifulSoup(ctnt, features="html.parser")
    # nodes = [n for n in ctnt]
    contents = list()
    for n in nodes:
        contents.append(dom2node(n))
    return contents


if __name__ == "__main__":
    url = get_joker_url()
    print(url)
    print(extract_joker_nodes_from_url(url))