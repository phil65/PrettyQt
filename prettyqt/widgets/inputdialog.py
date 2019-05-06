# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets

from prettyqt import widgets


class InputDialog(QtWidgets.QInputDialog):

    @classmethod
    def get_int(cls, title=None, label=None, icon=None):
        par = widgets.Dialog()
        par.set_icon(icon)
        v = cls.getInt(par, title, label)
        if v[1]:
            return v[0]

    @classmethod
    def get_float(cls, title=None, label=None, icon=None):
        par = widgets.Dialog()
        par.set_icon(icon)
        v = cls.getDouble(par, title, label)
        if v[1]:
            return v[0]

    @classmethod
    def get_text(cls, title=None, label=None, icon=None, default_value=""):
        par = widgets.Dialog()
        par.set_icon(icon)
        v = cls.getText(par, title, label, text=default_value)
        if v[1]:
            return v[0]

    @classmethod
    def get_item(cls, items, title=None, label=None, icon=None):
        par = widgets.Dialog()
        par.set_icon(icon)
        v = cls.getItem(par, title, label, items, editable=False)
        if v[1]:
            return v[0]


if __name__ == "__main__":
    app = widgets.Application.create_default_app()
    result = InputDialog.get_text("a", "b", icon="mdi.timer")
    print(result)
    app.exec_()
