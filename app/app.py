from datetime import datetime
import json

from bottle import Bottle, view, static_file

from app_data import HOMEPAGE_MENU
from app_paths import STATIC_PATH
from db_functions import get_meter_data
from decorators import api_route

application = Bottle()


@application.route('/')
@view('menu')
def home():
    title = 'Home'
    return {'title': title, 'items': HOMEPAGE_MENU}


@application.route('/home_icon')
def home_icon():
    return static_file(filename='home64.png', root=STATIC_PATH)


@application.route('/style')
def style():
    return static_file(filename='base.css', root=STATIC_PATH)


@application.route('/<name>/roste')
@view('meter')
def meter(name):

    def format_item(item):
        date, height = item['date'], item['height']
        parsed_date = datetime.strptime(date, '%Y-%m-%d')
        return {'date': f'{parsed_date:%-d. %-m. %Y}',
                'height': f'{height / 10:.1f} cm'}

    name = name.title()
    title = f'{name} roste'
    meter_data = sorted(get_meter_data(name), key=lambda entry: entry['date'])
    data = [format_item(item) for item in meter_data]
    return {'title': title, 'data': data}


@application.route('/api')
@api_route
def api_base_url():
    data = {
        'description': 'Base URL of the API',
        'available endpoints': ['meter'],
    }
    return json.dumps(data)


@application.route('/api/meter')
@api_route
def api_meter():
    data = {
        'description': 'Measurement data',
        'available endpoints': ['oli', 'fanda'],
    }
    return json.dumps(data)


@application.route('/api/meter/<name>')
@api_route
def api_meter_by_name(name):
    name = name.title()
    data = sorted(get_meter_data(name), key=lambda entry: entry['date'])
    return json.dumps(data)
