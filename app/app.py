from datetime import datetime

from bottle import Bottle, view, static_file

import app_data

application = Bottle()


@application.route('/')
@view('menu')
def home():
    title = 'Home'
    items = [
        {'url': '/oli/maluje', 'text': 'Oli maluje'},
        {'url': '/oli/roste', 'text': 'Oli roste'},
        {'url': '/fanda/roste', 'text': 'Fanda roste'},
    ]
    return {'title': title, 'items': items}


@application.route('/home_icon')
def home_icon():
    return static_file(filename='home32.png', root='static')


@application.route('/oli/maluje')
@view('gallery')
def oli_gallery():
    title = 'Oli maluje'
    pictures = [0, 1]
    return {'title': title, 'pictures': pictures}


@application.route('/oli/maluje/<picture_id:int>')
def oli_picture(picture_id):
    filename = {
        0: 'doubledecker.jpg',
        1: 'ducks.jpg',
    }.get(picture_id, '')
    return static_file(filename=filename, root='static')


@application.route('/<name>/roste')
@view('meter')
def meter(name):
    def format_item(item):
        date, value = item['date'], item['value']
        date_str = datetime.strptime(date, '%Y%m%d').strftime('%-d. %-m. %Y')
        value_str = f'{value / 10:.1f} cm'
        return {'date': date_str, 'value': value_str}

    title = 'Oli roste'
    data = [format_item(item) for item in app_data.METER_DATA[name]]
    return {'title': title, 'data': data}
