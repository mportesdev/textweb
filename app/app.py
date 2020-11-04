# coding: utf-8

from datetime import datetime

import bottle


@bottle.route('/')
def home():
    return """
    <a href="date">date</a>
    <a href="time">time</a>
    <a href="date_time">date & time</a>
    """


@bottle.route('/date')
def date():
    return f'<h1>{datetime.now().strftime("%x")}</h1>'


@bottle.route('/time')
def time():
    return f'<h1>{datetime.now().strftime("%X")}</h1>'


@bottle.route('/date_time')
def date_time():
    return f'<h1>{datetime.now().strftime("%c")}</h1>'


application = bottle.default_app()
