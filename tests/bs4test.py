import bs4
import requests
from urllib.parse import urljoin
from page_loader.urlhandler import UrlHandler

# r = requests.get('https://example.com')
# soup = bs4.BeautifulSoup(r.content, 'lxml')
#
# print(soup.prettify())
# print('\n-----------------------------------------------\n')
#
# soup.a['href'] = 'hello'
# print(soup.prettify())
#
# url1 = 'https://example.com/images/'
# url2 = 'assets/image1.png'
#
# print(urljoin(url1, url2))
url = 'https://example.com/images'

url_handler = UrlHandler(url)
print(url_handler.to_filepath(only_netloc=True))