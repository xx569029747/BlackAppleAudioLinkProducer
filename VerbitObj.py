#!/bin/env python
# encoding:utf-8
import re

from utils import string_utils

codec_with_line_out = {
    'Mic at Int': [[0, 6, '5']],
    'Speaker at Int': [[0, 6, '1']],
    'Line Out at Ext': [[0, 6, '2']],
    'Mic at Ext': [[0, 6, '6']],
    'Line In at Ext': [[0, 6, '5']],
    'HP Out at Ext': [[0, 6, '3']],
    'SPDIF Out at Int': [[0, 6, '4']]
}

codec_without_line_out = {
    'Mic at Int': [[0, 6, '4']],
    'HP Out at Ext': [[0, 6, '2']],
    'Mic at Ext': [[0, 6, '5']],
    'Line In at Ext': [[0, 6, '4']],
    'Speaker at Int': [[0, 6, '1']],
    'SPDIF Out at Int': [[0, 6, '3']]
}

common_dict = {
    'Mic at Int': [[0, 7, '0'], [1, 7, '1'], [2, 7, 'a'], [3, 6, '9']],
    'Speaker at Int': [[0, 7, '0'], [1, 7, '1'], [2, 7, '1'], [3, 6, '9']],
    'Line Out at Ext': [[0, 7, 'f'], [1, 7, '0'], [2, 7, '0'], [3, 6, '0']],
    'Mic at Ext': [[0, 7, '0'], [1, 7, '0'], [2, 7, '8'], [3, 6, '0']],
    'Line In at Ext': [[0, 7, '0'], [1, 7, '0'], [2, 7, '8'], [3, 6, '0']],
    'HP Out at Ext': [[0, 7, '0'], [1, 7, '0'], [2, 7, '2'], [3, 6, '0']],
    'SPDIF Out at Int': [[0, 7, '0'], [1, 7, '1'], [2, 7, '4'], [3, 6, '0']]
}

codec_dict = {}


def modify_audio_codec(audio_type, audio_codec):
    if audio_type in codec_dict:
        for i in codec_dict[audio_type]:
            index = i[0]
            audio_codec[index] = string_utils.replace(audio_codec[index], i[1], i[2])
    return audio_codec


def convert_type(line):
    for key in codec_with_line_out:
        if string_utils.index_of(line, key):
            return key
    return None


def modify_codec(model_list, has_line_out):
    global codec_dict
    if has_line_out:
        codec_dict = codec_with_line_out
    else:
        codec_dict = codec_without_line_out
    for (key, value) in codec_dict.items():
        for i in range(len(common_dict[key])):
            value.append(common_dict[key][i])

    for model in model_list:
        model.codec = modify_audio_codec(model.audio_type, model.codec)
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
        self.audio_codec = []
        self.codec = None
        self.device_id = None
        convert_text_to_obj(self)
