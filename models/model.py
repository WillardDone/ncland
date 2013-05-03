# -*- coding: utf-8 -*-
import datetime
import time
import os
from datetime import date
from extensions import db
from werkzeug import cached_property
from flask.ext.sqlalchemy import BaseQuery
from flask.ext.principal import RoleNeed,UserNeed
from sqlalchemy import Date, cast, and_


class MemberQuery(BaseQuery):

    def from_identity(self, identity):
        """
        Loads user from flaskext.principal.Identity instance and
        assigns permissions from user.

        A "user" instance is monkeypatched to the identity instance.

        If no user found then None is returned.
        """
        try:
            member = self.get(int(identity.name))
        except ValueError,e:
            member = None

        if member:
            identity.provides.update(member.provides)


        identity.member = member

        return member

    def authenticate(self, username, password):
        member = self.filter(
            db.or_(Member.username==username)).first()
        # print '<>'*80,dir(member)

        if member:
            authenticated = (member.password == password)
        else:
            authenticated = False

        return member, authenticated

    def create_user(self, **kwargs):

        for item in kwargs.keys():
            if item not in ('username', 'password',  'create_time'):
                kwargs.pop(item)
        m = Member(**kwargs)

        db.session.add(m)
        db.session.commit()

        return m

class Member(db.Model):
    """
       username:用户帐号,
       password:用户密码,
       create_time:注册时间,
    """
    
    __tablename__ = 'account_member'
    query_class = MemberQuery

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    is_root = db.Column(db.Boolean, default=False, nullable=False)

    create_time = db.Column(db.DateTime, default=datetime.datetime.now)
    
    def __init__(self, **arg):

        for k, v in arg.iteritems():
            setattr(self,k,v)

    def __unicode__(self):
        return u"%s" % self.username    

    def is_superuser(self):
        return self.is_root

    def set_password(self, raw_password):
        import random
        from utils.common import get_hexdigest
        algo = "md5"
        salt = get_hexdigest(algo, str(random.random()), str(random.random()))[:5]
        hsh = get_hexdigest(algo, salt, raw_password)
        self.password = "%s$%s$%s" % (algo, salt, hsh)
        
        return self.password

    @cached_property
    def provides(self):

        needs = [RoleNeed('authenticated'),
                 UserNeed(self.id)]

        return needs

class Batch(db.Model):
    """批次表
      year :年度,
      county:区县,
      batch_name:批次名称,
      plough_area:耕地面积,
      other_farmland:其他农用地,
      unused_area:未利用地,
      stock_const_area:存量建设用地面积,
      increased_const_area:涉及新增建设用地,
      total_area:总面积,
      target_type:指标类型,
      match_target_area:配套指标面积,
      match_target_type:配套指标类别,
      reply_num:批复文号,
      reply_time:批复时间,
      remark:备注,
    """
    def __init__(self, **arg):
        for k, v in arg.iteritems():
            setattr(self,k,v)

    __tablename__ = 'batch'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    year = db.Column(db.Integer, nullable=False, default=0)
    county = db.Column(db.Integer, nullable=False, default=0)
    batch_name = db.Column(db.String(40), nullable=False, default='')
    plough_area = db.Column(db.Float, nullable=False, default=0)
    other_farmland = db.Column(db.Float, nullable=False, default=0)
    unused_area = db.Column(db.Float, nullable=False, default=0)
    stock_const_area = db.Column(db.Float, nullable=False, default=0)
    increased_const_area = db.Column(db.Float, nullable=False, default=0)
    total_area = db.Column(db.Float, nullable=False, default=0)
    target_type = db.Column(db.Integer, nullable=False, default=0)
    match_target_area = db.Column(db.Float, nullable=False, default=0)
    match_target_type = db.Column(db.Integer, nullable=False, default=0)
    reply_num =  db.Column(db.String(30), nullable=False, default='')
    reply_time = db.Column(db.DateTime,nullable=False, default=datetime.datetime.today())
    remark =  db.Column(db.String(400), nullable=False, default='')

        
