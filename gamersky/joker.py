from typing import List, Optional
from pathlib import Path
import os

import requests
from bs4 import BeautifulSoup
import json

from .models import ImageMessage, Article
from utils import get_latest_url, set_latest_url

WORK_PATH = Path(os.path.dirname(os.path.abspath(__file__)))


def page_to_image_messages(url: str) -> List[ImageMessage]:
    res = requests.get(url)
    if res.status_code != 200:
        print("page_url", url)
        print(res.status_code)
        return []
    res.encoding = res.apparent_encoding
    soup = BeautifulSoup(res.text, features="html.parser")
    ctnt_div = soup.find_all("div", {"class":"Mid2L_con"})[0]
    # ctnts = ctnt_div.find_all("p", {"style": "text-align: center;"})
    ctnts = ctnt_div.find_all("p")

    messages: List[ImageMessage] = []
    for ctnt in ctnts:
        if ctnt.img is None:
            continue
        image_src = ctnt.img["src"]
        caption = ctnt.text.strip()
        messages.append(
            ImageMessage(image_src, caption)
        )
    return messages


def article_to_image_messages(url: str) -> List[ImageMessage]:
    messages = []
    page_ext = Path(url).suffix
    page = 1

    _messages = page_to_image_messages(url)
    while _messages:
        messages += _messages
        page += 1
        _url = url.replace(page_ext, f"_{page}{page_ext}")
        _messages = page_to_image_messages(_url)
    return messages


def get_articles(page: int) -> List[Article]:
    url = (
        "https://db2.gamersky.com/LabelJsonpAjax.aspx?jsondata="
        "%0A%7B%22type%22%3A%22updatenodelabel%22%2C%22isCache%22%3Atrue%2C%22"
        "cacheTime%22%3A60%2C%22nodeId%22%3A%2220107%22%2C%22"
        f"page%22%3A{page}%7D"
    )
    res = requests.get(url)
    body = json.loads(res.text.split("(", maxsplit=1)[1][:-2])["body"]
    soup = BeautifulSoup(body)

    articles = []
    for li in soup.find_all("li"):
        title_div = li.find_all("div", {"class": "tit"})[0]
        title = title_div.text
        url = title_div.find_all("a", {"class": "tt"})[0]["href"]
        articles.append(Article(title, url))
    return articles


def get_joke_article_url(
    *, tail: str, head="搞笑 |", max_page=5
) -> Optional[str]:
    for p in range(max_page):
        for article in get_articles(page=p):
            if not article.title.startswith(head):
                continue
            if not article.title.endswith(tail):
                continue
            return article.url


def generate_image_joke_messages() -> List[ImageMessage]:
    fn = WORK_PATH / "latest_image_url"
    latest_url = get_latest_url(fn)
    joke_url = get_joke_article_url(tail="囧图")
    print(joke_url)
    if latest_url == joke_url:
        return []
    set_latest_url(fn, joke_url)
    return article_to_image_messages(joke_url)


def generate_gif_joke_messages() -> List[ImageMessage]:
    fn = WORK_PATH / "latest_gif_url"
    latest_url = get_latest_url(fn)
    joke_url = get_joke_article_url(tail="动态图")
    print(joke_url)
    if latest_url == joke_url:
        return []
    set_latest_url(fn, joke_url)
    return article_to_image_messages(joke_url)
