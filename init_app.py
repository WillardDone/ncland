# -*- coding: utf-8 -*-
"""
    init_app.py
    ~~~~~~~~~~~

    Application configuration

    :copyright: (c) 2010 by Dan Jacob.
    :license: BSD, see LICENSE for more details.
"""

import time
import base64
import datetime

from datetime import date

from flask import Flask, g, session, request, flash, \
    redirect, jsonify, url_for, render_template
from urls import URLS
from extensions import db, cache, mail
from flask.ext.principal import Principal, RoleNeed, \
    UserNeed, identity_loaded

from sqlalchemy import Date, cast, and_
from config import DefaultConfig,LocalConfig
from models.model import Member
from filters import configure_template_filters

__all__ = ["create_app"]


def create_app(config=None):

    app = Flask(__name__)

    if not config:
        config = LocalConfig
    else:
        config = 'config.' + config

    # print '**'*40,config

    app.config.from_object(config)


    configure_blueprints(app)

    configure_extensions(app)

    configure_identity(app)
    
    configure_errorhandlers(app)
    
    configure_before_handlers(app)

    configure_context_processors(app)

    configure_template_filters(app)
    
    return app

def configure_blueprints(app):
    """配置蓝图"""

    for blueprints, url_prefix in URLS:
        # print blueprints
        app.register_blueprint(blueprints, url_prefix=url_prefix)


def configure_extensions(app):
    """配置拓展程序，数据库db、缓存cache、邮件mail"""
    # configure extensions         
    db.init_app(app)
    cache.init_app(app)
    mail.init_app(app)


def configure_identity(app):
    """配置身份认证信息"""

    principal = Principal(app)

    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        g.member = Member.query.from_identity(identity)


def configure_context_processors(app):
    """配置全局函数，上下文环境"""

    @app.context_processor
    def current_time():
        return dict(current_time=time.time())
    @app.context_processor
    def _7days_before():

        now_date = datetime.date.today()
        _7days_before = now_date + datetime.timedelta(days = -6)
        return dict(_7days_before=_7days_before)



def configure_before_handlers(app):
    """配置预处理操作，请求前、请求后..."""

    @app.before_request
    def authenticate():

        g.member = getattr(g.identity, 'member', None)


def configure_errorhandlers(app):
    """配置错误处理机制，401、402、403..."""
    @app.errorhandler(401)
    def unauthorized(error):
        if request.is_xhr:
            return jsonify(error="Login required")
        return redirect(url_for("index.login",next=request.path))
  
    @app.errorhandler(403)
    def forbidden(error):
        if request.is_xhr:
            return jsonify(error='Sorry, page not allowed')
        return render_template("errors/403.html", error=error)

    @app.errorhandler(404)
    def page_not_found(error):
        if request.is_xhr:
            return jsonify(error='Sorry, page not found')
        return render_template("errors/404.html", error=error)

    @app.errorhandler(500)
    def server_error(error):
        if request.is_xhr:
            return jsonify(error='Sorry, an error has occurred')
        return render_template("errors/500.html", error=error)





