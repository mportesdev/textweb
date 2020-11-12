from datetime import datetime
from pathlib import Path

from bottle import Bottle, view, static_file, HTTPError
from PIL import Image

from app_data import HOMEPAGE_MENU, PICTURE_FILES, METER_DATA

STATIC_PATH = Path(__file__).resolve().parent / 'static'

application = Bottle()


@application.route('/')
@view('menu')
def home():
    title = 'Home'
    return {'title': title, 'items': HOMEPAGE_MENU}


@application.route('/home_icon')
def home_icon():
    return static_file(filename='home32.png', root=STATIC_PATH)


@application.route('/style')
def style():
    return static_file(filename='base.css', root=STATIC_PATH)


@application.route('/<name>/maluje')
@view('gallery')
def oli_gallery(name):
    title = f'{name.title()} maluje'
    pictures = range(len(PICTURE_FILES[name]))
    return {'title': title, 'pictures': pictures}


@application.route('/<name>/maluje/<picture_id:int>')
def oli_picture(name, picture_id):
    try:
        filename = PICTURE_FILES[name][picture_id]
    except (KeyError, IndexError):
        raise HTTPError(404, 'File does not exist.')

    return static_file(filename=filename, root=STATIC_PATH)


@application.route('/<name>/nahled/<picture_id:int>')
def oli_thumbnail(name, picture_id):
    try:
        filename = PICTURE_FILES[name][picture_id]
    except (KeyError, IndexError):
        raise HTTPError(404, 'File does not exist.')

    thumb_path = get_thumbnail(STATIC_PATH / filename)
    return static_file(filename=thumb_path.name, root=STATIC_PATH)


def get_thumbnail(pic_path, long_side=400):
    thumb_path = pic_path.with_name(pic_path.stem + '_thumb' + pic_path.suffix)

    if not thumb_path.exists():
        img = Image.open(pic_path)
        w = img.width
        h = img.height
        if w > h:
            thumb = img.resize((long_side, long_side * h // w))
        else:
            thumb = img.resize((long_side * w // h, long_side))
        thumb.save(thumb_path)

    return thumb_path


@application.route('/<name>/roste')
@view('meter')
def meter(name):

    def format_item(item):
        date, value = item['date'], item['value']
        date_str = datetime.strptime(date, '%Y%m%d').strftime('%-d. %-m. %Y')
        value_str = f'{value / 10:.1f} cm'
        return {'date': date_str, 'value': value_str}

    title = f'{name.title()} roste'
    data = [format_item(item) for item in METER_DATA[name]]
    return {'title': title, 'data': data}
