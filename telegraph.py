import json
import os
from pathlib import Path
import certifi
import urllib3
import utils as U
from config import ACCESS_TOKEN, AUTHOR_NAME, BOT_TOKEN
work_path = Path(os.path.dirname(os.path.abspath(__file__)))

publish_url = 'https://api.telegra.ph/createPage'
fields = {
    'path': '瞎扯/如何正确地吐槽/Blabla',
    'return_content': 'true',
    'access_token': ACCESS_TOKEN,
    'title': '',
    'author_name': AUTHOR_NAME,
    'content': list()
}

TITLE = "瞎扯 · 如何正确地吐槽 / Blabla"
joker_url = U.get_joker_url()
f_last_url = work_path / 'last_path'
try:
    with open(f_last_url, 'r') as f:
        last_url = f.read().strip()
except Exception:
    last_url = ''
if joker_url == last_url:
    exit(0)
else:
    with open(f_last_url, 'w') as f:
        f.write(joker_url)

fields['content'] = json.dumps(U.extract_joker_nodes_from_url(joker_url))
fields['title'] = TITLE

http = urllib3.PoolManager(
    cert_reqs="CERT_REQUIRED",
    ca_certs=certifi.where()
)
response = http.request('POST', publish_url, fields=fields).data.decode('utf-8')
response = json.loads(response)
telegraph_url = response['result']['url']
channel_api = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?'
data = {
    'chat_id': '@laobai_interesting',
    'text': telegraph_url,
}
http.request('POST', channel_api, fields=data)
