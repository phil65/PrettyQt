# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets

from prettyqt import widgets


class ToolButton(QtWidgets.QToolButton):

    @classmethod
    def for_menu(cls, menu, icon=None):
        btn = cls()
        btn.setMenu(menu)
        btn.setPopupMode(cls.InstantPopup)
        btn.set_icon(icon)
        return btn


ToolButton.__bases__[0].__bases__ = (widgets.AbstractButton,)
