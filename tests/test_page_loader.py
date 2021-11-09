from page_loader import download
from urllib.parse import urljoin
import os.path

PAGE_URL = 'https://example.com'
HTML_FILENAME = 'example-com.html'
ASSETS_DIR_NAME = 'example-com_files'

ASSETS = [
    {
        'url_path': '/assets/test_image.jpg',
        'filename': 'example-com-assets-test-image.jpg',
    },
]


def read(filepath, mode='r'):
    return open(filepath, mode).read()


def get_fixture_path(filepath):
    dirname = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(dirname, 'fixtures', filepath)


def get_fixture_data(filename, mode='r'):
    return read(get_fixture_path(filename), mode)


def test_download(tmpdir, requests_mock):
    content = get_fixture_data(HTML_FILENAME)
    requests_mock.get(PAGE_URL, text=content)

    expected_html_filepath = get_fixture_path(os.path.join('expected', HTML_FILENAME))
    expected_html_content = read(expected_html_filepath)

    for asset in ASSETS:
        asset_url = urljoin(PAGE_URL, asset['url_path'])
        expected_asset_path = get_fixture_path(os.path.join('expected', ASSETS_DIR_NAME, asset['filename']))
        expected_asset_content = read(expected_asset_path, 'rb')
        asset['content'] = expected_asset_content
        requests_mock.get(asset_url, content=expected_asset_content)

    assert not os.listdir(tmpdir)

    output_filepath = download(PAGE_URL, tmpdir)
    assert len(os.listdir(tmpdir)) == 2

    tmp_assets_dir_name = os.path.join(tmpdir, ASSETS_DIR_NAME)
    tmp_assets_listdir = os.listdir(tmp_assets_dir_name)
    assert len(tmp_assets_listdir) == len(ASSETS)

    assert read(output_filepath) == expected_html_content

    for asset in ASSETS:
        assert asset['filename'] in tmp_assets_listdir
        asset_filepath = os.path.join(tmp_assets_dir_name, asset['filename'])
        assert asset['content'] == read(asset_filepath, 'rb')