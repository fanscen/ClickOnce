import urllib2
import re
import urlparse

def download1(url):
	return urllib2.urlopen(url).read()
	
def download(url, user_agent = 'wswp', numretries = 2):
	print "Downloading: ", url
	headers = {'User-agent': user_agent}
	request = urllib2.Request(url, headers = headers)
	try:
		html = urllib2.urlopen(request).read()
	except urllib2.URLError as e:
		print("Downloading error", e.reason)
		html = None
		if numretries > 0:
			if hasattr(e,'code') and 500 <= e.code < 600:
				#retry 5xx HTTP errors
				html = download(url, numretries -1)		
	return html

def link_crawler(seed_url, link_regex):
	"""Crawl from the given seed URl following links matched by link_regex
	"""
	crawl_queue =  [seed_url]
	while crawl_queue:
		url = crawl_queue.pop()
		html = download(url)
		#filter for links matching our regular expression
		for link in get_links (html):
			if re.match(link_regex, link):
				link = urlparse.urljoin(seed_url, link)
				crawl_queue.append(link)
				
def get_links(html):
	"""return a list of links from html
	"""
	webpage_regex = re.compile('<a[^>]>+href=["\'](.*?)["\']', re.IGNORECASE)
	return webpage_regex.findall(html)

link_crawler('http://example.webscraping.com', '/(index|view)')