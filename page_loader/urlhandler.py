import urllib.parse
import os.path
import re
import mimetypes

mimetypes.init()


def _get_mime_ext(content_type):
    return mimetypes.guess_extension(content_type, strict=False)


def _url_to_path(url):
    return re.sub(r'[^0-9a-zA-Z]', '-', url)


class UrlHandler:
    def __init__(self, url):
        self._url = urllib.parse.urlsplit(url)

    @property
    def scheme(self):
        return self._url.scheme

    @property
    def netloc(self):
        return self._url.netloc

    @property
    def path(self):
        return self._url.path

    @property
    def islocal(self):
        return len(self.scheme) == 0 and len(self.netloc) == 0

    def get_url(self, strip_scheme=False):
        if not strip_scheme:
            return self._url.geturl()

        scheme = f'{self.scheme}://'
        return self._url.geturl().replace(scheme, '', 1)

    def join(self, other_url):
        if isinstance(other_url, UrlHandler):
            other_url = other_url.get_url()
        joined_url = urllib.parse.urljoin(self.get_url(), other_url)
        return UrlHandler(joined_url)

    def to_filepath(self, mimetype=''):
        """
        How to determine file extension?
        1) if path has file extension then use it
        2) if mimetype has been provided then use in case filepath has no extension,
           otherwise - ignore mimetype and use path extension
        3) if neither filepath extension nor mimetype is present, use '.html'
        """
        path, ext = os.path.splitext(self.path)
        if not ext:
            guessed_ext = _get_mime_ext(mimetype)
            ext = guessed_ext if guessed_ext is not None else '.html'

        return _url_to_path(self.netloc + path) + ext
