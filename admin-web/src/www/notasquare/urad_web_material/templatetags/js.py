from django.template import Library

import json

register = Library()

@register.filter(name='get')
def get(o, index):
    try:
        return o[index]
    except:
        pass

@register.filter(name='is_array')
def is_array(o):
    try:
        if type(o) == list:
            return True
    except:
        pass

@register.filter(name='is_str')
def is_str(o):
    try:
        if type(o) == unicode:
            return True
    except:
        pass

@register.filter(name='is_dict')
def is_dict(o):
    try:
        if type(o) == dict:
            return True
    except:
        pass

@register.filter(name='filter')
def filter(o):
    try:
        text_arr = o.split('_')
        text_arr = [x.capitalize() for x in text_arr]
        text = ' - '.join(text_arr)
        return text
    except:
        pass
