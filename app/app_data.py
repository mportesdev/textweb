from app_paths import IMG_PATH
from db_functions import entries_exist


def jpg_pictures(author):
    return [
        path.name
        for path in (IMG_PATH / author).glob('*.jpg')
        if '_thumb' not in path.name
    ]


PICTURE_FILES = {
    author: jpg_pictures(author)
    for author in ('oli', 'fanda')
}

HOMEPAGE_MENU = [
    {
        'url': '/oli/maluje',
        'text': 'Oli maluje',
        'display': bool(PICTURE_FILES['oli']),
    },
    {
        'url': '/fanda/maluje',
        'text': 'Fanda maluje',
        'display': bool(PICTURE_FILES['fanda']),
    },
    {
        'url': '/oli/roste',
        'text': 'Oli roste',
        'display': entries_exist('meter', 'Oli'),
    },
    {
        'url': '/fanda/roste',
        'text': 'Fanda roste',
        'display': entries_exist('meter', 'Fanda'),
    },
]
