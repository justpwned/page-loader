import requests
import os
import bs4
from page_loader.urlhandler import UrlHandler
import logging
from itertools import chain
from progress.bar import Bar


def write_file(filepath, content):
    with open(filepath, 'wb') as fd:
        if isinstance(content, str):
            content = content.encode()
        fd.write(content)


def download_asset(url):
    if isinstance(url, UrlHandler):
        url = url.get_url()
    logging.info(f'Downloading "{url}"')
    response = requests.get(url)
    response.raise_for_status()
    mimetype = response.headers.get('content-type', '').split(';')[0]
    return response.content, mimetype


def save_assets(assets, asset_dir):
    for path, content in assets:
        filepath = os.path.join(asset_dir, path)
        write_file(filepath, content)


TAGS_LINK_ATTR = {
    'img': 'src',
    'script': 'src',
    'link': 'href'
}


def extract_assets_from_html(html, assets_dir, base_urlhandler):
    soup = bs4.BeautifulSoup(html, 'html.parser')

    assets = []
    tags = [tag for tag_name in TAGS_LINK_ATTR for tag in chain(soup(tag_name))]
    bar = Bar('Extracting assets: ', max=len(tags))
    for tag in tags:
        attr = TAGS_LINK_ATTR[tag.name]
        orig_src = tag.get(attr)
        if not orig_src:
            continue

        logging.info(f'Extracting <{tag.name} {attr}={orig_src}>')

        orig_src_handler = UrlHandler(orig_src)

        # Uncomment next line when done
        if orig_src_handler.is_local(base_urlhandler):
            asset_url = base_urlhandler.join(orig_src)
            content, mimetype = download_asset(asset_url)

            new_asset_name = base_urlhandler.join(orig_src_handler).to_filepath(mimetype)
            new_src = os.path.join(assets_dir, new_asset_name)

            tag[attr] = new_src
            assets.append((new_src, content))
        bar.next()
    bar.finish()

    return soup.prettify(), assets


def download(url, out_dir):
    content, mimetype = download_asset(url)

    url_handler = UrlHandler(url)
    url_filepath = url_handler.to_filepath(mimetype)

    if url_filepath.endswith('.html'):
        logging.info(f'Start extracting assets from "{url}"...')
        assets_dir = f'{os.path.splitext(url_filepath)[0]}_files'
        content, assets = extract_assets_from_html(content, assets_dir, url_handler)

        if len(assets) > 0:
            out_assets_filepath = os.path.join(out_dir, assets_dir)
            if not os.path.exists(out_assets_filepath):
                os.mkdir(out_assets_filepath)
            save_assets(assets, out_dir)

    out_filepath = os.path.join(out_dir, url_filepath)
    write_file(out_filepath, content)
    return out_filepath
