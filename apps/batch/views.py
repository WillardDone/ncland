# -*-coding: utf-8 -*-
import datetime
import xlwt
from datetime import date

from flask import request, Blueprint,render_template,\
    current_app,url_for,redirect,g,flash,session
from flask.ext.principal import identity_changed, \
  Identity, AnonymousIdentity
from permissions import auth,admin
from extensions import db

from utils.pagination import Pagination
from models.model import Batch

from utils.choices import TARGET_TYPE_CHOICES,COUNTY_CHOICES,\
        PROJECT_TYPE_CHOICES,INDUSTRY_TYPE_CHOICES,GROUND_USE_TYPE_CHOICES,YEAR_CHOICES


batch = Blueprint('batch', __name__)

@batch.route('/',methods=['POST','GET'])
def index():
    """新增批次"""
    g.__setattr__('action','batch.typein')
    from forms import addBatchForm
    form = addBatchForm()

    if form.validate_on_submit():
        _batch = Batch()

        form.populate_obj(_batch)
        db.session.add(_batch)
        db.session.commit()
        return redirect(url_for('batch.batchlist'))
    

    return render_template('/batch/batch.html',
        form=form)


@batch.route('/batchlist',methods=['POST','GET'])
def batchlist():
    """所有批次列表"""
    g.__setattr__('action','batch.batchlist')

    page = int(request.form.get('page',1))
    pagesize = int(request.form.get('page_size',2))

    action = request.form.get('action','')

    #查询条件
    _county = int(request.form.get('county',0))
    _year = int(request.form.get('year',0))

    print "<>"*40,_county,_year
    batchlist = Batch.query

    if _county:
        batchlist = batchlist.filter_by(county=_county)
    if _year:
        batchlist = batchlist.filter_by(year=_year)
  

    batchlist = batchlist.order_by('id desc').all()
    print len(batchlist)
    # print Ground.query.filter(and_(filter_str)).order_by('id desc')

    if action == "export":
        return redirect(batch_excel_created(batchlist)) 


    pagination = Pagination(batchlist,page,pagesize)
    batchlist = pagination.list()
    print len(batchlist)
    return render_template('/batch/batchlist.html',
        pagination=pagination,
        page=page,
        page_size=pagesize,
        batchlist=batchlist,
        countys=COUNTY_CHOICES,
        years=YEAR_CHOICES,
        _county=str(_county),
        _year=str(_year)
        )    


def batch_excel_created(_QuerySet, name=u"batch"):
    wbk = xlwt.Workbook()
    sheet = wbk.add_sheet('sheet 1')
    sheet.write(0,0, u'序号(批次编号)')
    sheet.write(0,1, u'建设用地批次名称')
    sheet.write(0,2, u'年度')
    sheet.write(0,3, u'区县')
    sheet.write(0,4, u'耕地面积')
    sheet.write(0,5, u'未用地面积')
    sheet.write(0,6, u'存量建设用地面积')
    sheet.write(0,7, u'新增建设用地面积')
    sheet.write(0,8, u'地块面积')
    sheet.write(0,9, u'其他农用地面积')
    sheet.write(0,10, u'备注')

    row_start_index = 0
    for item in _QuerySet:
        row_start_index += 1
        sheet.write(row_start_index,0, item.id)
        sheet.write(row_start_index,1, item.batch_name)
        sheet.write(row_start_index,2, item.year)
        sheet.write(row_start_index,3, item.county)
        sheet.write(row_start_index,4, item.plough_area)
        sheet.write(row_start_index,5, item.unused_area)
        sheet.write(row_start_index,6, item.stock_const_area)
        sheet.write(row_start_index,7, item.increased_const_area)
        sheet.write(row_start_index,8, item.total_area)
        sheet.write(row_start_index,9, item.other_farmland)
        sheet.write(row_start_index,10, item.remark)
    wbk.save(current_app.config['PROJECT_DIR']+'/static/xls/%s.xls'%name)
    return "/static/xls/%s.xls"%name



