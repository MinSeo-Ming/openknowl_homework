import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbsparta

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

data = requests.get('https://www.genie.co.kr/chart/top200?ditc=D&rtm=N&ymd=20200713',headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')
musicLists = soup.select('#body-content > div.newest-list > div > table > tbody > tr')

for music in musicLists:
    rank = music.select_one('td.number').text.split()[0]
    title = music.select_one('td.info > a.title.ellipsis').text.split('\n')[-1].lstrip()
    singers = music.select_one('td.info > a.artist.ellipsis').text
    doc = {
        'rank': rank,
        'title': title,
        'artist':singers
    }
    db.musicchart.insert_one(doc)
    print(rank, title, singers)
