#!/bin/env python
# encoding:utf-8

import itertools


def index_of(str_obj, sub_str):
    try:
        str_obj.index(sub_str)
        return True
    except ValueError:
        return False


def convert_to_list(it):
    tmp = []
    for obj in it:
        tmp_list = []
        if isinstance(obj[0], list):
            tmp_list = list(obj[0])
            tmp_list.append(obj[1])
        elif isinstance(obj[1], list):
            tmp_list = list(obj[1])
            tmp_list.append(obj[0])
        else:
            tmp_list.append(obj[0])
            tmp_list.append(obj[1])
        tmp.append(tmp_list)
    return tmp


def deal(data_dict, keys, key, final_list):
    keys.remove(key)
    final_list = convert_to_list(itertools.product(final_list, data_dict.get(keys[0])))
    if len(keys) == 1:
        return final_list
    else:
        return deal(data_dict, keys, keys[0], final_list)


def read_to_lines():
    lines = open('/Volumes/EveryThing/Downloads/Audio/audio_1150/alc1150_code').readlines()
    for i in range(len(lines)):
        if index_of(lines[i], 'Node 0x'):
            print lines[i]
        if index_of(lines[i], 'Connection: '):
            print lines[i + 1]


def main():
    # read_to_lines()
    keys = ['0x12', '0x14', '0x15', '0x18', '0x1e']
    num_dict = {}
    lines = open('/Users/blue/Downloads/lines').readlines()
    after_dict = {}
    total_list = []
    final_dict = {}
    for line in lines:
        params = line.split(' ')
        key = params[0]
        sub_list = []
        for i in range(1, len(params)):
            sub_list.append(params[0] + '-' + params[i].strip())
        num_dict[key] = sub_list
    for key in num_dict:
        after_list = []
        sub_list = num_dict[key]
        for string in sub_list:
            next_node = string.split('-')[1]
            try:
                sub_sub_list = num_dict[next_node]
                for string1 in sub_sub_list:
                    last_node = string1.split('-')[1]
                    after_list.append(string + '-' + last_node)
                    total_list.append(string + '-' + last_node)
            except KeyError:
                after_list.append(string)
                total_list.append(string)
            after_dict[key] = after_list
    for string in total_list:
        length = len(string.split('-'))
        key = string.split('-')[length - 1]
        if key not in after_dict:
            after_dict[key] = {}
        tmp = list(after_dict[key])
        tmp.append(string)
        after_dict[key] = tmp
    for key in after_dict:
        if key in keys:
            final_dict[key] = after_dict.get(key)
    final_list = []
    keys = final_dict.keys()
    data_list = final_dict.get(keys[0])
    data_list = deal(final_dict, keys, keys[0], data_list)
    for tmp_list in data_list:
        is_add = True
        str_list = []
        for string in list(tmp_list):
            str_array = str(string).split('-')
            for tmp in str_array:
                if tmp not in str_list:
                    str_list.append(tmp)
                else:
                    is_add = False
                    break
        if is_add:
            final_list.append(tmp_list)
    for s in final_list:
        print s


def convert_to_10():
    new_data = []
    data = ['0x15-0x0d-0x03', '0x14-0x0c-0x02', '0x09-0x22-0x12', '0x1e-0x06', '0x08-0x23-0x18']
    for strings in data:
        new_string = []
        for string in strings.split('-'):
            new_string.append(str(int(string, 16)))
        new_data.append('-'.join(new_string))
    print new_data


if __name__ == '__main__':
    convert_to_10()
