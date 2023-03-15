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
            
            #指数の表示XX.XXptまたはXXX.XXptを取得する。ptに格納する。
            pt_td = tr.find('td', {'class': 'text-center'}, text=re.compile('^\d{2,3}\.\d{2}pt$'))
            if pt_td:
                pt = float(pt_td.text[:-2])
                if pt >= 1.0:
                    item['pt'] = pt
            else:
                item['pt'] = '---'

    # 「電投締切[hh:mm]」の時間を取得する。
    li_elements = soup.find_all('li')
    for li in li_elements:
        li_text = li.text
        if re.search('電投締切\[\d+:\d+\]', li_text):
            time = re.search('電投締切\[\d+:\d+\]', li_text).group()
            for d in data:
                if d['url'] == url:
                    d['time'] = time


# Sort and print
#data = sorted(filter(lambda x: x['percentage'] >= 50, data), key=lambda x: x['percentage'], reverse=True)
#[hh:mm]の時間が早い順に配列をソートする。
data = sorted(data, key=lambda x: x['time'])

# フォーマットを見やすくするために、リストの中身を整形して要素を区切り表のようにする。オッズが2.0以上の場合は、赤字で表示する。
# percentageが50%以上の場合のみ表示する。
for d in data:
    if d['percentage'] >= 50:
        # オッズが2.0以上の場合は赤字で表示する
        if isinstance(d['odds'], float) and d['odds'] >= 2.0:
            print(f"\033[31m{d['percentage']}% {d['time']} {d['url']} {d['odds']} {d['pt']}\033[0m")
        # オッズが2.0未満の場合は通常の色で表示する
        else:
            print(f"{d['percentage']}% {d['time']} {d['url']} {d['odds']} {d['pt']}")




