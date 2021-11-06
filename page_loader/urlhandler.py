from urllib.parse import urlparse, ParseResult
import os.path
import re


def replace_aplha_to_char(old_string, char):
    return re.sub(r'[^0-9a-zA-Z]', char, old_string)


class UrlHandler:
    def __init__(self, url):
        urlparsed = urlparse(url)
        self.scheme = urlparsed.scheme
        self.netloc = urlparsed.netloc
        self.path = urlparsed[2:]  # iterable

    @property
    def is_local(self):
        return len(self.scheme) == 0 and len(self.netloc) == 0

    def get_url(self, strip_scheme=False):
        scheme = self.scheme if not strip_scheme else ''
        url = ParseResult(scheme, self.netloc, *self.path).geturl()
        if strip_scheme:
            return url.replace(r'//', '', 1)
        return url

    def to_filepath(self, only_netloc=False):
        if only_netloc:
            return replace_aplha_to_char(self.netloc, '-')

        url = self.get_url(strip_scheme=True)
        ext = ''
        if self.path[0]:
            url, ext = os.path.splitext(url)

        return replace_aplha_to_char(url, '-') + ext
