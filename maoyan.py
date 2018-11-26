#from bs4 import BeautifulSoup as bs
#from urllib import request
#import json
#import requests
#import re
#import csv
#import time
from bs4 import BeautifulSoup as bs
from urllib.error import HTTPError
from urllib.request import urlopen
import json
import csv
import time
headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
	}
	#def __init__(self,url):
	#	self.url = url
def get_html():
	try:
		url = 'https://box.maoyan.com/promovie/api/box/second.json'
		netword=urlopen(url)
	except HTTPError as hp:
		print(hp)
	else:
    # 采用BeautifulSoup来解析，且指定解析器
		html=bs(netword,'lxml')
		return html
		
def download(html):
	one_page_film = []
	p=html.find('p')
	text=p.get_text()
	#将数据转换为python能够处理的格式
	jsonObj = json.loads(text)
	#获取字典里面特定的键对应的键值
	data = jsonObj.get('data')
	#想要的数据就在字典的键’list‘对应的值
	lists = data.get('list')
	#print(type(lists)==type([]))判断类型
	for list in lists:
		film_dict = {}
		#获取字典里面特定的键对应的键值，并存储到列表中去
		#avgShowView
		film_dict['movieName'] = list.get('movieName')
		film_dict['releaseInfo'] = list.get('releaseInfo')
		film_dict['sumBoxInfo'] = list.get('sumBoxInfo')
		film_dict['boxInfo'] = list.get('boxInfo')
		film_dict['boxRate'] = list.get('boxRate')
		film_dict['showInfo'] = list.get('showInfo')
		film_dict['showRate'] = list.get('showRate')
		film_dict['avgShowView'] = list.get('avgShowView')
		film_dict['avgSeatView'] = list.get('avgSeatView')
		print(film_dict)
		one_page_film.append(film_dict)
	return one_page_film

def save_infor(one_page_film):
	with open("猫眼专业版票房.csv","w") as csvfile:
		csv_file = csv.writer(csvfile)
		csv_file.writerow(['电影名称', '上映天数', '总票房', '综合票房','票房占比', '排片场次', '排片占比', '场均人次', '上座率'])
		for one in one_page_film:
			csv_file.writerow([one['movieName'], one['releaseInfo'], one['sumBoxInfo'], one['boxInfo'],one['boxRate'], one['showInfo'], one['showRate'],one['avgShowView'], one['avgSeatView']])
		
if __name__ =='__main__':
	 # 请求页面
	html = get_html()
	# 提取信息
	one_page_film = download(html)
	if one_page_film:
	# 存储信息
		save_infor(one_page_film)
	time.sleep(2)