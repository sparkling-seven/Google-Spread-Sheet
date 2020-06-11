from bs4 import BeautifulSoup
import requests
import time
from itertools import zip_longest
import pandas as pd, numpy as np


import json
import  gspread
from googleapiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import get_as_dataframe, set_with_dataframe


scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('tidal-digit-276902-efcc36a80aec.json', scope)
gc = gspread.authorize(credentials)
SPREADSHEET_KEY = '1DxPdf4JAcQp5LmKAEmBX2wuYW1j4ckva53Tnwm_byBg'
worksheet = gc.open_by_key(SPREADSHEET_KEY)
wb = worksheet.sheet1



url = 'https://gyao.yahoo.co.jp/ct/anime/'
r = requests.get(url)

soup = BeautifulSoup(r.text, 'html.parser')


section1 = soup.find_all('h2', class_ = 'section-header-title')

time.sleep(3)

sections = soup.find_all(class_='item-carousel-container')

time.sleep(3)

section_urls = soup.find_all('a')


header_titles = []
for i in section1:
  sec = i.text
  header_titles.append(sec)

# Pタグではなく、sectionsからtextを取得する?が、うまくいかない
# anime_titles = []
# for section in sections:
#   section_ = section.find_all('p')
#   anime_titles.append(section_)

# 別の方法でタイトルを取得するlenは22
anime_titles = []
for section in soup.find_all(class_='item-carousel-container'):
  p_tag = section.find_all('p')
  anime_titles.append(p_tag)

anime_titles_len = []
for i in anime_titles:
  length = len(i)
  anime_titles_len.append(length)

cumulative = np.cumsum(anime_titles_len)

anime_titles_text = []
for i in anime_titles:
  for j in i :
    anime_titles_text.append(j.text)

url_lists = []
for i in soup.find_all(class_='item-carousel-container'):
    a_tag = i.find_all('a')
    # url_lists.append(a_tag)
    for j in a_tag:
        link = j.get('href')
        url_lists.append(link)

# url_lists = []
# for section in sections:
#   section_ = section.find_all('a')
#   url_lists.append(section_)



# まとめてイッキ見！　一挙配信中のアニメ
anime1 = []
for i in anime_titles_text[cumulative[1]:cumulative[2]]:
  animeTitle_ = i.split('【一挙配信】')[1]
  anime1.append(animeTitle_)

# anime_titles1 = []
# for section in sections:
#   anime_titles.append(section.text)

# anime_titles2 = []
# for i in anime_titles[2]:
#   a = i.split('【一挙配信】')[0]
#   anime_titles2.append(a)

# 現在テレビ放送中の春アニメ
# anime2 = []
# for i in anime_titles[3]:
#   title = i.string
#   anime2.append(title)



# time.sleep(3)
# まとめてイッキ見！　一挙配信中のアニメ
# Anime_URL1 = []
# for i in url_lists[2]:
#     url = i.get('href')
#     Anime_URL1.append(url)


mydict = {
  header_titles[0]:anime1, 'URL':url_lists[cumulative[1]:cumulative[2]],
  header_titles[1]:anime_titles_text[cumulative[2]:cumulative[3]], 'URL1':url_lists[cumulative[2]:cumulative[3]],
  header_titles[2]:anime_titles_text[cumulative[3]:cumulative[4]], 'URL2':url_lists[cumulative[3]:cumulative[4]],
  header_titles[5]:anime_titles_text[cumulative[6]:cumulative[7]], 'URL3':url_lists[cumulative[6]:cumulative[7]],
  header_titles[6]:anime_titles_text[cumulative[7]:cumulative[8]], 'URL4':url_lists[cumulative[7]:cumulative[8]],
  header_titles[7]:anime_titles_text[cumulative[8]:cumulative[9]], 'URL5':url_lists[cumulative[8]:cumulative[9]],
  header_titles[8]:anime_titles_text[cumulative[9]:cumulative[10]], 'URL6':url_lists[cumulative[9]:cumulative[10]],
  header_titles[9]:anime_titles_text[cumulative[10]:cumulative[11]], 'URL7':url_lists[cumulative[10]:cumulative[11]],
  header_titles[10]:anime_titles_text[cumulative[11]:cumulative[12]], 'URL8':url_lists[cumulative[11]:cumulative[12]],
  header_titles[11]:anime_titles_text[cumulative[12]:cumulative[13]], 'URL9':url_lists[cumulative[12]:cumulative[13]],
  header_titles[12]:anime_titles_text[cumulative[13]:cumulative[14]], 'URL10':url_lists[cumulative[13]:cumulative[14]],
  header_titles[13]:anime_titles_text[cumulative[14]:cumulative[15]], 'URL11':url_lists[cumulative[14]:cumulative[15]],
  header_titles[14]:anime_titles_text[cumulative[15]:cumulative[16]], 'URL12':url_lists[cumulative[15]:cumulative[16]],
  header_titles[15]:anime_titles_text[cumulative[16]:cumulative[17]], 'URL13':url_lists[cumulative[16]:cumulative[17]],
  header_titles[16]:anime_titles_text[cumulative[17]:cumulative[18]], 'URL14':url_lists[cumulative[17]:cumulative[18]],
  header_titles[17]:anime_titles_text[cumulative[18]:cumulative[19]], 'URL15':url_lists[cumulative[18]:cumulative[19]],
  header_titles[18]:anime_titles_text[cumulative[19]:cumulative[20]], 'URL16':url_lists[cumulative[19]:cumulative[20]],
  header_titles[19]:anime_titles_text[cumulative[20]:cumulative[21]], 'URL17':url_lists[cumulative[20]:cumulative[21]],
  }
dict_df = pd.DataFrame({key:pd.Series(value) for key, value in mydict.items()}) 



sh = gc.open_by_key('1DxPdf4JAcQp5LmKAEmBX2wuYW1j4ckva53Tnwm_byBg').worksheet('シート1')

set_with_dataframe(sh, dict_df)
# resize=False, include_index=False




# rows = []
# for i in range(2, 20):
#     rows.append(i)

# # for row, title in zip(rows, anime):
#         # wb.update_cell(row, column, title)
# for row, a1,a2,a3,a4 in zip_longest(rows, anime1, anime2, anime3, anime4, fillvalue=20):
#     wb.update('A:G'+str(row), [[a1,'' , a2, '', a3, '', a4]])      
# anime_title_function(3, 3)
 

# time.sleep(3)

# def anime_url_function(list_num, column):
#     Anime_URL = []
#     for i in url_lists[list_num]:
#         url_ = i.get('href')
#         Anime_URL.append(url_)

#     rows = []
#     for i in range(2,len(Anime_URL)+2):
#         rows.append(i)

#     for row,url in zip(rows,Anime_URL):
#          wb.update_cell(row, column, url)
# anime_url_function(3, 4)




# def anime_title_function(list_num,anime_title):
#   # rows = []
#   # for i in range(0,20):
#   #   rows.append(i)


  
 














