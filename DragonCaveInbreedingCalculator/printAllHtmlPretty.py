from urllib.request import urlopen
from bs4 import BeautifulSoup
url = 'http://dragcave.net/view/TLfo'
page = urlopen(url).read()
soup = BeautifulSoup(page)
prettySoup = soup.prettify();
print(prettySoup);