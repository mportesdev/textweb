from datetime import datetime

from bottle import Bottle, view, static_file, HTTPError
from PIL import Image

from app_data import HOMEPAGE_MENU, PICTURE_FILES, METER_DATA
from app_paths import STATIC_PATH, IMG_PATH

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
        parsed_date = datetime.strptime(date, '%Y%m%d')
        return {'date': f'{parsed_date:%-d. %-m. %Y}',
                'value': f'{value / 10:.1f} cm'}

    title = f'{name.title()} roste'
    data = [format_item(item) for item in meter_data(name)]
    return {'title': title, 'data': data}


def meter_data(name):
    return METER_DATA[name]
