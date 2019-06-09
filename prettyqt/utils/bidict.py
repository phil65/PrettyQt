# -*- coding: utf-8 -*-

from bidict import bidict as bdct


class bidict(bdct):

    def __init__(self, *args, **kwargs):
        super().__init__(kwargs)
