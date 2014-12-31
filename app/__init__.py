#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_appconfig import AppConfig
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)

AppConfig(app, configfile=None)

Bootstrap(app)

db = SQLAlchemy(app)

from app import views, models

