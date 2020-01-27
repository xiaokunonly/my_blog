from django.utils import timezone
import math
from django import template
#要成为一个可用的filter,文件中必须包含一个名为rigister的模块级变量
register=template.Library()

@register.filter(name='timesince_zh')
def time_sinch_zh(value):
    now=timezone.now()
    diff=now-value
    if diff.days==0 and diff.seconds>=0 and diff.seconds <60:
        return'刚刚'
    elif diff.days==0 and diff.seconds>=60 and diff.seconds<3600:
        return str(math.floor(diff.seconds/60))+'分钟前'
    elif diff.days==0 and diff.seconds>=3600 and diff.seconds<=86400:
        return str(math.floor(diff.seconds/3600))+'小时前'
    elif diff.days>=1 and diff.days<30:
        return str(diff.days)+'天前'
    elif diff.days>=30 and diff.days<365:
        return str(math.floor(diff.days/30))+'个月前'
    elif diff.days>=365:
        return str(math.floor(diff.days/365))+'年前'
@register.filter(name='string_trans')
def string_trans(value):
    return str(value)