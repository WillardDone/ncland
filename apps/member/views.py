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

member = Blueprint('member', __name__)

@member.route('/',methods=['POST','GET'])
def index():
    """新增用户"""
    g.__setattr__('action','member_manage')
    from forms import MemberForm
    form = MemberForm()

    if form.validate_on_submit():
        member = Member()

        form.populate_obj(member)
        db.session.add(member)
        db.session.commit()
        flash(u'添加成功！')

    members = Member.query.all()

    return render_template('/member/member.html',form=form,members=members)



@member.route('/<int:m_id>/delete',methods=['POST','GET'])
def delete(m_id=None):
    """删除用户"""
    if m_id:
        member = Member.query.filter_by(id=m_id).first()
        db.session.delete(member)
        db.session.commit()

        return redirect(url_for('member.index'))
    else:
        raise "Error"


