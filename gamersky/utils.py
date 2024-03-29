# %%
from bs4 import BeautifulSoup
import requests
url = "https://www.gamersky.com/news/202305/1597522_2.shtml"

# %%
res = requests.get(url)
res.encoding = res.apparent_encoding
# %%
soup = BeautifulSoup(res.text, features="html.parser")
# res.json()
# %%
div = soup.find_all("div", {"class":"Mid2L_con"})[0]
# %%
ctnts = div.find_all("p", {"style": "text-align: center;"})
# %%
# ctnts[1].find_all("img")[0]["src"]
ctnts[0].text

# %%

url = "https://www.gamersky.com/ent/"
url = 'https://db2.gamersky.com/LabelJsonpAjax.aspx?jsondata={"type":"updatenodelabel","isCache":true,"cacheTime":60,"nodeId":"20107","page":2}'
import json
body = json.loads(requests.get(url).text.split("(", maxsplit=1)[1][:-2])["body"]
# %%
import re
res = re.sub("\s+", " ", body)

# %%
soup = BeautifulSoup(res)

# %%
time = soup.find_all("li")[0].find_all("div", {"class": "time"})[0].text
# %%
from datetime import datetime, date
dt = datetime.strptime(time, "%Y-%m-%d %H:%M")

# %%
date.today()

# %%

soup.find_all("li")[0].find_all("div", {"class": "tit"})[0].find_all("a", {"class": "tt"})
# %%.
page = 2
url = (
        "https://db2.gamersky.com/LabelJsonpAjax.aspx?jsondata="
        "%0A%7B%22type%22%3A%22updatenodelabel%22%2C%22isCache%22%3Atrue%2C%22"
        "cacheTime%22%3A60%2C%22nodeId%22%3A%2220107%22%2C%22"
        f"page%22%3A{page}%7D"
    )

# %%
requests.get("https://www.gamersky.com/news/202403/1726936_1.shtml").status_code
# %%
from pathlib import Path
url = "https://www.gamersky.com/news/202403/1726936.shtml"
# base = Path(url).as_uri().parent
# stem = Path(url).stem
ext = Path(url).suffix

# base / (stem + "_2" + ext)
url.replace(ext, "_1"+ext)


# %%