class Ground(db.Model):
    """地块表
      batch_name:批次名称,
      county:区县,
      project_type:项目类型,
      industry_type:产业类型,
      used_type:土地用途,
      ground_num:地块编号,
      project_name:项目名称,
      plough_area:耕地面积,
      other_farmland:其他农用地,
      unused_area:未利用地,
      stock_const_area:存量建设用地面积,
      increased_const_area:涉及新增建设用地,
      total_area:地块面积,
      target_area:指标面积,
      target_type:指标类型,
      match_area:配套面积,
      match_target_type:配套指标类别,
      target_according:安排指标依据,

      指标面积=耕地面积+其他农用地面积+未利用地面积
      地块面积=指标面积+建设用地面积
    """
    def __init__(self, **arg):
        for k, v in arg.iteritems():
            setattr(self,k,v)
    __tablename__ = 'ground'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    batch_name = db.Column(db.String(40), nullable=False, default='')
    county = db.Column(db.Integer, nullable=False, default=0)
    project_type = db.Column(db.Integer, nullable=False, default=0)
    industry_type = db.Column(db.Integer, nullable=False, default=0)
    used_type = db.Column(db.Integer, nullable=False, default=0)
    ground_num = db.Column(db.String(30), nullable=False, default='')
    project_name = db.Column(db.String(30), nullable=False, default='')
    plough_area = db.Column(db.Float, nullable=False, default=0)
    other_farmland = db.Column(db.Float, nullable=False, default=0)
    unused_area = db.Column(db.Float, nullable=False, default=0)
    stock_const_area = db.Column(db.Float, nullable=False, default=0)
    increased_const_area = db.Column(db.Float, nullable=False, default=0)
    total_area = db.Column(db.Float, nullable=False, default=0)
    target_area = db.Column(db.Float, nullable=False, default=0)
    target_type = db.Column(db.Integer, nullable=False, default=0)
    match_area = db.Column(db.Float, nullable=False, default=0)
    match_target_type = db.Column(db.String(20), nullable=False, default='')
    target_according =  db.Column(db.String(200), nullable=False, default='')




class Review(db.Model):
    """
       project_name:项目名称,
       project_address1:项目座落1,
       project_address2:项目座落2,
       project_area:项目用地面积,
       increased_const_area:其中新增建设用地面积,
       other_farmland:农用地面积,
       unused_area:未利用地面积,
       created_time:创建日期,
       applicant:申请单位,
       reply_num:初审批复文号,
       examine_time:审查时间,
       examine_suggestion:审查意见,
    """
    def __init__(self, **arg):

        for k, v in arg.iteritems():
            setattr(self,k,v)

    __tablename__ = 'review'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    project_name = db.Column(db.String(40), nullable=False, default='')
    project_address1 = db.Column(db.Integer, nullable=False, default=0)
    project_address2 = db.Column(db.String(40), nullable=False, default='')
    project_area = db.Column(db.Numeric, nullable=False, default=0)
    increased_const_area = db.Column(db.Numeric, nullable=False, default=0)
    other_farmland = db.Column(db.Numeric, nullable=False, default=0)
    unused_area = db.Column(db.Numeric, nullable=False, default=0)
    apply_time = db.Column(db.DateTime,nullable=False, default=datetime.datetime.today())
    examine_time = db.Column(db.DateTime,nullable=False, default=datetime.datetime.today())
    applicant =  db.Column(db.String(30), nullable=False, default='')
    reply_num =  db.Column(db.String(30), nullable=False, default='')
    examine_suggestion =  db.Column(db.String(400), nullable=False, default='')

class Inquiry(db.Model):
    """
        project_name:项目名称,
        project_address1:项目座落1,
        project_address2:项目座落2,
        project_area:项目用地面积,
        increased_const_area:其中新增建设用地面积,
        other_farmland:农用地面积,
        unused_area:未利用地面积,
        apply_time:申请日期,
        applicant:申请单位,
        reply_num:省厅预审批复文号,
        inquiry_time:省厅预审时间,
        examine_suggestion:审查意见,
    """
    def __init__(self, **arg):

        for k, v in arg.iteritems():
            setattr(self,k,v)

    __tablename__ = 'inquiry'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    applicant =  db.Column(db.String(30), nullable=False, default='')
    reply_num = db.Column(db.String(30), nullable=False, default='')
    inquiry_time = db.Column(db.DateTime,nullable=False, default=datetime.date.today())
    examine_suggestion =  db.Column(db.String(400), nullable=False, default='')
    project_address1 = db.Column(db.Integer, nullable=False, default=0)
    project_address2 = db.Column(db.String(40), nullable=False, default='')
    increased_const_area = db.Column(db.Numeric, nullable=False, default=0)
    other_farmland = db.Column(db.Numeric, nullable=False, default=0)
    unused_area = db.Column(db.Numeric, nullable=False, default=0)
    apply_time = db.Column(db.DateTime,nullable=False, default=datetime.date.today())
    project_name = db.Column(db.String(40), nullable=False, default='')
    project_area = db.Column(db.Numeric, nullable=False, default=0)
    