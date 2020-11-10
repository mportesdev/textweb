from datetime import datetime

from bottle import Bottle, view, static_file

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
            <a href="/oli/obrazky">Oli maluje</a>
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


@application.route('/oli/obrazky')
@view('gallery')
def oli_gallery():
    pictures = [0, 1, 2]
    return {'pictures': pictures}


@application.route('/oli/obrazky/<picture_id:int>')
def oli_picture(picture_id):
    filename = {
        0: 'green.png',
        1: 'orange.png',
        2: 'blue.png',
    }.get(picture_id, '')
    return static_file(filename=filename, root='static')
