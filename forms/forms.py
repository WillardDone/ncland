# -*-  coding=utf-8 -*-

import re

from flask.ext import wtf
from flask.ext.wtf import Form, TextAreaField, SubmitField, \
    TextField, ValidationError, required, email, url, optional, \
    SelectField, DecimalField,validators,RadioField

from models.model import Member,Batch
from utils.choices import YEAR_CHOICES,COUNTY_CHOICES,INDUSTRY_TYPE_CHOICES,\
    GROUND_USE_TYPE_CHOICES,PROJECT_TYPE_CHOICES,TARGET_TYPE_CHOICES

class LoginForm(Form):

    username = wtf.TextField(u"用户名", validators=[required(
            message="You must provide an email or username")])
    password = wtf.PasswordField(u"密码")
    submit = wtf.SubmitField(u"登录")

class MemberForm(Form):

    username = wtf.TextField(
        validators = [validators.Required(u'用户名是必填项！'), 
        validators.Length(max=100)])

    password = wtf.PasswordField(label=u'密码', 
        validators = [validators.Required(u'必填'), 
        validators.Length(max=20), 
        validators.Length(min=6, 
            message=u'最小位数6位.')]
    )
    password2 = wtf.PasswordField(label=u'密码', 
        validators = [validators.Required(u'必填'), 
        validators.Length(max=20), 
        validators.Length(min=6,
            message=u'最小位数6位.'),
        validators.EqualTo('password', 
            message=u'两次密码不匹配!')]
    )
   

    def validate_username(self, filed):

        username = filed.data.strip()
        if Member.query.filter_by(
            username=username).all():
            raise ValidationError(u'用户名已经存在！')

class addBatchForm(Form):

    year = wtf.SelectField(label=u'年度：',coerce=str,choices=YEAR_CHOICES)
    county = wtf.SelectField(label=u'区县：',coerce=str,choices=COUNTY_CHOICES)
    batch_name = wtf.TextField(
        validators = [validators.Required(u'建设用地批次名称是必填项！'), 
        validators.Length(max=100)])
    remark = wtf.TextAreaField(
        validators = [validators.Required(u'备注是必填项！'), 
        validators.Length(max=100)])

class addGroundForm(Form):

    batch_name = wtf.SelectField(label=u'选择批次：',coerce=int,choices=[(batch.id,batch.batch_name) for batch in Batch.query.all()])
    county = wtf.SelectField(label=u'区县：',coerce=str,choices=COUNTY_CHOICES)
    project_type = wtf.SelectField(label=u'项目类型：',coerce=str,choices=PROJECT_TYPE_CHOICES)
    industry_type = wtf.SelectField(label=u'产业类型：',coerce=str,choices=INDUSTRY_TYPE_CHOICES)
    used_type = wtf.SelectField(label=u'土地用途：',coerce=str,choices=GROUND_USE_TYPE_CHOICES)
    ground_num = wtf.TextField(label=u"地块编号：", validators=[required(
            message=u"地块编号不能为空！")])
    project_name = wtf.TextField(label=u"项目名称：", validators=[required(
            message=u"项目名称不能为空！")])
    plough_area = wtf.TextField(label=u"耕地面积：", validators=[required(
            message=u"耕地面积不能为空！")])
    other_farmland = wtf.TextField(label=u"其他农用地：", validators=[required(
            message=u"其他农用地面积不能为空！")])
    unused_area = wtf.TextField(label=u"未利用地：", validators=[required(
            message=u"未利用地面积不能为空！")])
    stock_const_area = wtf.TextField(label=u"存量建设用地面积：", validators=[required(
            message=u"存量建设用地面积不能为空！")])
    increased_const_area = wtf.TextField(label=u"涉及新增建设用地面积：", validators=[required(
            message=u"存量建设用地面积不能为空！")])
    total_area = wtf.TextField(label=u"地块面积：")
    target_area = wtf.TextField(label=u"指标面积：")
    target_type = wtf.SelectField(label=u'配套指标类型：',coerce=str,choices=TARGET_TYPE_CHOICES)
    match_area = wtf.TextField(label=u"配套面积：", validators=[required(
                message=u"配套面积不能为空！")])

    # match_target_type = [wtf.BooleanField(label=u"指标类型：",
    #         validators=[required(message="指标类型不能为空！")]) for choices in TARGET_TYPE_CHOICES]
    
    target_according = wtf.TextAreaField(label=u"安排指标依据：", validators=[required(
                message=u"安排指标依据不能为空！")])

    

class addFirstExaForm(Form):
    """添加初审表单"""
    project_name = wtf.TextField(label=u"项目名称：", validators=[required(
            message=u"项目名称不能为空！")])
    project_address1 = wtf.SelectField(label=u'项目坐落：',coerce=str,choices=COUNTY_CHOICES)
    project_address2 = wtf.TextField(label=u"项目座落2：", validators=[required(
            message=u"项目坐落不能为空！")])
    project_area = wtf.TextField(label=u"项目用地面积：", validators=[required(
            message=u"项目用地面积不能为空！")])
    increased_const_area = wtf.TextField(label=u"新增建设用地面积：", validators=[required(
            message=u"新增建设用地面积不能为空！")])
    other_farmland = wtf.TextField(label=u"其中农用地[含：耕地]：", validators=[required(
            message=u"其他农用地面积不能为空！")])
    unused_area = wtf.TextField(label=u"未利用地：", validators=[required(
            message=u"未利用地面积不能为空！")])
    inquiry_time = wtf.TextField(label=u"省厅预审时间：", validators=[required(
                message=u"省厅预审时间不能为空！")])
    applicant = wtf.TextField(label=u"申请单位：", validators=[required(
            message=u"申请单位不能为空！")])
    reply_num = wtf.TextField(label=u"省厅初审批复文号：", validators=[required(
            message=u"省厅初审批复文号不能为空！")])
    apply_time = wtf.TextField(label=u"申请时间：", validators=[required(
                message=u"申请时间不能为空！")])
    examine_suggestion = wtf.TextAreaField(label=u"审查意见：", validators=[required(
                message=u"审查意见不能为空！")])



class addPreExaForm(Form):
    """添加预审表单"""

    project_name = wtf.TextField(label=u"项目名称：", validators=[required(
            message=u"项目名称不能为空！")])
    project_address1 = wtf.SelectField(label=u'项目坐落：',coerce=str,choices=COUNTY_CHOICES)
    project_address2 = wtf.TextField(label=u"项目座落2：", validators=[required(
            message=u"项目坐落不能为空！")])
    project_area = wtf.TextField(label=u"项目用地面积：")
    increased_const_area = wtf.TextField(label=u"新增建设用地面积：", validators=[required(
            message=u"新增建设用地面积！")])
    other_farmland = wtf.TextField(label=u"其他农用地：", validators=[required(
            message=u"其他农用地面积不能为空！")])
    unused_area = wtf.TextField(label=u"未利用地：", validators=[required(
            message=u"未利用地面积不能为空！")])
    apply_time = wtf.TextField(label=u"申请日期：", validators=[required(
                message=u"创建日期不能为空！")])
    applicant = wtf.TextField(label=u"申请单位：", validators=[required(
            message=u"申请单位不能为空！")])
    reply_num = wtf.TextField(label=u"预审批复文号：")
    review_time = wtf.TextField(label=u"审查时间：", validators=[required(
                message=u"审查时间不能为空！")])
    examine_suggestion = wtf.TextAreaField(label=u"审查意见：", validators=[required(
                message=u"审查意见不能为空！")])
