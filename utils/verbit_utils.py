#!/bin/env python
# encoding:utf-8
import commands

import os

from VerbitObj import VerbitObj
from utils import node_utils


def generate_code(linux_audio_code_file):
    cmd = 'verbit ' + linux_audio_code_file
    code, output = commands.getstatusoutput(cmd)
    if code == 0:
        return VerbitObj(output)
    else:
        raise RuntimeError


def main():
    code_file = '/Volumes/Storage/Documents/Private/alc269vc_audio/audio_files/codec_0'
    lines = open(code_file, 'r').readlines()
    tmp_file_path = './tmp_file'
    tmp_file = open(tmp_file_path, 'w')
    for line in lines:
        if line.strip() != 'AFG Function Id: 0x1 (unsol 1)':
            tmp_file.write(line)
    obj = generate_code(tmp_file_path)
    codec = ''
    for model in obj.audio_codec:
        for string in model.codec:
            codec += (string + ' ')
    nodes = node_utils.read_lines(lines)
    node_utils.get_connects(nodes)
    os.remove(tmp_file_path)


if __name__ == '__main__':
    main()
