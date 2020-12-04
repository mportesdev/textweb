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

METER_DATA = {
    'oli': [
        {
            'date': '20170528',
            'value': 789.5
        },
        {
            'date': '20171013',
            'value': 842
        },
        {
            'date': '20180103',
            'value': 871.5
        },
        {
            'date': '20180413',
            'value': 902.5
        },
        {
            'date': '20180719',
            'value': 928
        },
        {
            'date': '20181013',
            'value': 946.5
        },
        {
            'date': '20190114',
            'value': 960.5
        },
        {
            'date': '20190507',
            'value': 1011.5
        },
        {
            'date': '20190826',
            'value': 1032.5
        },
        {
            'date': '20200202',
            'value': 1052.5
        },
        {
            'date': '20200630',
            'value': 1090
        },
        {
            'date': '20200829',
            'value': 1108.5
        },
        {
            'date': '20201028',
            'value': 1121
        },
    ],

    'fanda': [
        {
            'date': '20200630',
            'value': 827
        },
        {
            'date': '20200829',
            'value': 840
        },
        {
            'date': '20201028',
            'value': 852
        },
    ]
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
        'display': entries_exist('meter', 'oli'),
    },
    {
        'url': '/fanda/roste',
        'text': 'Fanda roste',
        'display': entries_exist('meter', 'fanda'),
    },
]
