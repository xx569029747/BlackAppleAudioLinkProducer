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


def replace(str_obj, index, char):
    if len(str_obj) - 1 < index:
        return str_obj + char
    else:
        str_list = list(str_obj)
        str_list[index] = char
        return ''.join(str_list)


def read_lines(lines):
    for i in range(len(lines)):
        line = lines[i]
        if index_of(line, 'Node 0x') is not None:
            print line.strip()
        if index_of(line, 'Connection: ') is not None:
            print lines[i + 1].strip().replace('*', '')
