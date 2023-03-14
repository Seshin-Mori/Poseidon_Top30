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
#X.Xをオッズとして取得。---の場合---を入れる
for url in urls:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    td_elements = soup.find_all('td', {'class': 'text-center'})
    for td in td_elements:
        if re.search('\d+\.\d+', td.text):
            odds = float(re.search('\d+\.\d+', td.text).group())
            for d in data:
                if d['url'] == url:
                    d['odds'] = odds
        elif re.search('---', td.text):
            for d in data:
                if d['url'] == url:
                    d['odds'] = '---'
#urlのページからli属性（クラス名なし）を取得、[hh:mm]を取得
for url in urls:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    li_elements = soup.find_all('li')
    for li in li_elements:
        if re.search('\[\d+:\d+\]', li.text):
            time = re.search('\[\d+:\d+\]', li.text).group()
            for d in data:
                if d['url'] == url:
                    d['time'] = time

# パーセンテージの高い順にソートして上位30件を表示50%以上のものを表示
data.sort(key=lambda x: x['percentage'], reverse=True)
for d in data:
    if d['percentage'] >= 50:
        print(d)

