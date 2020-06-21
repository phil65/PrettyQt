# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""


def string_to_num_array(array: str) -> list:
    floats = [float(i) for i in array.split(",")]
    return [int(i) if i.is_integer() else i for i in floats]
