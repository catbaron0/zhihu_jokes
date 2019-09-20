import certifi
import urllib3
from typing import Dict, List
from bs4 import BeautifulSoup, NavigableString, Tag


def get_joker_url(url: str) -> str:
    http = urllib3.PoolManager(
        cert_reqs="CERT_REQUIRED",
        ca_certs=certifi.where()
    )
    response = http.request('GET', url)
    soup = BeautifulSoup(
        response.data.decode('utf-8'),
        features="html.parser"
    )
    daily_node = soup.find_all('h2')[0]
    href = daily_node.find_next('a').attrs['href'].strip('/')
    return href


def dom2node(dom_node) -> Dict:
    '''
    Generate Node from DOM node.
    :param dom: BeautifulSoup node.
    return: Dict, telegraph node.
    '''
    node = dict()
    if type(dom_node) == NavigableString:
        # return {'tag': 'p', 'children': [str(dom_node)]}
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
        # pn = dom_node.find_previous_sibling()
        # # node['attrs']['class'] = 'inline'
        # if nn and nn.name == 'br' and pn and pn.name == 'br':
        #     print('removed a br')
        #     return ''
            # return '\naa'
    node['attrs'] = dom_node.attrs
    if len(dom_node) > 0:
        node['children'] = [dom2node(n) for n in dom_node]
    return node


def extract_joker_nodes_from_url(url: str) -> List:
    http = urllib3.PoolManager(
        cert_reqs="CERT_REQUIRED",
        ca_certs=certifi.where()
    )
    response = http.request('GET', url)
    soup = BeautifulSoup(
        response.data.decode('utf-8').replace('<br/><br/>', '<br/>'),
        features="html.parser"
    )
    h2: List[Tag] = soup.find_all("h2")
    joker_node = None
    for n in h2:
        if n.get_text().startswith('🛁'):
            joker_node = n
    assert joker_node
    p_joker_node = joker_node
    contents = list()
    while True:
        p_joker_node = p_joker_node.find_next_sibling()
        if not p_joker_node or p_joker_node.name == 'h2':
            break
        contents.append(dom2node(p_joker_node))
    return contents
