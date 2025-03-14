import sys

from channel.utils import send_gif, send_photo, send_text
from zhihu.joker import publish_zhihu_jokes
from gamersky.joker import generate_gif_joke_messages
from gamersky.joker import generate_image_joke_messages


if sys.argv[1] == "gg":
    messages = generate_gif_joke_messages()
    print("image gif number", len(messages))
    for msg in messages:
        res = send_gif(msg.image_src, msg.caption)
        print(msg)
        print(res)

if sys.argv[1] == "gi":
    messages = generate_image_joke_messages()
    print("image message number", len(messages))
    for msg in messages:
        res = send_photo(msg.image_src, msg.caption)
        print(msg)
        print(res)

if sys.argv[1] == "zh":
    zhihu_joke_paragraph_url = publish_zhihu_jokes()
    if zhihu_joke_paragraph_url:
        send_text(zhihu_joke_paragraph_url)

