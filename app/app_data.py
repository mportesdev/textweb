from .db_functions import entries_exist


HOMEPAGE_MENU = [
    {
        'url': '/oli/roste',
        'text': 'Oli roste',
        'display': entries_exist('Meter', 'Oli'),
    },
    {
        'url': '/fanda/roste',
        'text': 'Fanda roste',
        'display': entries_exist('Meter', 'Fanda'),
    },
]
