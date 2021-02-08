from bottle import response


def api_route(func):
    """Decorator to set the Content-Type header."""

    def wrapper(*args, **kwargs):
        response.set_header('Content-Type', 'application/json; charset=utf-8')
        return func(*args, **kwargs)

    return wrapper
