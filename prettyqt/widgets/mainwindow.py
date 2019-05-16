# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""


import logging

from bidict import bidict
import qtawesome as qta
from qtpy import QtCore, QtWidgets

from prettyqt import core, widgets

DOCK_POSITIONS = dict(top=QtCore.Qt.TopDockWidgetArea,
                      bottom=QtCore.Qt.BottomDockWidgetArea,
                      left=QtCore.Qt.LeftDockWidgetArea,
                      right=QtCore.Qt.RightDockWidgetArea)

MODALITIES = bidict(dict(window=QtCore.Qt.WindowModal,
                         application=QtCore.Qt.ApplicationModal,
                         none=QtCore.Qt.NonModal))

TOOLBAR_AREAS = bidict(dict(left=QtCore.Qt.LeftToolBarArea,
                            right=QtCore.Qt.RightToolBarArea,
                            top=QtCore.Qt.TopToolBarArea,
                            bottom=QtCore.Qt.BottomToolBarArea,
                            all=QtCore.Qt.AllToolBarAreas,
                            none=QtCore.Qt.NoToolBarArea))


class MainWindow(QtWidgets.QMainWindow):
    """
    Class for our mainWindow
    includes all docks, a centralwidget and a toolbar
    """

    def __getitem__(self, index):
        return self.findChild(QtWidgets.QWidget, index)

    def add_toolbar(self, toolbar, position):
        """adds a toolbar to the mainmenu at specified area

        Valid values for position: "left", "right", "top", "bottom"

        Args:
            toolbar: toolbar to use
            position: position of the toolbar

        Raises:
            ValueError: position does not exist
        """
        if position not in TOOLBAR_AREAS:
            raise ValueError("Position not existing")
        self.addToolBar(position, TOOLBAR_AREAS[position])

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

    def set_modality(self, modality: str = "window"):
        """set modality for the window

        Valid values for modality: "modeless", "window", "application"

        Args:
            modality: modality for the main window (default: {"window"})

        Raises:
            ValueError: modality type does not exist
        """
        if modality not in MODALITIES:
            raise ValueError("Invalid value for modality.")
        self.setWindowModality(MODALITIES[modality])


MainWindow.__bases__[0].__bases__ = (widgets.Widget,)


if __name__ == "__main__":
    app = widgets.app()
    form = MainWindow()
    form.show()
    app.exec_()
