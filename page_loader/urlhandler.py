from urllib.parse import urlparse, ParseResult, urljoin
import os.path
import re
import mimetypes

mimetypes.init()


def get_mime_ext(content_type):
    return mimetypes.guess_extension(content_type, strict=False) or ''


def transform_url(url):
    return re.sub(r'[^0-9a-zA-Z]', '-', url)


class UrlHandler:
    def __init__(self, url):
        urlparsed = urlparse(url)
        self.scheme = urlparsed.scheme
        self.netloc = urlparsed.netloc
        path, etc = urlparsed.path, urlparsed[3:]  # iterable
        if path == '/':
            path = ''
        self.path = (path,) + etc

    @property
    def is_local(self):
        return len(self.scheme) == 0 and len(self.netloc) == 0

    def get_url(self, strip_scheme=False):
        scheme = self.scheme if not strip_scheme else ''
        url = ParseResult(scheme, self.netloc, *self.path).geturl()
        if strip_scheme:
            return url.replace(r'//', '', 1)
        return url

    def to_filepath(self, out_dir='', mimetype='', *, only_netloc=False):
        """
        Note: If extension is not present in the "path" part of the url,
        function uses supplied mimetype to guess the extension. If successful
        it appends according extension to the filepath, otherwise it leaves
        url as is.
        """
        if only_netloc:
            return os.path.join(out_dir, transform_url(self.netloc))

        url = self.get_url(strip_scheme=True)

        gussed_ext = get_mime_ext(mimetype)
        if not self.path[0]:
            fullname = transform_url(url) + gussed_ext
        else:
            new_url, ext = os.path.splitext(url)
            if ext == '':
                ext = gussed_ext
            fullname = transform_url(new_url) + ext

        return os.path.join(out_dir, fullname)

    def join(self, other_url):
        if isinstance(other_url, UrlHandler):
            other_url = other_url.get_url()
        return urljoin(self.get_url(), other_url)

    @staticmethod
    def urljoin(url1, url2):
        if isinstance(url1, UrlHandler):
            url1 = url1.get_url()
        if isinstance(url2, UrlHandler):
            url2 = url2.get_url()
        return urljoin(url1, url2)
