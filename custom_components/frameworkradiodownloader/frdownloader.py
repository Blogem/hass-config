import re
import urllib
import wget
from bs4 import BeautifulSoup

FR_ARCHIVE_PAGE = 'http://www.frameworkradio.net/archive/'

def deduplicatelist(l):
  return list(dict.fromkeys(l))

with urllib.request.urlopen(FR_ARCHIVE_PAGE) as response:
    fr_archive = response.read()

soup = BeautifulSoup(fr_archive, features="lxml")

links = []
i = 0
for link in soup.find_all('a'):
    href = link.get('href')
    # only download episodes from 600 and up (up to 9999)
    result = re.match('^.*/\d{4}/\d{2}/([6-9]\d{2}|[1-9]\d{3})-.*$', href)

    if result:
        i += 1
        print('Parsing '+href)
        with urllib.request.urlopen(href) as response:
            fr_podcast = response.read()

        soup_podcast = BeautifulSoup(fr_podcast, features="lxml")
        
        for link in soup_podcast.find_all('a'):
            href = link.get('href')
            result = re.match('^.*\/s\/.*\.mp3$', href)

            if result:
                links.append(href)

links = deduplicatelist(links)

for link in links:
    print('Downloading '+link)
    file = wget.download(link)
    print ('Downloaded '+file)



