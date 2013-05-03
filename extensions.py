#!/usr/bin/env python
#coding=utf-8

from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.cache import Cache
from flask.ext.mail import Mail

__all__ = ['db', 'cache','mail']

db = SQLAlchemy()
cache = Cache()
mail = Mail()