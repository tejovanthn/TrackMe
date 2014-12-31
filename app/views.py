#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import render_template
from app import app


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

    return render_template('index.html', goal=goal)
