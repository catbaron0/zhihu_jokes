import time
from functools import wraps

import requests

from .config import BOT_TOKEN


def retry(func, retry=4):
    @wraps(func)
    def wrapper(*args, **kwargs):
        for i in range(retry):
            res = func(*args, **kwargs)
            if res.status_code == 200:
                return res
            print(res)
            print(res.text)
            print(f"retry for the {i+1}th time.")
            time.sleep(5)
    return wrapper


@retry
def send_text(text):
    data = {
        'chat_id': '@laobai_interesting',
        'text': text,
    }
    api_url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?'
    return requests.post(api_url, data=data)


@retry
def send_photo(img_url, caption):
    data = {
        'chat_id': '@laobai_interesting',
        'photo': img_url,
        'caption': caption,
        'disable_notification': True
    }
    api_url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto?'
    return requests.post(api_url, data=data)


@retry
def send_gif(gif_url, caption):
    data = {
        'chat_id': '@laobai_interesting',
        'caption': caption,
        'disable_notification': True
    }
    gif_data = requests.get(gif_url).content
    files = {
        'animation': ('animation.gif', gif_data)
    }
    api_url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendAnimation'
    return requests.post(api_url, data=data, files=files)
