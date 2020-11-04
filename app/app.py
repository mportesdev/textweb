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


@route('/date')
def date():
    return f'''
        <h1>
            {datetime.now().strftime("%x")}
        </h1>
    '''


@route('/time')
def time():
    return f'''
        <h1>
            {datetime.now().strftime("%X")}
        </h1>
    '''


@route('/date_time')
def date_time():
    return f'''
        <h1>
            {datetime.now().strftime("%c")}
        </h1>
    '''


application = default_app()
