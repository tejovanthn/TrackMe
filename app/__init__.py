#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_appconfig import AppConfig
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.cache import Cache

app = Flask(__name__)

AppConfig(app, configfile='config.py')

Bootstrap(app)

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

db = SQLAlchemy(app)

from momentjs import momentjs
app.jinja_env.globals['momentjs'] = momentjs

from app import views, models

