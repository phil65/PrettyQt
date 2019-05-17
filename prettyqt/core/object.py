# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtCore


class Object(QtCore.QObject):

    def to_json(self):
        dct = self.__getstate__()
        for k, v in dct.items():
            if isinstance(v, QtCore.QObject):
                dct[k] = v.to_json()
        return dct
