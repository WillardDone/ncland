# -*-coding: utf-8 -*-
import datetime
import os
import json
import simplejson
import xlwt
from datetime import date
from sqlalchemy import Date, cast, and_
from flask import request, Blueprint,render_template,\
    current_app,url_for,redirect,g,flash,session
from flask.ext.principal import identity_changed, \
  Identity, AnonymousIdentity
from permissions import auth,admin
from extensions import db

from models.model import Inquiry,Review
from utils.choices import TARGET_TYPE_CHOICES,COUNTY_CHOICES,\
        PROJECT_TYPE_CHOICES,INDUSTRY_TYPE_CHOICES,GROUND_USE_TYPE_CHOICES
from utils.pagination import Pagination 

examine = Blueprint('examine', __name__)

@examine.route('/first_examine_add',methods=['POST','GET'])
def first_examine_add():
    """添加初审信息"""   
    g.__setattr__('action','examine.first_examine_add')

    from forms import addFirstExaForm

    form = addFirstExaForm()

    if form.validate_on_submit():
        inquiry = Inquiry() 
        form.populate_obj(inquiry)

        db.session.add(inquiry)
        db.session.commit()
        return redirect(url_for('examine.firstexalist'))

    return render_template('/examine/addFirstExa.html',
        form=form)

@examine.route('/firstexalist',methods=['POST','GET'])
def firstexalist():
    """初审信息列表"""  
    g.__setattr__('action','examine.firstexalist')

    page = int(request.form.get('page',1))
    pagesize = int(request.form.get('page_size',10))

    action = request.form.get('action','')

    #查询条件
    _county = int(request.form.get('county',0))

    inquirylist = Inquiry.query

    if _county:
        inquirylist = inquirylist.filter_by(project_address1=_county)

    inquirylist = inquirylist.order_by('apply_time desc').all()


    for inquiry in inquirylist:
        inquiry.project_address2 = COUNTY_CHOICES.__getitem__(inquiry.project_address1-1)[1]\
                                    +'-'+inquiry.project_address2_time.strftime('%Y-%m-%d')
        inquiry.apply_time = inquiry.apply_time.strftime('%Y-%m-%d')
    if action == "export":
        return redirect(inquiry_excel_created(inquirylist))

    pagination = Pagination(inquirylist,page,pagesize)
    inquirylist = pagination.list()

    return render_template('/examine/inquirylist.html',
        inquirylist=inquirylist,
        countys=COUNTY_CHOICES,
        pagination=pagination,
        _county=str(_county),
        page=page,
        page_size=pagesize)


def inquiry_excel_created(_QuerySet, name=u"inquiry"):
    wbk = xlwt.Workbook()
    sheet = wbk.add_sheet('sheet 1')
    sheet.write(0,0, u'项目名称')
    sheet.write(0,1, u'申请单位')
    sheet.write(0,2, u'项目坐落')
    sheet.write(0,3, u'项目用地面积')
    sheet.write(0,4, u'新增建设用地面积')
    sheet.write(0,5, u'其中农用地[含：耕地]')
    sheet.write(0,6, u'未利用地')
    sheet.write(0,7, u'申请时间')
    sheet.write(0,8, u'省厅初审批复文号')
    sheet.write(0,9, u'省厅初审时间')
    sheet.write(0,10, u'审查意见')

    row_start_index = 0
    for item in _QuerySet:
        row_start_index += 1
        sheet.write(row_start_index,0, item.project_name)
        sheet.write(row_start_index,1, item.applicant)
        sheet.write(row_start_index,2, item.project_address2)
        sheet.write(row_start_index,3, str(item.project_area)+u"亩")
        sheet.write(row_start_index,4, str(item.increased_const_area)+u"亩")
        sheet.write(row_start_index,5, str(item.other_farmland)+u"亩")
        sheet.write(row_start_index,6, str(item.unused_area)+u"亩")
        sheet.write(row_start_index,7, item.apply_time)
        sheet.write(row_start_index,8, item.reply_num)
        sheet.write(row_start_index,9, item.inquiry_time)
        sheet.write(row_start_index,10, item.examine_suggestion)
    wbk.save(current_app.config['PROJECT_DIR']+'/static/xls/%s.xls'%name)
    return "/static/xls/%s.xls"%name


@examine.route('/pre_examine_add',methods=['POST','GET'])
def pre_examine_add():
    """添加预审信息"""   
    g.__setattr__('action','examine.pre_examine_add')

    from forms import addPreExaForm

    form = addPreExaForm()

    if form.validate_on_submit():
        review = Review() 
        form.populate_obj(review)

        db.session.add(review)
        db.session.commit()
        return redirect(url_for('examine.preexalist'))

    return render_template('/examine/addPreExa.html',
        form=form)

@examine.route('/preexalist',methods=['POST','GET'])
def preexalist():
    """预审信息"""   
    g.__setattr__('action','examine.preexalist')

    page = int(request.form.get('page',1))
    pagesize = int(request.form.get('page_size',10))

    action = request.form.get('action','')

    #查询条件
    _county = int(request.form.get('county',0))

    reviewlist = Review.query

    if _county:
        reviewlist = reviewlist.filter_by(project_address1=_county)

    reviewlist = reviewlist.order_by('apply_time desc').all()

    for review in reviewlist:
        review.project_address2 = COUNTY_CHOICES.__getitem__(review.project_address1-1)[1]\
                                    +'-'+review.project_address2
        review.examine_time = review.examine_time.strftime('%Y-%m-%d')
        review.apply_time = review.apply_time.strftime('%Y-%m-%d')
    if action == "export":
        return redirect(review_excel_created(reviewlist))

    pagination = Pagination(reviewlist,page,pagesize)
    reviewlist = pagination.list()

    return render_template('/examine/reviewlist.html',
        reviewlist=reviewlist,
        countys=COUNTY_CHOICES,
        pagination=pagination,
        page=page,
        page_size=pagesize,
        _county=str(_county))


def review_excel_created(_QuerySet, name=u"review"):
    wbk = xlwt.Workbook()
    sheet = wbk.add_sheet('sheet 1')
    sheet.write(0,0, u'项目名称')
    sheet.write(0,1, u'申请单位')
    sheet.write(0,2, u'项目坐落')
    sheet.write(0,3, u'项目用地面积')
    sheet.write(0,4, u'新增建设用地面积')
    sheet.write(0,5, u'其中农用地[含：耕地]')
    sheet.write(0,6, u'未利用地')
    sheet.write(0,7, u'申请时间')
    sheet.write(0,8, u'省厅审批复文号')
    sheet.write(0,9, u'省厅审时间')
    sheet.write(0,10, u'审查意见')

    row_start_index = 0
    for item in _QuerySet:
        row_start_index += 1
        sheet.write(row_start_index,0, item.project_name)
        sheet.write(row_start_index,1, item.applicant)
        sheet.write(row_start_index,2, item.project_address1)
        sheet.write(row_start_index,3, str(item.project_area)+u"亩")
        sheet.write(row_start_index,4, str(item.increased_const_area)+u"亩")
        sheet.write(row_start_index,5, str(item.other_farmland)+u"亩")
        sheet.write(row_start_index,6, str(item.unused_area)+u"亩")
        sheet.write(row_start_index,7, item.apply_time)
        sheet.write(row_start_index,8, item.reply_num)
        sheet.write(row_start_index,9, item.examine_time)
        sheet.write(row_start_index,10, item.examine_suggestion)
    wbk.save(current_app.config['PROJECT_DIR']+'/static/xls/%s.xls'%name)
    return "/static/xls/%s.xls"%name



