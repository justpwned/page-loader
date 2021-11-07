import pytest
import requests
import re
from page_loader import download
import os.path
import requests_mock


def get_fixture_path(filepath):
    dirname = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(dirname, 'fixtures', filepath)


def read_fixture_file(filename):
    return open(get_fixture_path(filename)).read()


def norm(string):
    return re.sub(r'[\s]', '', string).lower()


@requests_mock.Mocker(kw='mock')
def test_download(tmpdir, **kwargs):
    url = 'https://example.com'
    expected_filename = 'example-com.html'
    expected_content = read_fixture_file(expected_filename)
    kwargs['mock'].get(url, text=expected_content, headers={'content-type': 'text/html; charset=UTF-8'})

    out_filepath = download(url, tmpdir)
    assert out_filepath == os.path.join(tmpdir, expected_filename)
    assert norm(open(out_filepath).read()) == norm(expected_content)


@requests_mock.Mocker(kw='mock')
def test_download_404(tmpdir, **kwargs):
    url = 'https://example.com'
    kwargs['mock'].get(url, status_code=404)
    with pytest.raises(requests.HTTPError) as ex:
        out_filepath = download(url, tmpdir)


@requests_mock.Mocker(kw='mock')
def test_download_with_images(tmpdir, **kwargs):
    url = 'https://example.com/images'
    expected_filename = 'example-com-images.html'
    content = read_fixture_file(expected_filename)
    expected_content = read_fixture_file('example-com-images_expected.html')
    kwargs['mock'].get(url, text=content, headers={'content-type': 'text/html; charset=UTF-8'})
    kwargs['mock'].get('https://example.com/assets/test_image1.jpg', content=b'')
    kwargs['mock'].get('https://example.com/assets/test_image2.jpg', content=b'')
    kwargs['mock'].get('https://example.com/assets/test_image3.jpg', content=b'')

    out_filepath = download(url, tmpdir)
    assert out_filepath == os.path.join(tmpdir, expected_filename)
    assert norm(open(out_filepath).read()) == norm(expected_content)
