#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
if os.path.exists('.env'):
    print('Importing environment from .env...')
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]

from app import create_app
from flask_script import Manager
from app import db
#from app.users.models import User
#from datetime import datetime

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)


@manager.command
def test():
    from subprocess import call
    call(['nosetests', '-v',
          '--with-coverage', '--cover-package=app', '--cover-branches',
          '--cover-erase', '--cover-html', '--cover-html-dir=cover'])


@manager.command
def db_reset():
    '''Drop all & create all.ó'''
    db.drop_all()
    db.create_all()


if __name__ == '__main__':
    manager.run()

