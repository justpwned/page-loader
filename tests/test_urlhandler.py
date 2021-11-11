from page_loader.urlhandler import UrlHandler

TEST_URL = 'https://example.com/hello/there'


def test_geturl():
    handler = UrlHandler(TEST_URL)
    no_scheme_test_url = 'example.com/hello/there'
    assert handler.get_url() == TEST_URL
    assert handler.get_url(strip_scheme=True) == no_scheme_test_url


def test_is_local():
    handler1 = UrlHandler(TEST_URL)
    base_handler = UrlHandler('https://example.com')
    handler2 = UrlHandler('/hello/there')
    assert handler1.is_local(base_handler)
    assert handler2.is_local()


def test_to_filepath():
    handler = UrlHandler(TEST_URL)
    assert handler.to_filepath() == 'example-com-hello-there.html'
    assert handler.to_filepath(mimetype='image/jpeg') == 'example-com-hello-there.jpg'
