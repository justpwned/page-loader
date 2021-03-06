import pytest
import page_loader
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
    {
        'url_path': 'https://images.unsplash.com/photo-1636453966235-a5e76101975c',
        'filename': 'images-unsplash-com-photo-1636453966235-a5e76101975c.jpg',
        'mimetype': 'image/jpeg'
    },
    {
        'url_path': '/assets/styles.css',
        'filename': 'example-com-assets-styles.css'
    },
    {
        'url_path': 'https://js.stripe.com/v3/',
        'filename': 'js-stripe-com-v3-.js',
        'mimetype': 'application/javascript'
    }
]


def mock_format_html(html):
    return html.prettify()


page_loader.loader.format_html = mock_format_html


def read(filepath, mode='r'):
    return open(filepath, mode).read()


def get_fixture_path(filepath):
    test_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(test_dir, 'fixtures', filepath)


def get_fixture_data(filename, mode='r'):
    return read(get_fixture_path(filename), mode)


@pytest.fixture(autouse=True)
def prepare_mock_assets(requests_mock):
    for asset in ASSETS:
        asset_url = urljoin(PAGE_URL, asset['url_path'])
        expected_asset_path = get_fixture_path(os.path.join('expected', ASSETS_DIR_NAME, asset['filename']))
        expected_asset_content = read(expected_asset_path, 'rb')
        asset['content'] = expected_asset_content
        requests_mock.get(asset_url, content=expected_asset_content,
                          headers={'content-type': asset.get('mimetype', '')})


def test_download(requests_mock, tmpdir):
    content = get_fixture_data(HTML_FILENAME)
    requests_mock.get(PAGE_URL, text=content)

    expected_html_filepath = get_fixture_path(os.path.join('expected', HTML_FILENAME))
    expected_html_content = read(expected_html_filepath)

    assert not os.listdir(tmpdir)

    output_filepath = page_loader.download(PAGE_URL, tmpdir)
    assert len(os.listdir(tmpdir)) == 2

    tmp_assets_dir_name = os.path.join(tmpdir, ASSETS_DIR_NAME)
    tmp_assets_listdir = os.listdir(tmp_assets_dir_name)
    assert len(tmp_assets_listdir) == len(ASSETS)

    assert read(output_filepath) == expected_html_content

    for asset in ASSETS:
        assert asset['filename'] in tmp_assets_listdir
        asset_filepath = os.path.join(tmp_assets_dir_name, asset['filename'])
        assert asset['content'] == read(asset_filepath, 'rb')


def test_request_error(requests_mock, tmpdir):
    requests_mock.get(PAGE_URL, status_code=404)
    with pytest.raises(page_loader.exceptions.RequestException):
        _ = page_loader.download(PAGE_URL, tmpdir)
