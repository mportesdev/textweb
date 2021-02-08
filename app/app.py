from datetime import datetime
import json

from bottle import Bottle, view, static_file, HTTPError
from PIL import Image

from app_data import HOMEPAGE_MENU, PICTURE_FILES
from app_paths import STATIC_PATH, IMG_PATH
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


@application.route('/<name>/maluje')
@view('gallery')
def gallery(name):
    title = f'{name.title()} maluje'
    picture_ids = range(len(PICTURE_FILES[name]))
    return {'title': title, 'name': name, 'pictures': picture_ids}


@application.route('/<name>/maluje/<picture_id:int>')
def picture(name, picture_id):
    try:
        filename = PICTURE_FILES[name][picture_id]
    except (KeyError, IndexError):
        raise HTTPError(404, 'File does not exist.')

    return static_file(filename=filename, root=IMG_PATH / name)


@application.route('/<name>/nahled/<picture_id:int>')
def thumbnail(name, picture_id):
    try:
        filename = PICTURE_FILES[name][picture_id]
    except (KeyError, IndexError):
        raise HTTPError(404, 'File does not exist.')

    thumb_path = get_thumbnail(IMG_PATH / name / filename)
    return static_file(filename=thumb_path.name, root=thumb_path.parent)


def get_thumbnail(pic_path, long_side=400):
    thumb_path = pic_path.with_name(pic_path.stem + '_thumb' + pic_path.suffix)

    if not thumb_path.exists():
        with Image.open(pic_path) as img:
            img.thumbnail((long_side, long_side))
            img.save(thumb_path)

    return thumb_path


@application.route('/<name>/roste')
@view('meter')
def meter(name):

    def format_item(item):
        date, height = item['date'], item['height']
        parsed_date = datetime.strptime(date, '%Y-%m-%d')
        return {'date': f'{parsed_date:%-d. %-m. %Y}',
                'height': f'{height / 10:.1f} cm'}

    title = f'{name.title()} roste'
    data = [format_item(item) for item in meter_data(name)]
    return {'title': title, 'data': data}


def meter_data(name):
    name = name.capitalize()
    return sorted(get_meter_data(name), key=lambda entry: entry['date'])


@application.route('/api/<name>/roste')
@api_route
def meter_api(name):
    serializable = [dict(row) for row in meter_data(name)]
    return json.dumps(serializable)
