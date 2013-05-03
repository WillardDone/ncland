# -*- coding: utf-8 -*-
"""
    manage.py
    ~~~~~~~~~

    Description of the module goes here...

    :copyright: (c) 2013 by Dwn.
    :license: MacOS, see LICENSE for more details.
    :runDemo: python manage.py runserver -c DefaultConfig
"""
from flask import current_app

from flaskext.script import Manager,Server, prompt, prompt_pass, \
    prompt_bool, prompt_choices

from init_app import create_app
from extensions import db


manager = Manager(create_app)

manager.add_command("runserver", Server('0.0.0.0',port=8010))


@manager.command
def createall():
    "Creates database tables"

    db.create_all()


manager.add_option('-c', '--config',
                   dest="config",
                   required=False,
                   help="config file")


if __name__ == "__main__":
    # manager.run({'runserver':Server('', port=9911)})
    manager.run()
