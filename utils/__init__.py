# -*- coding: utf-8 -*-
from utils.choices import TARGET_TYPE_CHOICES,COUNTY_CHOICES,\
        PROJECT_TYPE_CHOICES,INDUSTRY_TYPE_CHOICES,GROUND_USE_TYPE_CHOICES
def match_target_type_resolution(typa='2_3_'):
    """针对配套指标类型作解析"""

    result = ""
    if typa:
        typa_list = typa.split('_')
        for t in typa_list:
            if t:
                result += (TARGET_TYPE_CHOICES.__getitem__(int(t)-1)[1]).encode('utf-8')+","
    return result.decode('utf-8')

