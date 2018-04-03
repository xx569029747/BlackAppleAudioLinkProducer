#!/bin/env python
# encoding:utf-8
import commands

import os

from VerbitObj import VerbitObj


def generate_code(linux_audio_code_file):
    cmd = 'verbit ' + linux_audio_code_file
    code, output = commands.getstatusoutput(cmd)
    if code == 0:
        return VerbitObj(output)
    else:
        raise RuntimeError


def main():
    code_file = '/Volumes/EveryThing/Downloads/Audio/audio_1150/alc1150_code'
    lines = open(code_file, 'r').readlines()
    tmp_file_path = './tmp_file'
    tmp_file = open(tmp_file_path, 'w')
    for line in lines:
        if line.strip() != 'AFG Function Id: 0x1 (unsol 1)':
            tmp_file.write(line)
    generate_code(tmp_file_path)
    os.remove(tmp_file_path)


if __name__ == '__main__':
    main()
