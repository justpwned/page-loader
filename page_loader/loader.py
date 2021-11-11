import requests
import os
import bs4
from page_loader.urlhandler import UrlHandler
from itertools import chain
from page_loader.progressbar import ProgressBar
from page_loader.exceptions import *
import logging


def write_file(filepath, content):
    with open(filepath, 'wb') as fd:
        if isinstance(content, str):
            content = content.encode()
        fd.write(content)


def download_asset(url):
    if isinstance(url, UrlHandler):
        url = url.get_url()
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as ex:
        raise RequestException(str(ex)) from ex
    mimetype = response.headers.get('content-type', '').split(';')[0]
    return response.content, mimetype


def save_assets(assets, asset_dir):
    for path, content in assets:
        filepath = os.path.join(asset_dir, path)
        write_file(filepath, content)


TAGS_LINK_ATTR = {
    'img': 'src',
    'script': 'src',
    'link': 'href',
    'audio': 'src',
    'video': 'src',
    'source': 'src',
    'object': 'data',
    'track': 'src'
}


def format_html(html):
    return str(html)


def extract_assets_from_html(html, assets_dir, base_urlhandler):
    soup = bs4.BeautifulSoup(html, 'html.parser')

    assets = []
    tags = [tag for tag_name in TAGS_LINK_ATTR for tag in chain(soup.find_all(tag_name)) if
            tag.get(TAGS_LINK_ATTR[tag_name])]

    bar = ProgressBar('Extracting assets: ', max=len(tags))
    for tag in tags:
        attr = TAGS_LINK_ATTR[tag.name]
        orig_src = tag.get(attr)
        if not orig_src:
            continue

        asset_url = base_urlhandler.join(orig_src)
        try:
            content, mimetype = download_asset(asset_url)
        except RequestException:
            continue

        new_asset_name = asset_url.to_filepath(mimetype)
        new_src = os.path.join(assets_dir, new_asset_name)
        tag[attr] = new_src
        assets.append((new_src, content))
        bar.next()

    bar.finish()
    return format_html(soup), assets


def download(url, out_dir):
    try:
        content, mimetype = download_asset(url)
    except RequestException as ex:
        logging.error(str(ex))
        raise

    url_handler = UrlHandler(url)
    url_filepath = url_handler.to_filepath(mimetype)

    if url_filepath.endswith('.html'):
        assets_dir = f'{os.path.splitext(url_filepath)[0]}_files'

        out_assets_filepath = os.path.join(out_dir, assets_dir)
        try:
            os.makedirs(out_assets_filepath, exist_ok=True)
        except PermissionError as ex:
            raise PermissionException(str(ex)) from ex

        content, assets = extract_assets_from_html(content, assets_dir, url_handler)
        save_assets(assets, out_dir)

        if len(assets) == 0:
            from shutil import rmtree
            rmtree(out_assets_filepath)

    out_filepath = os.path.join(out_dir, url_filepath)
    write_file(out_filepath, content)
    return out_filepath
