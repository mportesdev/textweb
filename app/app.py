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
    ]
    return {'title': title, 'items': items}


@application.route('/oli/maluje')
@view('gallery')
def oli_gallery():
    title = 'Oli maluje'
    pictures = [0, 1, 2]
    return {'title': title, 'pictures': pictures}


@application.route('/oli/maluje/<picture_id:int>')
def oli_picture(picture_id):
    filename = {
        0: 'green.png',
        1: 'orange.png',
        2: 'blue.png',
    }.get(picture_id, '')
    return static_file(filename=filename, root='static')


@application.route('/oli/roste')
@view('meter')
def oli_meter():
    title = 'Oli roste'
    data = [
        {'date': item['date'], 'value': item['value']}
        for item in app_data.OLI_METER_DATA
    ]
    return {'title': title, 'data': data}
