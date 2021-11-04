from page_loader import download
import os.path
import requests_mock


def get_fixture_path(filepath):
    dirname = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(dirname, 'fixtures', filepath)


@requests_mock.Mocker(kw='mock')
def test_download(tmpdir, **kwargs):
    url = 'https://example.com'
    expected_content = open(get_fixture_path('example-com.html')).read()
    kwargs['mock'].get(url, text=expected_content, headers={'content-type': 'text/html; charset=UTF-8'})

    out_filepath = download(url, tmpdir)
    assert out_filepath == os.path.join(tmpdir, 'example-com.html')
    assert open(out_filepath).read() == expected_content
