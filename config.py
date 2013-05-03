# -*- coding: utf-8 -*-
"""
    config.py
    ~~~~~~~~~~~

    Default configuration

    :copyright: (c) 2013 by DWN.
    :license: MacOS, see LICENSE for more details.
"""


class DefaultConfig(object):
    """
    Default configuration for a jx6admin application.
    """

    DEBUG = True
    SQLALCHEMY_ECHO = False
    CSRF_ENABLED = False

    SQLALCHEMY_DATABASE_URI = 'postgresql://jx6:jx#t3n@61.147.97.248:54321/jx6analysis'

    SECRET_KEY = 't(5hxsl0t*(^7v9dftc)k47cp0*miuic=4kw^1bm(iey#*z2-h'

    MAIL_SERVER = '61.147.97.226'
    MAIL_USERNAME = 'kf@xq5.com'
    DEFAULT_MAIL_SENDER = 'kf@xq5.com'


    CACHE_TYPE = "memcached"
    CACHE_KEY_PREFIX = "jx6"
    CACHE_DEFAULT_TIMEOUT = 300

    DEBUG_LOG = '/tmp/nc_landlogs/debug.log'
    ERROR_LOG = '/tmp/nc_landlogs/error.log'


    # SESSION_LO_COOKIE_NAME = '_jx6_t'
    # SESSION_AUTOLOGIN_COOKIE_NAME = '_jx6_u'
    # SESSION_COOKIE_AGE = 365*24*60*60
    # SESSION_COOKIE_DOMAIN = '.jx6.com'

class LocalConfig(object):

    DEBUG = True
    SQLALCHEMY_ECHO = False
    CSRF_ENABLED = False

    SQLALCHEMY_DATABASE_URI = 'postgresql://dwn:123456@127.0.0.1:5432/ncland'
    SECRET_KEY = 't(5hxsl0t*(^7v9dftc)k47cp0*miuic=4kw^1bm(iey#*z2-h'

    CACHE_TYPE = "memcached"
    CACHE_KEY_PREFIX = "jx6"
    CACHE_DEFAULT_TIMEOUT = 300

    DEBUG_LOG = '/tmp/nc_landlogs/debug.log'
    ERROR_LOG = '/tmp/nc_landlogs/error.log'

    PROJECT_DIR = '/home/workspace/ncland/'

    # SESSION_LO_COOKIE_NAME = '_jx6_t'
    # SESSION_AUTOLOGIN_COOKIE_NAME = '_jx6_u'
    # SESSION_COOKIE_AGE = 365*24*60*60
    # SESSION_COOKIE_DOMAIN = '.jx6.com'


    # MAIL_SERVER = '61.147.97.226'
    # MAIL_USERNAME = 'kf@xq5.com'
    # DEFAULT_MAIL_SENDER = 'kf@xq5.com'


 








