from datetime import datetime

from bottle import Bottle, view, static_file

application = Bottle()


@application.route('/')
@view('menu')
def home():
    title = 'Home'
    items = [
        {'url': '/date', 'text': 'date'},
        {'url': '/time', 'text': 'time'},
        {'url': '/date_time', 'text': 'date & time'},
        {'url': '/oli/obrazky', 'text': 'Oli maluje'},
    ]
    return {'title': title, 'items': items}


@application.route('/<name:re:date|time|date_time>')
@view('simple')
def date_time(name):
    title = name.replace('_', ' & ').title()
    format_spec = {
        'date': '%-d. %-m. %Y',
        'time': '%-H:%M:%S',
        'date_time': '%-d. %-m. %Y, %-H:%M:%S',
    }.get(name)
    text = datetime.now().strftime(format_spec)
    return {'title': title, 'text': text}


@application.route('/oli/obrazky')
@view('gallery')
def oli_gallery():
    title = 'Oli maluje'
    pictures = [0, 1, 2]
    return {'title': title, 'pictures': pictures}


@application.route('/oli/obrazky/<picture_id:int>')
def oli_picture(picture_id):
    filename = {
        0: 'green.png',
        1: 'orange.png',
        2: 'blue.png',
    }.get(picture_id, '')
    return static_file(filename=filename, root='static')
