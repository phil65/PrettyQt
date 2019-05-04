# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

import qtawesome as qta
from qtpy import QtWidgets

from prettyqt import widgets


class PushButton(QtWidgets.QPushButton):

    def __getstate__(self):
        return dict(title=self.text(),
                    enabled=self.isEnabled())

    def __setstate__(self, state):
        super().__init__()
        self.setText(state["title"])
        self.setEnabled(state["enabled"])

    def set_enabled(self):
        self.setEnabled(True)

    def set_disabled(self):
        self.setEnabled(False)

    def set_icon(self, icon):
        if isinstance(icon, str):
            icon = qta.icon(icon)
        if icon:
            self.setIcon(icon)

    def set_style_icon(self, icon: str):
        STYLES = dict(close=QtWidgets.QStyle.SP_TitleBarCloseButton,
                      maximise=QtWidgets.QStyle.SP_TitleBarMaxButton)
        qicon = self.style().standardIcon(STYLES[icon], None, self)
        self.setIcon(qicon)


if __name__ == "__main__":
    app = widgets.Application.create_default_app()
    widget = PushButton("This is a test")
    import pickle
    with open('data.pkl', 'wb') as jar:
        pickle.dump(widget, jar)
    with open('data.pkl', 'rb') as jar:
        widget2 = pickle.load(jar)
    assert widget2.text() == widget.text()
    widget.show()
    app.exec_()
