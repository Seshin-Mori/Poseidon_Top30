import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import pytz

# 日本時間を取得するための設定
JST = pytz.timezone('Asia/Tokyo')

# YYYYMMDD format
today = datetime.now(JST).strftime("%Y%m%d")

# URLのリストを作成
urls = []
for i in range(1, 25):
    urls.append(f"https://poseidon-boatrace.net/race/{today}/{i}")
    for j in range(1, 13):
        urls.append(f"https://poseidon-boatrace.net/race/{today}/{i}/{j}R")

# 正規表現でパーセンテージを取得
data = []
for url in urls:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    td_elements = soup.find_all('td', {'class': 'text-center'})
    for td in td_elements:
        if re.search('\d+\.\d+%', td.text):
            percentage = float(re.search('\d+\.\d+%', td.text).group().replace('%', ''))
            data.append({'url': url, 'percentage': percentage})

# パーセンテージの高い順にソートして上位30件を表示
data_sorted = sorted(data, key=lambda x: x['percentage'], reverse=True)
for i in range(30):
    #もし30個の中に同じURLのものがあれば、被っているものの中から一番パーセンテージが高いものだけを表示。被りなしで30個を表示する。
    if data_sorted[i]['url'] != data_sorted[i+1]['url']:
        print(data_sorted[i])

