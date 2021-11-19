import base64
from datetime import datetime
import hashlib
import hmac
from http import HTTPStatus

from bottle import Bottle, view, static_file, request, TEMPLATE_PATH, HTTPError

from .data import HOMEPAGE_MENU
from .db_functions import get_meter_data, insert_into_meter, get_person_names
from .decorators import api_route
from .paths import APP_PATH, STATIC_PATH

application = Bottle()

TEMPLATE_PATH.append(APP_PATH / 'views')


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

    def date_key(entry):
        return datetime.strptime(entry['date'], '%Y-%m-%d')

    def format_item(item):
        date, height = item['date'], item['height']
        parsed_date = datetime.strptime(date, '%Y-%m-%d')
        return {'date': f'{parsed_date:%-d. %-m. %Y}',
                'height': f'{height / 10:.1f} cm'}

    name = name.title()
    title = f'{name} roste'
    meter_data = sorted(get_meter_data(name), key=date_key)
    data = [format_item(item) for item in meter_data]
    return {'title': title, 'data': data}


@application.route('/api')
@api_route
def api_base_url():
    body = {
        'description': 'Base URL of the API',
        'available endpoints': ['meter'],
    }
    return body


@application.route('/api/meter')
@api_route
def api_meter():
    body = {
        'description': 'Measurement data',
        'available endpoints': ['oli', 'fanda', 'add'],
    }
    return body


@application.route('/api/meter/add', ['GET', 'POST'])
@api_route
def api_meter_add():
    if request.method == 'GET':
        return {'description': 'Add records via POST requests'}

    if not token_ok(request.headers.get('token', '')):
        raise HTTPError(HTTPStatus.UNAUTHORIZED,
                        'Incorrect write access token')

    if not request.content_type.startswith('application/json'):
        raise HTTPError(HTTPStatus.BAD_REQUEST,
                        'Content type must be application/json')

    data = request.json
    if not meter_record_valid(data):
        raise HTTPError(HTTPStatus.BAD_REQUEST, 'Invalid data')

    try:
        insert_into_meter(data)
    except Exception as err:
        raise HTTPError(HTTPStatus.INTERNAL_SERVER_ERROR,
                        f'Error writing to database: {err}')

    return {'message': 'Record saved to database'}


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
    body = sorted(get_meter_data(name), key=lambda entry: entry['date'])
    return body
