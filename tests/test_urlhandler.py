from page_loader.urlhandler import UrlHandler

test_url = 'https://example.com/hello/there'


def test_geturl():
    handler = UrlHandler(test_url)
    no_scheme_test_url = 'example.com/hello/there'
    assert handler.get_url() == test_url
    assert handler.get_url(strip_scheme=True) == no_scheme_test_url


def test_local():
    local_url = '/hello/there'
    handler = UrlHandler(test_url)
    local_handler = UrlHandler(local_url)
    assert handler.is_local is False
    assert local_handler.is_local is True


def test_to_filepath():
    handler = UrlHandler(test_url)
    assert handler.to_filepath(only_netloc=True) == 'example-com'
    assert handler.to_filepath() == 'example-com-hello-there'


def test_to_filepath_ext():
    ext_handler = UrlHandler('https://example.com/hello/there.jpeg')
    domen_handler = UrlHandler('https://example.com')
    test_url_handler = UrlHandler(test_url)
    assert ext_handler.to_filepath() == 'example-com-hello-there.jpeg'
    assert ext_handler.to_filepath('assets') == 'assets/example-com-hello-there.jpeg'
    assert test_url_handler.to_filepath(mimetype='text/html') == 'example-com-hello-there.html'

    assert domen_handler.to_filepath() == 'example-com'
    assert domen_handler.to_filepath(mimetype='text/html') == 'example-com.html'
