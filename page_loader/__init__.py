import requests
import os.path
import re

MIME_EXT = {
    'text/html': '.html'
}


def generate_file_path(url, out_dir, ext):
    out_dir_full_path = os.path.abspath(out_dir)
    scheme, url = url.split('://')
    new_url = re.sub(r'[^0-9a-zA-Z]', '-', url)
    return os.path.join(out_dir_full_path, new_url + ext)


def get_mime_ext(content_type):
    content_type = content_type.split(';')[0]
    return MIME_EXT[content_type]


def download(url, out_dir):
    res = requests.get(url)
    res.raise_for_status()

    file_ext = get_mime_ext(res.headers['content-type'])
    out_filepath = generate_file_path(url, out_dir, file_ext)

    with open(out_filepath, 'wb') as fd:
        fd.write(res.content)

    return out_filepath
