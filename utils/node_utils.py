#!/bin/env python
# encoding:utf-8
from utils import string_utils


def read_lines(lines):
    last_node = None
    nodes = {}
    for i in range(len(lines)):
        line = lines[i]
        if string_utils.index_of(line, 'Node 0x') is not None:
            line = line.strip()
            node = line[str(line).index('0x'):str(line).index('[') - 1]
            last_node = node
            nodes[node] = NodeObjModel(node)
        if string_utils.index_of(line, 'Connection: ') is not None:
            nodes[last_node].connections = lines[i + 1].strip().replace('*', '')
    return nodes


def get_connects(nodes):
    for (key, value) in nodes.items():
        if value.connections is not None:
            params = (key + ' ' + str(value.connections)).split(' ')
            location_list = []
            for i in range(1, len(params)):
                location_list.append(params[0] + '-' + params[i].strip())
            value.location_list = location_list
            print value.location_list


def get_connects_dict(location_dict):
    after_dict = {}
    for key in location_dict:
        after_list = []
        sub_list = location_dict[key]
        for string in sub_list:
            next_node = string.split('-')[1]
            try:
                sub_sub_list = location_dict[next_node]
                for string1 in sub_sub_list:
                    last_node = string1.split('-')[1]
                    after_list.append(string + '-' + last_node)
            except KeyError:
                after_list.append(string)
            after_dict[key] = after_list
    print after_dict


class NodeObjModel:

    def __init__(self, node):
        self.node = node
        self.connections = None
        self.location_list = []