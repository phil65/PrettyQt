# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

import logging
from typing import Dict

import qtawesome as qta
from qtpy import QtCore, QtWidgets

from prettyqt import core, widgets

DOCK_POSITIONS = dict(top=QtCore.Qt.TopDockWidgetArea,
                      bottom=QtCore.Qt.BottomDockWidgetArea,
                      left=QtCore.Qt.LeftDockWidgetArea,
                      right=QtCore.Qt.RightDockWidgetArea)


class MainWindow(QtWidgets.QMainWindow):
    """
    Class for our mainWindow
    includes all docks, a centralwidget and a toolbar
    """

    def __getitem__(self, index):
        return self.findChild(QtWidgets.QWidget, index)

    def load_window_state(self):
        settings = core.Settings()
        geom = settings.value("mainwindow.geometry", None)
        state = settings.value("mainwindow.state", None)
        if geom is not None and state is not None:
            try:
                self.restoreGeometry(geom)
                self.restoreState(state)
            except TypeError:
                logging.info("Wrong type for window state. Probably Qt binding switch?")
                pass

    def closeEvent(self, event):
        """
        override, gets executed when app gets closed.
        saves GUI settings
        """
        settings = core.Settings()
        settings.set_value("mainwindow.geometry", self.saveGeometry())
        settings.set_value("mainwindow.state", self.saveState())
        super().closeEvent(event)
        event.accept()

    def set_icon(self, icon):
        if icon:
            if isinstance(icon, str):
                icon = qta.icon(icon, color="lightgray")
            self.setWindowIcon(icon)

    def set_stylesheet(self, item, dct: Dict[str, str]) -> str:
        ss = "; ".join(f"{k.replace('_', '-')}: {v}" for k, v in dct.items())
        self.setStyleSheet(f"{item} {{{ss};}}")

    def add_widget_as_dock(self,
                           name: str,
                           title: str,
                           vertical: bool = True,
                           position: str = "left") -> widgets.DockWidget:
        dock_widget = widgets.DockWidget(self, name=name, title=title)
        widget = widgets.Widget()
        widget.setObjectName(f"{name}.widget")
        orientation = "vertical" if vertical else "horizontal"
        layout = widgets.BoxLayout(orientation, widget)
        layout.set_margin(0)
        dock_widget.setWidget(widget)
        self.add_dockwidget(dock_widget, position)
        dock_widget.box = layout
        return dock_widget

    def add_dockwidget(self, dockwidget, position):
        position = DOCK_POSITIONS[position]
        self.addDockWidget(QtCore.Qt.DockWidgetArea(position), dockwidget)

    def toggle_fullscreen(self):
        """toggle between fullscreen and regular size
        """
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()


if __name__ == "__main__":
    app = widgets.Application.create_default_app()
    form = MainWindow()
    form.show()
    app.exec_()
