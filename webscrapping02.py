import pandas as pd 
import requests
from bs4 import BeautifulSoup
import time # to time the requests
from multiprocessing import Process, Queue, Pool
import threading
import sys


book_list = pd.read_csv('trading_book_top_20_list.csv')
# print(book_list.head(3))
book_list['Author'] = 'walala'
book_list['Ratings'] = 'bahaha'
book_list['Publish_year'] = 'dididi'
book_list['n of ratings'] = 'fafafa'
# print(book_list.head(3))

proxies = { # define the proxies which you want to use
  'http': 'http://191.19.121.13:443',
  'https': 'http://191.22.121.13:443',
}
startTime = time.time()
qcount = 0 # the count in queue used to track the elements in queue
#products=[] # List to store name of the product
#prices=[] # List to store price of the product
#ratings=[] # List to store ratings of the product
# no_pages = 9 # no of pages to scrape in the website (provide it via arguments)

def get_data(index, df):
    url = 'https://www.stocktrader.com'+df.iloc[index,1]
    headers = {
                "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64;x64; rv:66.0) Gecko/20100101 Firefox/66.0", 
                "Accept-Encoding":"gzip, deflate","Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 
                "DNT":"1","Connection":"close", 
                "Upgrade-Insecure-Requests":"1"
                }
    r = requests.get(url, headers=headers)#,proxies=proxies)
    content = r.content
    soup = BeautifulSoup(content,'html.parser')
    if soup.find('a',class_ = 'a-link-normal contributorNameID'):
        author = soup.find('a',class_ = 'a-link-normal contributorNameID').string
        if author:
            book_list['Author'][index] = author
    if soup.find('span',class_='a-icon-alt'):
        rating = soup.find('span',class_='a-icon-alt').string
        if rating:
            book_list['Ratings'][index] = rating
    if soup.find(id = 'productSubtitle'):
        year = soup.find(id = 'productSubtitle').string
        if year:
            book_list['Publish_year'][index] = year
    if soup.find(id = 'acrCustomerReviewText'):
        count = soup.find(id = 'acrCustomerReviewText').string
        if count:
            book_list['n of ratings'][index] = count
            
filter_index = book_list[book_list['0'].apply(lambda str: str.startswith('/go'))].index

for index in filter_index:
    get_data(index, book_list)
book_list.to_csv('debug01.csv')




