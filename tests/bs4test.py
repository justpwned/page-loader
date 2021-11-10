import bs4
import requests
from urllib.parse import urljoin, urlsplit, SplitResult, urlunsplit
from page_loader.urlhandler import UrlHandler
import os.path

# r = requests.get('https://example.com')
# soup = bs4.BeautifulSoup(r.content, 'lxml')
#
# print(soup.prettify())
# print('\n-----------------------------------------------\n')
#
# soup.a['href'] = 'hello'
# print(soup.prettify())
#
url1 = 'https:/example.com/images/'
url2 = 'https://google.com/assets/image1.png'
# requests.get(urlparse(url1).geturl())
#
# print(urljoin(url1, url2))
# url = 'https://example.com/images'
#
# url_handler = UrlHandler(url )
# print(url_handler.to_filepath(only_netloc=True))

path, ext = os.path.splitext('hellohel')
print(path)
print(ext)

if not ext:
    print('hell')
