from .config import BOT_TOKEN
import urllib3
import certifi


class Channel:
    def __init__(self):
        self.http = urllib3.PoolManager(
            cert_reqs="CERT_REQUIRED",
            ca_certs=certifi.where()
        )
        self.channel_api = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?'

    def send_text(self, text):
        data = {
            'chat_id': '@laobai_interesting',
            'text': text,
        }
        self.http.request('POST', self.channel_api, fields=data)

    def send_photo(self, img_url, caption):
        data = {
            'chat_id': '@laobai_interesting',
            'photo': img_url,
            'caption': caption,
        }
        self.http.request('POST', self.channel_api, fields=data)
