
import requests
from bs4 import BeautifulSoup
import pandas as pd

URL = 'https://www.stocktrader.com/best-stock-trading-books/'
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')


## First get book title as key, url as value in a dictionary book_link
results = soup.find_all('strong')
book_link = {}
author_name = {}
for c in results:
	title=c.get_text()

	links = []
	for link in c.find_all('a', href = True):
		if link.text:
			links.append(link['href'])
	if len(links) > 0:
		book_link[title] = links
book_link_df = pd.DataFrame(book_link)

book_link_df.T.to_excel('trading_book_top_20.xlsx')
book_link_df.T.to_csv('trading_book_top_20_list.csv')
