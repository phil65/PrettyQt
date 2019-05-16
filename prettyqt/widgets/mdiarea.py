# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from bidict import bidict

from qtpy import QtWidgets

from prettyqt import widgets


VIEW_MODES = bidict(dict(default=QtWidgets.QMdiArea.SubWindowView,
                         tabbed=QtWidgets.QMdiArea.TabbedView))


WINDOW_ORDERS = bidict(dict(creation=QtWidgets.QMdiArea.CreationOrder,
                            stacking=QtWidgets.QMdiArea.StackingOrder,
                            activation=QtWidgets.QMdiArea.ActivationHistoryOrder))


class MdiArea(QtWidgets.QMdiArea):

    def set_view_mode(self, mode):
        if mode not in VIEW_MODES:
            raise ValueError("Invalid value for mode.")
        self.setViewMode(VIEW_MODES[mode])

    def get_view_mode(self):
        return VIEW_MODES.inv[self.viewMode()]

    def set_window_order(self, mode):
        if mode not in WINDOW_ORDERS:
            raise ValueError("Invalid value for mode.")
        self.setViewMode(WINDOW_ORDERS[mode])

    def get_window_order(self):
        return WINDOW_ORDERS.inv[self.viewMode()]


MdiArea.__bases__[0].__bases__ = (widgets.AbstractScrollArea,)


if __name__ == "__main__":
    app = widgets.app()
    widget = MdiArea()
    widget.show()
    app.exec_()
