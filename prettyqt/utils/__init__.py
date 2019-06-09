# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

import bidict as bdct


class bidict(bdct.bidict):

    def __init__(self, *args, **kwargs):
        super().__init__(kwargs)
