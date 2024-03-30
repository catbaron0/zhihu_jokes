from .config import BOT_TOKEN
import urllib3
import certifi


class Channel:
    def __init__(self):
        self.http = urllib3.PoolManager(
            cert_reqs="CERT_REQUIRED",
            ca_certs=certifi.where()
        )

    def send_text(self, text):
        data = {
            'chat_id': '@laobai_interesting',
            'text': text,
        }
        api_url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?'
        self.http.request('POST', api_url, fields=data)

    def send_photo(self, img_url, caption):
        data = {
            'chat_id': '@laobai_interesting',
            'photo': img_url,
            'caption': caption,
        }
        api_url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto?'
        self.http.request(
            'POST', api_url, fields=data, disable_notification=True
        )

    def send_video(self, video_url, caption):
        data = {
            'chat_id': '@laobai_interesting',
            'video': video_url,
            'caption': caption,
        }
        api_url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendVideo?'
        self.http.request(
            'POST', api_url, fields=data, disable_notification=True
        )
