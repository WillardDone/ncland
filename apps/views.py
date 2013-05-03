# -*-coding: utf-8 -*-
import datetime
from datetime import date

from flask import request, Blueprint,render_template,\
    current_app,url_for,redirect,g,flash,session
from flask.ext.principal import identity_changed, \
  Identity, AnonymousIdentity
from permissions import auth,admin
from extensions import db

from models.model import Member

index_r = Blueprint('index', __name__)

@index_r.route('/') 
@auth.require(401)
def index():

    return redirect(url_for('batch.index'))


@index_r.route('/login',methods=['POST','GET'])
def login():
    """login module"""
    from forms import LoginForm
    
    form = LoginForm()
    next_url = request.args.get('next')

    if form.validate_on_submit():

        member, authenticated = \
          Member.query.authenticate(
            form.username.data, 
            form.password.data)
        if member and authenticated:

            identity_changed.send(
              current_app._get_current_object(),
              identity=Identity(member.id))
            next_url = next_url if next_url \
                else url_for('index.index')
            return redirect(next_url)
        else:
            flash(u"用户名或密码错误.", "error")

    return render_template('login.html', form=form)

@index_r.route('/loginout')
def loginout():

    flash(u"退出登陆成功.", "success")
    identity_changed.send(
      current_app._get_current_object(),
      identity=AnonymousIdentity())

    next_url = request.args.get('next','')
    if not next_url or next_url == request.path:
        next_url = url_for("index.login")

    return redirect(next_url)


