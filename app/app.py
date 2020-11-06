from datetime import datetime

from bottle import Bottle, request, view

application = Bottle()


@application.route('/')
def home():
    return '''
        <p>
            <a href="/date">date</a>
        </p>
        <p>
            <a href="/time">time</a>
        </p>
        <p>
            <a href="/date_time">date & time</a>
        </p>
        <p>
            <a href="/ip">IP address</a>
        </p>
    '''


@application.route('/<name:re:date|time|date_time>')
@view('simple')
def date_time(name):
    format_spec = {
        'date': '%-d. %-m. %Y',
        'time': '%-H:%M:%S',
        'date_time': '%-d. %-m. %Y, %-H:%M:%S',
    }.get(name)
    text = datetime.now().strftime(format_spec)
    return {'text': text}


@application.route('/ip')
@view('simple')
def ip():
    text = request.get('REMOTE_ADDR')
    return {'text': text}
