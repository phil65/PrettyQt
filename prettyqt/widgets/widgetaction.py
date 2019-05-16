# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets

from prettyqt import widgets


class WidgetAction(QtWidgets.QWidgetAction):
    pass


WidgetAction.__bases__[0].__bases__ = (widgets.Action,)
