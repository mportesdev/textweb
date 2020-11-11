from datetime import datetime
from pathlib import Path

from bottle import Bottle, view, static_file
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


@application.route('/oli/maluje')
@view('gallery')
def oli_gallery():
    title = 'Oli maluje'
    pictures = [0, 1]
    return {'title': title, 'pictures': pictures}


@application.route('/oli/maluje/<picture_id:int>')
def oli_picture(picture_id):
    filename = PICTURE_FILES['oli'][picture_id]
    return static_file(filename=filename, root=STATIC_PATH)


@application.route('/oli/nahled/<picture_id:int>')
def oli_thumbnail(picture_id):
    filename = PICTURE_FILES['oli'][picture_id]
    thumb_path = get_thumbnail(STATIC_PATH / filename)
    return static_file(filename=thumb_path.name, root=STATIC_PATH)


def get_thumbnail(pic_path, thumb_width=400):
    thumb_path = pic_path.with_name(pic_path.stem + '_thumb' + pic_path.suffix)

    if not thumb_path.exists():
        img = Image.open(pic_path)
        thumb = img.resize((thumb_width, thumb_width * img.height // img.width))
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

    title = 'Oli roste'
    data = [format_item(item) for item in METER_DATA[name]]
    return {'title': title, 'data': data}
