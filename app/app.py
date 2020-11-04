# coding: utf-8

from datetime import datetime

import bottle


@bottle.route('/')
def home():
    return """
    <a href="date">date</a>
    <a href="time">time</a>
    """


@bottle.route('/date')
def date():
    return datetime.now().strftime('%x')


@bottle.route('/time')
def time():
    return datetime.now().strftime('%X')


@bottle.route('/date_time')
def date_time():
    return datetime.now().strftime('%c')


application = bottle.default_app()
