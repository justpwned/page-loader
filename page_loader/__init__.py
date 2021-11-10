import requests
import os
import bs4
import bs4.formatter
from page_loader.urlhandler import UrlHandler


def write_file(filepath, content):
    with open(filepath, 'wb') as fd:
        if isinstance(content, str):
            content = content.encode()
        fd.write(content)


def download_asset(url):
    if isinstance(url, UrlHandler):
        url = url.get_url()
    response = requests.get(url)
    response.raise_for_status()
    mimetype = response.headers.get('content-type', '').split(';')[0]
    return response.content, mimetype


def save_assets(assets, asset_dir):
    for path, content in assets:
        filepath = os.path.join(asset_dir, path)
        write_file(filepath, content)


def download_assets_from_html(html, assets_dir, base_urlhandler):
    soup = bs4.BeautifulSoup(html, 'html.parser')

    assets = []
    images = soup.find_all('img')
    for img in images:
        orig_src = img.get('src')
        if not orig_src:
            continue

        img_url = base_urlhandler.join(orig_src)
        img_content, img_mimetype = download_asset(img_url)

        orig_src_handler = UrlHandler(orig_src)
        new_asset_name = base_urlhandler.join(orig_src_handler).to_filepath(img_mimetype)
        new_src = os.path.join(assets_dir, new_asset_name)

        img['src'] = new_src
        assets.append((new_src, img_content))

    return soup.prettify(), assets


def download(url, out_dir):
    content, mimetype = download_asset(url)

    url_handler = UrlHandler(url)
    url_filepath = url_handler.to_filepath(mimetype)

    if url_filepath.endswith('.html'):
        assets_dir = f'{os.path.splitext(url_filepath)[0]}_files'
        content, assets = download_assets_from_html(content, assets_dir, url_handler)

        if len(assets) > 0:
            os.mkdir(os.path.join(out_dir, assets_dir))
            save_assets(assets, out_dir)

    out_filepath = os.path.join(out_dir, url_filepath)
    write_file(out_filepath, content)
    return out_filepath
