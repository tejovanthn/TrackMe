#!venv/bin/python
# -*- coding: utf-8 -*-

from flask.ext.script import Manager, Shell, Server
from app import app

manager = Manager(app)
manager.add_command('runserver', Server())
manager.add_command('shell', Shell())
manager.run()
