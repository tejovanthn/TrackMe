#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_appconfig import AppConfig
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.cache import Cache

app = Flask(__name__)

AppConfig(app, configfile="config.py")

Bootstrap(app)

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

db = SQLAlchemy(app)

from app import views, models

