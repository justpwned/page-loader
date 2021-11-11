class PageLoaderException(Exception):
    pass


class RequestException(PageLoaderException):
    pass


class PermissionException(PageLoaderException):
    pass
