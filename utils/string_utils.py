#!/bin/env python
# encoding:utf-8


def index_of(str_obj, sub_obj):
    if not isinstance(str_obj, str):
        str_obj = str(str_obj)
    if not isinstance(sub_obj, str):
        sub_obj = str(sub_obj)
    try:
        index = str_obj.index(sub_obj)
    except ValueError:
        index = None
    return index
