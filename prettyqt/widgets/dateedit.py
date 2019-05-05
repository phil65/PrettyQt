# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets


class DateEdit(QtWidgets.QDateEdit):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setCalendarPopup(True)

    def set_enabled(self):
        self.setEnabled(True)

    def set_disabled(self):
        self.setEnabled(False)


if __name__ == "__main__":
    from prettyqt import widgets
    app = widgets.Application.create_default_app()
    widget = DateEdit()
    widget.show()
    app.exec_()
