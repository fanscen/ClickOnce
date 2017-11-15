import urllib2

def download1(url):
	return urllib2.urlopen(url).read()
	
def download(url,numretries = 2):
	print "Downloading: ", url
	
	try:
		html = urllib2.urlopen(url).read()
	except urllib2.URLError as e:
		print("Downloading error", e.reason)
		html = None
		if numretries > 0:
			if hasattr(e,'code') and 500 <= e.code < 600:
				#retry 5xx HTTP errors
				return download(url, numretries -1)		
	return html

print download('http://www.sina.com')