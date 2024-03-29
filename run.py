from channel.model import Channel
from zhihu.joker import publish_zhihu_jokes
from gamersky.joker import generate_gif_joke_messages
from gamersky.joker import generate_image_joke_messages

channel = Channel()


messages = generate_gif_joke_messages()
for msg in messages[:20]:
    channel.send_video(msg.image_src, msg.caption)

messages = generate_image_joke_messages()
for msg in messages[:20]:
    channel.send_photo(msg.image_src, msg.caption)

zhihu_joke_paragraph_url = publish_zhihu_jokes()
if zhihu_joke_paragraph_url:
    print("send url")
    channel.send_text(zhihu_joke_paragraph_url)
