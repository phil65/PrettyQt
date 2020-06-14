# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

import logging
from typing import Union

import qtawesome as qta
from qtpy import QtCore, QtGui, QtWidgets

from prettyqt import core, gui, widgets
from prettyqt.utils import bidict

DOCK_POSITIONS = bidict(top=QtCore.Qt.TopDockWidgetArea,
                        bottom=QtCore.Qt.BottomDockWidgetArea,
                        left=QtCore.Qt.LeftDockWidgetArea,
                        right=QtCore.Qt.RightDockWidgetArea)

TOOLBAR_AREAS = bidict(left=QtCore.Qt.LeftToolBarArea,
                       right=QtCore.Qt.RightToolBarArea,
                       top=QtCore.Qt.TopToolBarArea,
                       bottom=QtCore.Qt.BottomToolBarArea,
                       all=QtCore.Qt.AllToolBarAreas,
                       none=QtCore.Qt.NoToolBarArea)


QtWidgets.QMainWindow.__bases__ = (widgets.Widget,)


class MainWindow(QtWidgets.QMainWindow):
    """
    Class for our mainWindow
    includes all docks, a centralwidget and a toolbar
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setDockOptions(self.AllowTabbedDocks |
                            self.AllowNestedDocks |
                            self.GroupedDragging |
                            self.AnimatedDocks)

    def __getitem__(self, index):
        return self.findChild(QtWidgets.QWidget, index)

    def __getstate__(self):
        icon = gui.Icon(self.windowIcon())
        return dict(central_widget=self.centralWidget(),
                    title=self.windowTitle(),
                    is_maximized=self.isMaximized(),
                    icon=icon if not icon.isNull() else None,
                    size=(self.size().width(), self.size().height()))

    def __setstate__(self, state):
        self.__init__()
        self.title = state["title"]
        self.set_icon(state["icon"])
        if state["central_widget"]:
            self.setCentralWidget(state["central_widget"])
        self.resize(state["size"])
        if state["is_maximized"]:
            self.showMaximized()
        self.resize(*state["size"])
        self.box = self.layout()

    def set_widget(self, widget):
        self.setCentralWidget(widget)

    def createPopupMenu(self):
        # qactions = self.createPopupMenu()
        menu = widgets.Menu(parent=self)
        for i, item in enumerate(self.get_docks()):
            action = widgets.Action(text=item.windowTitle(), parent=self)
            action.set_checkable(True)
            action.set_checked(item.isVisible())
            action.set_shortcut(f"Ctrl+Shift+{i}")
            action.set_shortcut_context("application")
            action.toggled.connect(item.setVisible)
            menu.add_action(action)
        menu.add_separator()
        for i in self.get_toolbars():
            action = widgets.Action(text=i.windowTitle(), parent=self)
            action.set_checkable(True)
            action.toggled.connect(i.setVisible)
            action.set_checked(i.isVisible())
            menu.add_action(action)
        return menu

    def add_toolbar(self, toolbar, position: str = "top"):
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
        self.addToolBar(TOOLBAR_AREAS[position], toolbar)

    def add_toolbar_break(self, position: str = "top"):
        """Adds a toolbar break to the given area
        after all the other objects that are present.

        Valid values for position: "left", "right", "top", "bottom"

        Args:
            position: position of the toolbar

        Raises:
            ValueError: position does not exist
        """
        if position not in TOOLBAR_AREAS:
            raise ValueError("Position not existing")
        self.addToolBarBreak(TOOLBAR_AREAS[position])

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

    def set_icon(self, icon: Union[QtGui.QIcon, str, None]):
        """set the icon for the menu

        Args:
            icon: icon to use
        """
        if not icon:
            icon = gui.Icon()
        elif isinstance(icon, str):
            icon = qta.icon(icon, color="lightgray")
        self.setWindowIcon(icon)

    def add_widget_as_dock(self,
                           name: str,
                           title: str,
                           vertical: bool = True,
                           position: str = "left") -> widgets.DockWidget:
        dock_widget = widgets.DockWidget(self, name=name, title=title)
        widget = widgets.Widget()
        widget.id = f"{name}.widget"
        orientation = "vertical" if vertical else "horizontal"
        layout = widgets.BoxLayout(orientation, widget, margin=0)
        dock_widget.setWidget(widget)
        self.add_dockwidget(dock_widget, position)
        dock_widget.box = layout
        return dock_widget

    def add_dockwidget(self, dockwidget, position: str = "left"):
        position = DOCK_POSITIONS[position]
        self.addDockWidget(QtCore.Qt.DockWidgetArea(position), dockwidget)

    def remove_dockwidgets(self, dockwidgets: list):
        for i in dockwidgets:
            self.removeDockWidget(i)

    def get_docks(self) -> list:
        return self.find_children(QtWidgets.QDockWidget, recursive=False)

    def get_toolbars(self) -> list:
        return self.find_children(QtWidgets.QToolBar, recursive=False)

    def toggle_fullscreen(self):
        """toggle between fullscreen and regular size
        """
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()


if __name__ == "__main__":
    app = widgets.app()
    form = MainWindow()
    form.show()
    app.exec_()
