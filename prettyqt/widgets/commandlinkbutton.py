# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets

from prettyqt import widgets, core


QtWidgets.QCommandLinkButton.__bases__ = (widgets.PushButton,)


class CommandLinkButton(QtWidgets.QCommandLinkButton):

    value_changed = core.Signal(bool)


if __name__ == "__main__":
    app = widgets.app()
    widget = CommandLinkButton("This is a test")
    widget.show()
    app.exec_()
