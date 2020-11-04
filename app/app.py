from datetime import datetime

from bottle import route, default_app


@route('/')
def home():
    return '''
        <p>
            <a href="date">date</a>
        </p>
        <p>
            <a href="time">time</a>
        </p>
        <p>
            <a href="date_time">date & time</a>
        </p>
    '''


@route('/<name:re:date|time|date_time>')
def date_time(name):
    format_spec = {
        'date': '%x',
        'time': '%X',
        'date_time': '%c',
    }.get(name)
    text = datetime.now().strftime(format_spec)
    return f'<h1>{text}</h1>'


application = default_app()
