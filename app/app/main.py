import base64
from datetime import datetime
import json
import hashlib
import hmac

from bottle import Bottle, view, static_file, request

from .data import HOMEPAGE_MENU
from .db_functions import get_meter_data, insert_into_meter, get_person_names
from .decorators import api_route
from .paths import APP_PATH, STATIC_PATH

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
        'available endpoints': ['oli', 'fanda', 'add'],
    }
    return json.dumps(data)


@application.route('/api/meter/add', ['GET', 'POST'])
@api_route
def api_meter_add():
    if request.method == 'GET':
        body = {
            'description': 'Use this endpoint to add records via POST requests',
        }
        return json.dumps(body)

    if not token_ok(request.headers.get('token', '')):
        return 'Incorrect write access token'

    if not request.content_type.startswith('application/json'):
        return 'Content type must be application/json'

    data = request.json
    if not meter_record_valid(data):
        return 'Invalid data'

    try:
        insert_into_meter(data)
    except Exception as err:
        return f'Error writing to database: {err}'

    return 'Record saved to database'


def token_ok(token):
    token_digest = hashlib.sha256(token.encode()).digest()
    secret_digest = base64.b64decode((APP_PATH / '.digest').read_text())
    return hmac.compare_digest(token_digest, secret_digest)


def meter_record_valid(data):
    if not isinstance(data, dict) or data.keys() != {'name', 'date', 'height'}:
        return False

    if data['name'] not in list(get_person_names()):
        return False

    try:
        datetime.strptime(data['date'], '%Y-%m-%d')
    except ValueError:
        return False

    height = data['height']
    if not isinstance(height, (float, int)) or not 0 < height < 2500:
        return False

    return True


@application.route('/api/meter/<name>')
@api_route
def api_meter_by_name(name):
    name = name.title()
    data = sorted(get_meter_data(name), key=lambda entry: entry['date'])
    return json.dumps(data)
