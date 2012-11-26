import BeautifulSoup
import random
import time
import urllib2
import nltk
import pickle

Q = "DTU"
start = random.randint(1, 2) * 10
url = 'https://www.google.com/search?q=%s&lr=lang_en&pws=0&safe=off&start=%d' % (Q, start)
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'    
headers={'User-Agent':user_agent,}
request = urllib2.Request(url, None, headers)
html = urllib2.urlopen(request).read()
# Add three URLs
soup = BeautifulSoup.BeautifulSoup(html)
urls = [a['href'] for a in soup.findAll('a', attrs={'class':'l'})]