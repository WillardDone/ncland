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

from models.model import Member,Batch,Ground
from utils.choices import TARGET_TYPE_CHOICES,COUNTY_CHOICES,\
        PROJECT_TYPE_CHOICES,INDUSTRY_TYPE_CHOICES,GROUND_USE_TYPE_CHOICES
from utils.pagination import Pagination 
from utils import match_target_type_resolution
ground = Blueprint('ground', __name__)

@ground.route('/',methods=['POST','GET'])
def index():
    """添加地块信息"""   
    g.__setattr__('action','ground.index')

    from forms import addGroundForm 
    form = addGroundForm()

    if form.validate_on_submit():
        ground = Ground()
        form.populate_obj(ground)
        match_target_type = ''
        for typa in request.form.getlist('match_target_type'):
            match_target_type += typa+"_"
        total_area = float(request.form.get('total_area',0))
        target_area = float(request.form.get('target_area',0))
        batch_name = request.form.get('batch_name',0)

        plough_area = float(request.form.get('plough_area',0))
        other_farmland = float(request.form.get('other_farmland',0))
        unused_area = float(request.form.get('unused_area',0))
        stock_const_area = float(request.form.get('stock_const_area',0))
        increased_const_area = float(request.form.get('increased_const_area',0))
        # total_area = float(request.form.get('total_area',0))
        batch_name = float(request.form.get('batch_name',0))

        print '<>'*30,total_area,target_area

        #将当前地块的各个面积值 加入到 针对该块地对应的批次的各个面积值上
        batch = Batch.query.filter_by(id=batch_name).first()
        setattr(batch,'plough_area',batch.plough_area+plough_area)         
        setattr(batch,'other_farmland',batch.other_farmland+other_farmland)         
        setattr(batch,'unused_area',batch.unused_area+unused_area)         
        setattr(batch,'stock_const_area',batch.stock_const_area+stock_const_area)         
        setattr(batch,'increased_const_area',batch.increased_const_area+increased_const_area)         
        setattr(batch,'total_area',batch.total_area+total_area)         

        #对不能通过form.populate_obj方法初始化的几个属性进行初始化
        setattr(ground,'match_target_type',match_target_type) 
        setattr(ground,'total_area',total_area) 
        setattr(ground,'target_area',target_area) 
        db.session.add(ground)
        db.session.commit()
        return redirect(url_for('ground.groundlist'))

    return render_template('/ground/ground.html',
        form=form,
        match_target_type=TARGET_TYPE_CHOICES)

@ground.route('/getBatch',methods=['POST','GET'])
def getBatch():

    batch_id = int(request.form.get('batch_id',0))
    batch = Batch.query.filter_by(id=batch_id).first()

    if batch :
        return simplejson.dumps(
                {"id":batch.id,
                 "county":batch.county,
                 "remark":batch.remark})
    else:
        return "Error"

@ground.route('/groundlist',methods=['POST','GET'])
def groundlist():
    """所有土地信息列表"""
    g.__setattr__('action','ground.groundlist')
    
    page = int(request.form.get('page',1))
    pagesize = int(request.form.get('page_size',10))
    action = request.form.get('action','')

    #查询条件
    batch_name = int(request.form.get('batch_name',0))
    county = int(request.form.get('county',0))
    project_type = int(request.form.get('project_type',0))
    industry_type = int(request.form.get('industry_type',0))
    used_type = int(request.form.get('used_type',0))

    ground_list = Ground.query

    if batch_name:
        ground_list = ground_list.filter_by(batch_name=batch_name)
    if county:
        ground_list = ground_list.filter_by(county=county)
    if project_type:
        ground_list = ground_list.filter_by(project_type=project_type)
    if industry_type:
        ground_list = ground_list.filter_by(industry_type=industry_type)
    if used_type:
        ground_list = ground_list.filter_by(used_type=used_type)

    ground_list = ground_list.order_by('id desc').all()
    
    # print Ground.query.filter(and_(filter_str)).order_by('id desc')

    for ground in ground_list:
        ground.match_target_type = match_target_type_resolution(ground.match_target_type)

    if action == "export":
        return redirect(ground_excel_created(ground_list)) 

    print '*'*40,pagesize,page
    pagination = Pagination(ground_list,page,pagesize)
    groundlist = pagination.list()

    return render_template('/ground/groundlist.html',
        pagination=pagination,
        page=page,
        page_size=pagesize,
        groundlist=groundlist,
        batchlist = Batch.query.all(),
        countys=COUNTY_CHOICES,
        project_types=PROJECT_TYPE_CHOICES,
        industry_types=INDUSTRY_TYPE_CHOICES,
        used_types=GROUND_USE_TYPE_CHOICES,
        _batch_name=batch_name,
        _county=str(county),
        _project_type=str(project_type),
        _industry_type=str(industry_type),
        _used_type=str(used_type)
        )    


def ground_excel_created(_QuerySet, name=u"ground"):
    wbk = xlwt.Workbook()
    sheet = wbk.add_sheet('sheet 1')
    sheet.write(0,0, u'序号(批次编号)')
    sheet.write(0,1, u'项目名称')
    sheet.write(0,2, u'项目类型')
    sheet.write(0,3, u'土地用途')
    sheet.write(0,4, u'地块编号')
    sheet.write(0,5, u'配套指标类别')
    sheet.write(0,6, u'配套面积')
    sheet.write(0,7, u'耕地面积')
    sheet.write(0,8, u'未用地面积')
    sheet.write(0,9, u'地块面积')
    sheet.write(0,10, u'新增建设用地面积')
    sheet.write(0,11, u'区县')
    sheet.write(0,12, u'安排指标依据')
    sheet.write(0,13, u'其他农用地面积')

    row_start_index = 0
    for item in _QuerySet:
        row_start_index += 1
        sheet.write(row_start_index,0, item.batch_name)
        sheet.write(row_start_index,1, item.project_name)
        sheet.write(row_start_index,2, PROJECT_TYPE_CHOICES.__getitem__(item.project_type-1)[1])
        sheet.write(row_start_index,3, GROUND_USE_TYPE_CHOICES.__getitem__(item.used_type-2)[1])
        sheet.write(row_start_index,4, item.ground_num)
        sheet.write(row_start_index,5, item.match_target_type)
        sheet.write(row_start_index,6, item.match_area)
        sheet.write(row_start_index,7, item.plough_area)
        sheet.write(row_start_index,8, item.unused_area)
        sheet.write(row_start_index,9, item.total_area)
        sheet.write(row_start_index,10, item.stock_const_area)
        sheet.write(row_start_index,11, COUNTY_CHOICES.__getitem__(item.county-1)[1])
        sheet.write(row_start_index,12, item.target_according)
        sheet.write(row_start_index,13, item.other_farmland)
    wbk.save(current_app.config['PROJECT_DIR']+'/static/xls/%s.xls'%name)
    return "/static/xls/%s.xls"%name




