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

# リストの中身をループして、パーセンテージ、オッズ、時間を取得する。
for url in urls:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    td_elements = soup.find_all('td', {'class': 'text-center'})

    for td in td_elements:
        td_text = td.text
        if re.search('\d+\.\d+%', td_text):
            percentage = float(re.search('\d+\.\d+%', td_text).group()[:-1])
            item = {'url': url, 'percentage': percentage}
            data.append(item)

        elif re.search('\d+\.\d+', td_text):
            odds = float(re.search('\d+\.\d+', td_text).group())
            for d in data:
                if d['url'] == url:
                    d['odds'] = odds

        elif td_text == '---':
            for d in data:
                if d['url'] == url:
                    d['odds'] = td_text
# [hh:mm]の時間を取得する。
    li_elements = soup.find_all('li')
    for li in li_elements:
        li_text = li.text
        if re.search('\[\d+:\d+\]', li_text):
            time = re.search('\[\d+:\d+\]', li_text).group()
            for d in data:
                if d['url'] == url:
                    d['time'] = time

# Sort and print
#data = sorted(filter(lambda x: x['percentage'] >= 50, data), key=lambda x: x['percentage'], reverse=True)
#[hh:mm]の時間が早い順に配列をソートする。
data = sorted(data, key=lambda x: x['time'])

#フォーマットを見やすくするために、リストの中身を整形して要素を区切り表のようにする。オッズが2.0以上の場合は、赤字で表示する。
for d in data:
    if d['odds'] == '---':
        d['odds'] = '---'
    elif d['odds'] >= 2.0:
        d['odds'] = f"\033[31m{d['odds']}\033[0m"
    else:
        d['odds'] = f"{d['odds']}"
    print(f"{d['url']} {d['percentage']}% {d['odds']} {d['time']}")


