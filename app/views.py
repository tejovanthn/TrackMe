#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import render_template, jsonify
from app import app, cache

from endomondo import MobileApi as Endomondo

goal = {'Running': {'MIN': 0, 'MAX': 1000,  "sport_id": [0]},
        'Cycling': {'MIN': 0, 'MAX': 10000, "sport_id": [1,2]}}


@app.route('/')
@app.route('/index')
def index():

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

#    notes = [{'id': w.id, 'starttime': w.start_time, 'note': w.note}             for w in workouts]

    return render_template('index.html', goal=goal)  # , notes=notes)


@cache.cached(timeout=300, key_prefix='endomain')
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


@app.route("/_get_endomondo_cal/<int:sport_id>")
def get_endomondo_cal(since_id=int(app.config["ENDOMONDO_START"]), sport_id=0):
    workouts = get_endomondo_workouts(since_id)

    results = {w.start_time.strftime("%s") : w.distance \
            for w in workouts if w.sport == sport_id}

    return jsonify(response=results)


