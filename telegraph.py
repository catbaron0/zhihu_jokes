import json
import certifi
import urllib3
import utils as U
ACCESS_TOKEN = ''
AUTHOR_NAME = ''
publish_url = 'https://api.telegra.ph/createPage'
fields = {
    'path': '瞎扯--如何正确地吐槽--Blabla-09-19',
    'return_content': 'true',
    'access_token': ACCESS_TOKEN,
    'title': '',
    'author_name': AUTHOR_NAME,
    'content': list()
}

TITLE = "瞎扯 · 如何正确地吐槽 / Blabla"
daily_url = 'https://www.zhihu.com/search?q=知乎晚报&utm_content=search_history&type=content'
joker_url = U.get_joker_url(daily_url)

fields['content'] = json.dumps(U.extract_joker_nodes_from_url(joker_url))
fields['title'] = TITLE

http = urllib3.PoolManager(
    cert_reqs="CERT_REQUIRED",
    ca_certs=certifi.where()
)
response = http.request('POST', publish_url, fields=fields).data.decode('utf-8')
response = json.loads(response)
telegraph_url = response['result']['url']
# print(json.loads(response.data.decode('utf-8')))
# print(json.loads(parameters['content']))
channel_api = f'https://api.telegram.org/bot802531612:AAH0vY732QpWrfZAhRlrszeDa7S5eEGuYf0/sendMessage?'
data = {
    'chat_id': '@laobai_interesting',
    'text': 'https://telegra.ph/瞎扯--如何正确地吐槽--Blabla-09-19'
}
http.request('POST', channel_api, fields=data)
