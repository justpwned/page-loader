import requests
import os
import bs4
import bs4.formatter
import re
from page_loader.urlhandler import UrlHandler

# Monkeypatching bs4 prettify method to include a custom indent parameter
orig_prettify = bs4.BeautifulSoup.prettify
r = re.compile(r'^(\s*)', re.MULTILINE)


def prettify(self, encoding=None, formatter="minimal", indent_width=4):
    return r.sub(r'\1' * indent_width, orig_prettify(self, encoding, formatter))


bs4.BeautifulSoup.prettify = prettify


class UnsortedAttributes(bs4.formatter.HTMLFormatter):
    def attributes(self, tag):
        for k, v in tag.attrs.items():
            if k == 'm':
                continue
            yield k, v


# END

def write_file(filepath, content):
    with open(filepath, 'wb') as fd:
        if isinstance(content, str):
            content = content.encode()
        fd.write(content)


def download_asset(url):
    if isinstance(url, UrlHandler):
        url = url.get_url()
    r = requests.get(url)
    r.raise_for_status()
    mimetype = r.headers.get('content-type', '').split(';')[0]
    return r.content, mimetype


def save_assets(assets, outdir):
    for path, content in assets:
        filepath = os.path.join(outdir, path)
        write_file(filepath, content)


def transform_assets_refs_to_local(html, out_dir, base_urlhandler):
    soup = bs4.BeautifulSoup(html, 'html.parser')

    assets = []
    images = soup.find_all('img')
    for img in images:
        old_src = img.get('src')
        if not old_src:
            continue

        img_src_url = base_urlhandler.join(old_src)
        img_content, img_mimetype = download_asset(img_src_url)
        src_handler = UrlHandler(old_src)
        if src_handler.is_local:
            new_asset_name = f'{base_urlhandler.to_filepath(only_netloc=True)}-' \
                             f'{src_handler.to_filepath(mimetype=img_mimetype).lstrip("-")}'
            new_src = os.path.join(out_dir, new_asset_name)
        else:
            new_src = src_handler.to_filepath(out_dir, img_mimetype)

        img['src'] = new_src
        assets.append((new_src, img_content))

    # new_html, [(asset_content, path)]
    return soup.prettify(formatter=UnsortedAttributes()), assets


# TODO: LOTS of stuff to refactor
def download(url, out_dir):
    content, mimetype = download_asset(url)

    url_handler = UrlHandler(url)
    out_filepath = url_handler.to_filepath(mimetype=mimetype)

    if mimetype == 'text/html':
        no_ext_out_filepath, _ = os.path.splitext(out_filepath)
        assets_dir = f'{no_ext_out_filepath}_files'
        content, assets = transform_assets_refs_to_local(content, assets_dir, url_handler)

        if len(assets) > 0:
            assets_out_dir = os.path.join(out_dir, assets_dir)
            os.mkdir(assets_out_dir)
            save_assets(assets, out_dir)

    out_filepath = os.path.join(out_dir, out_filepath)
    write_file(out_filepath, content)
    return out_filepath
