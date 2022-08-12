from django import template
from datetime import datetime
from datetime import datetime, date
from Fast.utils.date import format_simple_date, format_simple_date_for_default
from django.utils.html import format_html

register = template.Library()

@register.filter(name='simple_date')
def _simple_date(date_obj: datetime):
    return format_simple_date(date_obj) if isinstance(date_obj, (date, datetime)) else date_obj

@register.filter(name='simple_date_for_date_field')
def _simple_date_for_date_field(date_obj: datetime):
    return format_simple_date_for_default(date_obj) if isinstance(date_obj, (date, datetime)) else date_obj

@register.filter(name='html')
def _html(text: str):
    return format_html(text)

@register.filter(name='if_is_None')
def _if_is_None(obj, default: str):
    return obj if obj and obj != 'None' else default

