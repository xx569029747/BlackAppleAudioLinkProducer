#!/bin/env python
# encoding:utf-8
import re

from utils import string_utils


def convert_type(line):
    if string_utils.index_of(line, 'Line Out at Ext'):
        return 'Line Out at Ext'
    elif string_utils.index_of(line, 'Line In at Ext'):
        return 'Line In at Ext'
    elif string_utils.index_of(line, 'Mic at Ext'):
        return 'Mic at Ext'
    elif string_utils.index_of(line, 'HP Out at Ext'):
        return 'HP Out at Ext'
    elif string_utils.index_of(line, 'SPDIF Out at Int'):
        return 'SPDIF Out at Int'
    elif string_utils.index_of(line, 'Speaker at Int'):
        return 'Speaker at Int'
    elif string_utils.index_of(line, 'Mic at Int'):
        return 'Mic at Int'
    else:
        return None


def modify_codec_after_first(audio_type, codec):
    if audio_type == 'SPDIF Out at Int':
        codec[0] = string_utils.replace(codec[0], 7, '0')
        codec[1] = string_utils.replace(codec[1], 7, '1')
        codec[2] = string_utils.replace(codec[2], 6, '4')
        codec[3] = string_utils.replace(codec[3], 6, '0')
    elif audio_type == 'Line Out at Ext':
        codec[0] = string_utils.replace(codec[0], 7, 'f')
        codec[1] = string_utils.replace(codec[1], 7, '0')
        codec[2] = string_utils.replace(codec[2], 6, '0')
        codec[3] = string_utils.replace(codec[3], 6, '0')
    elif audio_type == 'Mic at Ext':
        codec[0] = string_utils.replace(codec[0], 7, '0')
        codec[1] = string_utils.replace(codec[1], 7, '0')
        codec[2] = string_utils.replace(codec[2], 6, '8')
        codec[3] = string_utils.replace(codec[3], 6, '0')
    elif audio_type == 'Line In at Ext':
        codec[0] = string_utils.replace(codec[0], 7, '0')
        codec[1] = string_utils.replace(codec[1], 7, '0')
        codec[2] = string_utils.replace(codec[2], 6, '8')
        codec[3] = string_utils.replace(codec[3], 6, '0')
    elif audio_type == 'HP Out at Ext':
        codec[0] = string_utils.replace(codec[0], 7, '0')
        codec[1] = string_utils.replace(codec[1], 7, '0')
        codec[2] = string_utils.replace(codec[2], 6, '2')
        codec[3] = string_utils.replace(codec[3], 6, '0')
    return codec


def modify_codec_with_line_out(audio_type, codec):
    if audio_type == 'SPDIF Out at Int':
        codec[0] = string_utils.replace(codec[0], 6, '4')
    elif audio_type == 'Line Out at Ext':
        codec[0] = string_utils.replace(codec[0], 6, '2')
    elif audio_type == 'Mic at Ext':
        codec[0] = string_utils.replace(codec[0], 6, '6')
    elif audio_type == 'Line In at Ext':
        codec[0] = string_utils.replace(codec[0], 6, '5')
    elif audio_type == 'HP Out at Ext':
        codec[0] = string_utils.replace(codec[0], 6, '3')
    return modify_codec_after_first(audio_type, codec)


def modify_codec_without_line_out(audio_type, codec):
    if audio_type == 'SPDIF Out at Int':
        codec[0] = string_utils.replace(codec[0], 6, '4')
    elif audio_type == 'Line Out at Ext':
        codec[0] = string_utils.replace(codec[0], 6, '2')
    elif audio_type == 'Mic at Ext':
        codec[0] = string_utils.replace(codec[0], 6, '6')
    elif audio_type == 'Line In at Ext':
        codec[0] = string_utils.replace(codec[0], 6, '5')
    elif audio_type == 'HP Out at Ext':
        codec[0] = string_utils.replace(codec[0], 6, '3')
    return modify_codec_after_first(audio_type, codec)


def modify_codec(model_list, has_line_out):
    for model in model_list:
        audio_type = model.audio_type
        print audio_type
        print model.codec
        if has_line_out:
            model.codec = modify_codec_with_line_out(audio_type, model.codec)
        else:
            model.codec = modify_codec_without_line_out(audio_type, model.codec)
        print model.codec
        print '####################'
    return model_list


def convert_text_to_obj(obj):
    text = obj.text
    start_modify_line = False
    model_list = []
    has_line_out = False
    for line in str(text).split('\n'):
        if line.startswith('Codec'):
            for string in line.split('   '):
                if string.startswith('Codec'):
                    obj.codec = string.split(':')[1].strip()
                elif string.startswith('DevID'):
                    obj.device_id = string.split(':')[1].strip()
        elif start_modify_line:
            if not line.startswith('-'):
                params = re.split(r'\s+', line.strip())
                audio_codec = params[len(params) - 4:len(params)]
                audio_type = convert_type(line)
                if len(audio_codec) == 4 and audio_type is not None:
                    has_line_out = has_line_out or string_utils.index_of(audio_type, 'Line Out') is not None
                    model_list.append(CodecModel(audio_type, params[len(params) - 6], audio_codec))
        elif string_utils.index_of(line, 'Modified Verbs'):
            start_modify_line = True
    obj.audio_codec = modify_codec(model_list, has_line_out)
    return obj


class CodecModel:

    def __init__(self, audio_type, location, codec):
        self.audio_type = audio_type
        self.location = location
        self.codec = codec


class VerbitObj:

    def __init__(self, text):
        self.text = text
        convert_text_to_obj(self)
