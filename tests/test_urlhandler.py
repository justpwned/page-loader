from page_loader.urlhandler import UrlHandler

TEST_URL = 'https://example.com/hello/there'


def test_geturl():
    handler = UrlHandler(TEST_URL)
    no_scheme_test_url = 'example.com/hello/there'
    assert handler.get_url() == TEST_URL
    assert handler.get_url(strip_scheme=True) == no_scheme_test_url


def test_to_filepath_():
    handler = UrlHandler(TEST_URL)
    assert handler.to_filepath() == 'example-com-hello-there.html'
    assert handler.to_filepath(mimetype='image/jpeg') == 'example-com-hello-there.jpg'
