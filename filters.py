# -*- coding:utf-8 -*-
import time,datetime
import os
import simplejson
from utils.choices import YEAR_CHOICES,COUNTY_CHOICES,PROJECT_TYPE_CHOICES, \
        INDUSTRY_TYPE_CHOICES,GROUND_USE_TYPE_CHOICES,TARGET_TYPE_CHOICES


def configure_template_filters(app):
    
    @app.template_filter()
    def num2project_type(n):
         return PROJECT_TYPE_CHOICES.__getitem__(n-1)[1]

    @app.template_filter()
    def num2county(n):
        return COUNTY_CHOICES.__getitem__(n-1)[1]

    @app.template_filter()
    def num2industry_type(n):
        return INDUSTRY_TYPE_CHOICES.__getitem__(n-2)[1]    

    
    @app.template_filter()
    def num2ground_use_type(n):
        return GROUND_USE_TYPE_CHOICES.__getitem__(n-2)[1]    

    @app.template_filter()
    def num2target_type(n):
        return TARGET_TYPE_CHOICES.__getitem__(n-1)[1] 

    @app.template_filter()
    def timestamp_format(value, style=''):

        if not value:
            return value
            
        if not style:
            style = '%Y-%m-%d %H:%M:%S'

        return value.strftime(style)