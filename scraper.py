#!/usr/bin/python

#import html2text
from html import unescape
from lxml import html
import time
import requests
from lxml import etree
from lxml.etree import tostring

def scrape_entry(url):
	print('Scraping {0}'.format(url))
	page = requests.get(url)
	tree = html.fromstring(page.text)
	html_body = tree.xpath('/html/body/div/table/tr[6]/td[2]/div[1]')[0]
	headers = html_body.xpath('//p/u')
	bodystr = ''.join([etree.tostring(child).decode("utf-8") for child in html_body.iterchildren()])
	title = tree.xpath('/html/body/div/table/tr[6]/td[2]/p[2]/strong')[0].text_content()
	return (title, unescape(bodystr))

def scrape_index():
	page = requests.get('https://www.brown.edu/Administration/News_Bureau/Databases/Encyclopedia/')
	tree = html.fromstring(page.text)
	index = tree.xpath('/html/body/div/table/tr[6]/td[2]/table/tr/td/div/p/a')
	f = lambda x : 'https://www.brown.edu/Administration/News_Bureau/Databases/Encyclopedia/'+ x.get('href')
	return map(f, index)

scrape_entry('https://www.brown.edu/Administration/News_Bureau/Databases/Encyclopedia/search.php?serial=W0060')

for entry in scrape_index():
	title, content = scrape_entry(entry)
	#print('Writing {0}'.format(title))
	f = open('{0}.html'.format(title),'w+')
	f.write(content)
	f.close()
	time.sleep(0.5)

#title, markdown = scrape_entry('https://www.brown.edu/Administration/News_Bureau/Databases/Encyclopedia/search.php?serial=A0040')
#print(markdown)
