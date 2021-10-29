import json

from bottle import response


def api_route(func):
    """Decorator to JSON-serialize the function's result and set
    the Content-Type header.
    """
    def wrapper(*args, **kwargs):
        response.set_header('Content-Type', 'application/json; charset=utf-8')
        result = func(*args, **kwargs)
        return json.dumps(result)

    return wrapper
