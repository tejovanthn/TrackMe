#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import render_template
from app import app

from endomondo import MobileApi as Endomondo


@app.route('/')
@app.route('/index')
def index():
    goal = {'Running': {
        'current': 2.5,
        'MIN': 0,
        'MAX': 1000,
        'percent': 2.5 * 100 / 1000,
        }, 'Cycling': {
        'current': 0,
        'MIN': 0,
        'MAX': 1000,
        'percent': 0 * 100 / 1000,
        }}

    print [w.distance for w in get_endomondo_workouts(since_id=int(app.config['ENDOMONDO_START']))]


    return render_template('index.html', goal=goal)


def get_endomondo():
    endomondo = Endomondo(email=app.config['ENDOMONDO_EMAIL'],
                          password=app.config['ENDOMONDO_PWORD'])
    auth_token = endomondo.get_auth_token()
    endomondo = Endomondo(auth_token=auth_token)

    return endomondo


def get_endomondo_workouts(since_id=None):
    endomondo = get_endomondo()

    workouts = endomondo.get_workouts()
    print since_id

    if isinstance(since_id, int):
        return [w for w in workouts if w.id >= since_id]
    else:
        return workouts


