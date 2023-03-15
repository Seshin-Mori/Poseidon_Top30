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
    tr_elements = soup.find_all('tr')

    for tr in tr_elements:
        percentage_td = tr.find('td', {'class': 'text-center'}, text=re.compile('\d+\.\d+%'))
        if percentage_td:
            percentage = float(percentage_td.text[:-1])
            item = {'url': url, 'percentage': percentage}
            data.append(item)

            odds_td = tr.find('td', {'class': 'text-center'}, text=re.compile('^\d\.\d$'))
            if odds_td:
                odds = float(odds_td.text)
                if odds >= 1.0:
                    item['odds'] = odds
            else:
                item['odds'] = '---'

        
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
#percentageが50%以上の場合のみ表示する。
for d in data:
    if d['percentage'] >= 50:
        if d['odds'] == '---':
            print(f"{d['time']} {d['url']} {d['percentage']}%")
        elif d['odds'] >= 2.0:
            print(f"{d['time']} {d['url']} {d['percentage']}% \033[31m{d['odds']}\033[0m")
        else:
            print(f"{d['time']} {d['url']} {d['percentage']}% {d['odds']}")  


