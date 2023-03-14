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
        
data = []

for url in urls:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    td_elements = soup.find_all('td', {'class': 'text-center'})
    for td in td_elements:
        td_text = td.text
        if re.search('\d+\.\d+%', td_text):
            percentage = float(re.search('\d+\.\d+%', td_text).group().replace('%', ''))
            odds, time = None, None
            for inner_td in td.parent.find_all('td', {'class': 'text-center'}):
                inner_td_text = inner_td.text
                if odds is None and re.search('\d+\.\d+', inner_td_text):
                    odds = float(re.search('\d+\.\d+', inner_td_text).group())

#ページ全体のli要素から[hh:mm]を取得し、timeに代入。これはtext-centerクラスのtd要素の中にはないため、ページ全体のli要素から取得する必要がある。
for li in soup.find_all('li'):
    li_text = li.text
    if re.search('\[\d+:\d+\]', li_text):
        time = re.search('\[\d+:\d+\]', li_text).group().replace('[', '').replace(']', '')
        break
    data.append({'percentage': percentage, 'odds': odds, 'time': time, 'url': url})

data_sorted = sorted([d for d in data if d['percentage'] >= 50], key=lambda x: x['percentage'], reverse=True)
for d in data_sorted[:30]:
    print(f"{d['percentage']}% {d['odds']} {d['time']} {d['url']}")
        

