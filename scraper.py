import bs4 as bs
import urllib.request


source = urllib.request.urlopen("http://www.bbc.co.uk/news").read()
soup = bs.BeautifulSoup(source, 'lxml')

print(soup.title.string)
