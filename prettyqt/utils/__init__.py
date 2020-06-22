# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

import bidict as bdct


class bidict(bdct.bidict):

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], dict):
            super().__init__(args[0])
        else:
            super().__init__(kwargs)
