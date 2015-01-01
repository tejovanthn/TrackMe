#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import render_template
from app import app, cache

from endomondo import MobileApi as Endomondo


@app.route('/')
@app.route('/index')
def index():
    goal = {'Running': {'MIN': 0, 'MAX': 1000}, 'Cycling': {'MIN': 0,
            'MAX': 1000}}

    # TODO Update from local database?

    workouts = \
        get_endomondo_workouts(since_id=int(app.config['ENDOMONDO_START'
                               ]))
    goal['Running']['current'] = sum([w.distance for w in workouts
            if w.sport == 0])
    goal['Cycling']['current'] = sum([w.distance for w in workouts
            if w.sport == 1 or w.sport == 2])

    goal['Running']['percent'] = goal['Running']['current'] * 100.0 \
        / goal['Running']['MAX']
    goal['Cycling']['percent'] = goal['Cycling']['current'] * 100.0 \
        / goal['Cycling']['MAX']

    notes = [{"id":w.id, "starttime":w.start_time, "note":w.notes} for w in workouts]

    return render_template('index.html', goal=goal, notes=notes)


def get_endomondo():
    endomondo = Endomondo(email=app.config['ENDOMONDO_EMAIL'],
                          password=app.config['ENDOMONDO_PWORD'])
    auth_token = endomondo.get_auth_token()
    endomondo = Endomondo(auth_token=auth_token)

    return endomondo


def get_endomondo_workouts(since_id=None):
    endomondo = get_endomondo()

    workouts = endomondo.get_workouts()

    if isinstance(since_id, int):
        return [w for w in workouts if w.id >= since_id]

    return workouts


