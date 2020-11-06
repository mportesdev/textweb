from datetime import datetime

from bottle import Bottle, request, template

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
def date_time(name):
    format_spec = {
        'date': '%-d. %-m. %Y',
        'time': '%-H:%M:%S',
        'date_time': '%-d. %-m. %Y, %-H:%M:%S',
    }.get(name)
    text = datetime.now().strftime(format_spec)
    return template('simple', text=text)


@application.route('/ip')
def ip():
    text = request.get('REMOTE_ADDR')
    return f'<h1>{text}</h1>' \
           f'<a href="/">home</a>'
