# Crawling random webpages
# ------------------------

# Part 1: Getting 10.000 random URLS
# ----------------------------------
# How?: Searching randomly on Google
# Algorithm:
#    Our query Q is initially "DTU"
#    Until 10.000 URLs have been found {
#       Search for Q and look at the first or second result page
#       Pick 3 random URLs (if 3 does not exist, then Q := 3 random letters)
#       Q := 2 random words from the search results page
#    }

# https://www.google.com/search?q=test&lr=lang_en&pws=0&start=20
#                                 ^       ^           ^       ^
#                               query  language   personal?  ranking

import random
import urllib2
import BeautifulSoup
import nltk
import pickle
import time

# Continue where we left
try:
    Q, url_list = pickle.load(open("url_list.pydata", "rb" ))
except IOError:
    Q = "DTU"
    url_list = []

while len(url_list) < 10000:
    # Sending GET request
    start = random.randint(1, 2) * 10
    url = 'https://www.google.com/search?q=%s&lr=lang_en&pws=0&safe=off&start=%d' % (Q, start)
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    headers={'User-Agent':user_agent,}
    request = urllib2.Request(url, None, headers)
    html = urllib2.urlopen(request).read()
    # Add three URLs
    soup = BeautifulSoup.BeautifulSoup(html)
    urls = [a['href'] for a in soup.findAll('a', attrs={'class':'l'})]
    try: # We might not be able to smale 3 results
        url_list.extend(random.sample(urls, 3))
        # Get 2 new query words
        text = nltk.clean_html(html)
        wordlist = nltk.word_tokenize(text)
        Q = "+".join(random.sample(wordlist, 2))
    except ValueError:
        print "Oops! Not enough search results for: %r" % Q
        Q = ''.join(random.sample([l for l in 'abcdefghijklmnopqrstuvwxyz'],3))
        print "Now searching for %r" % Q
    # Backup data in case of an error
    pickle.dump((Q,url_list),open("url_list.pydata", "wb" ))
    print "Length of url_list: %d, Last search query: %r" % (len(url_list), Q)
    time.sleep(3)

