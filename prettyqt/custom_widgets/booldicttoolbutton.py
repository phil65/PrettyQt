# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from prettyqt import widgets


class BoolDictToolButton(widgets.ToolButton):

    def __init__(self, title, icon=None, dct=None, parent=None):
        super().__init__(parent=parent)
        self.set_text(title)
        self.set_icon(icon)
        self.setMenu(widgets.Menu())
        self.set_popup_mode("instant")
        if dct:
            self.set_dict(dct)

    def __getitem__(self, key):
        menu = self.menu()
        return menu[key].isChecked()

    def __setitem__(self, key, value):
        menu = self.menu()
        menu[key].setChecked(value)

    def set_dict(self, dct):
        menu = self.menu()
        for k, v in dct.items():
            action = widgets.Action()
            action.set_text(v)
            action.setCheckable(True)
            action.id = k
            menu.add(action)

    def as_dict(self):
        return {act.id: act.isChecked() for act in self.menu()}


if __name__ == "__main__":
    app = widgets.app()
    dct = dict(a="test",
               b="test2")
    w = BoolDictToolButton("Title", None, dct)
    w.show()
    app.exec_()
