#!venv/bin/python
# -*- coding: utf-8 -*-

from flask.ext.script import Manager, Shell, Server
from app import app

from managers import database as db_manager
from managers import util as util_manager

manager = Manager(app)


manager.add_command('runserver', Server())
manager.add_command('shell', Shell())

manager.add_command('database', db_manager)
manager.add_command('util', util_manager)

manager.run()
