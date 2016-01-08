#!/usr/bin/python3
# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t -*-

from collections import OrderedDict

################################################################################
# interface
################################################################################

def new_delta():
    return _delta()

def merge_delta(delta, delta2):
    delta.oplist += delta2.oplist

def apply_delta(obj, delta):
    for obj_id, op_name, arg_list in delta.oplist:
        obj = _get_obj_by_id(obj)
        if op_name == "list_append":
            assert isinstance(obj, list)
            obj.append(arg_list[0])
        elif op_name == "list_modify":
            assert isinstance(obj, list)
            obj[int(arg_list[0])] = arg_list[1]
        elif op_name == "dict_add":
            assert isinstance(obj, dict) and str(arg_list[0]) not in obj
            obj[str(arg_list[0])] = arg_list[1]
        elif op_name == "dict_modify":
            assert isinstance(obj, dict) and str(arg_list[0]) in obj
            obj[str(arg_list[0])] = arg_list[1]
        else:
            assert False

################################################################################
# implementation
################################################################################

class _delta:

    def __init__(self):
        self.oplist = []

    def add_op(self, obj_id, op_name, *kargs):
        if op_name == "list_append":
            assert len(kargs) == 1      # list_append value
        elif op_name == "list_modify":
            assert len(kargs) == 2      # list_set index value
        elif op_name == "dict_add":
            assert len(kargs) == 2      # dict_add key value
        elif op_name == "dict_modify":
            assert len(kargs) == 2      # dict_set key value
        else:
            assert False

        op = (obj_id, op_name, kargs)

def _get_obj_by_id(root_obj, obj_id):
    ret = root_obj
    for on in obj_id.split(";"):
        if ":" in on:
            on, oi = on.split(":")
        else:
            oi = None

        ret = getattr(ret, on)
        if oi is not None:
            if isinstance(ret, list):
                ret = ret[int(oi)]
            elif isinstance(ret, OrderedDict) or isinstance(ret, dict):
                ret = ret[str(oi)]
            else:
                assert False

    return ret

