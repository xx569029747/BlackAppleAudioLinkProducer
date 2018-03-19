#!/bin/env python
# encoding:utf-8
import re

from utils import string_utils


def convert_text_to_obj(obj):
    text = obj.text
    start_modify_line = False
    for line in str(text).split('\n'):
        if line.startswith('Codec'):
            for string in line.split('   '):
                if string.startswith('Codec'):
                    obj.codec = string.split(':')[1].strip()
                elif string.startswith('DevID'):
                    obj.device_id = string.split(':')[1].strip()
        elif start_modify_line:
            if not line.startswith('-'):
                for param in re.split(r'\s+', line):
                    print param
        elif string_utils.index_of(line, 'Modified Verbs'):
            start_modify_line = True
    return obj


class VerbitObj:

    def __init__(self, text):
        self.text = text
        convert_text_to_obj(self)
