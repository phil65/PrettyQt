# -*- coding: utf-8 -*-
"""
"""

from typing import List
import logging

from qtpy import QtCore, QtWidgets

from prettyqt import core, gui, widgets
from prettyqt.utils import bidict


DOCK_POSITIONS = bidict(
    top=QtCore.Qt.TopDockWidgetArea,
    bottom=QtCore.Qt.BottomDockWidgetArea,
    left=QtCore.Qt.LeftDockWidgetArea,
    right=QtCore.Qt.RightDockWidgetArea,
)

TOOLBAR_AREAS = bidict(
    left=QtCore.Qt.LeftToolBarArea,
    right=QtCore.Qt.RightToolBarArea,
    top=QtCore.Qt.TopToolBarArea,
    bottom=QtCore.Qt.BottomToolBarArea,
    all=QtCore.Qt.AllToolBarAreas,
    none=QtCore.Qt.NoToolBarArea,
)

logger = logging.getLogger(__name__)

QtWidgets.QMainWindow.__bases__ = (widgets.Widget,)


class MainWindow(QtWidgets.QMainWindow):
    """
    Class for our mainWindow
    includes all docks, a centralwidget and a toolbar
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setDockOptions(
            self.AllowTabbedDocks
            | self.AllowNestedDocks
            | self.GroupedDragging
            | self.AnimatedDocks
        )

    def __getitem__(self, index):
        return self.findChild(QtWidgets.QWidget, index)

    def __getstate__(self):
        icon = gui.Icon(self.windowIcon())
        return dict(
            central_widget=self.centralWidget(),
            title=self.windowTitle(),
            is_maximized=self.isMaximized(),
            icon=icon if not icon.isNull() else None,
            size=(self.size().width(), self.size().height()),
        )

    def __setstate__(self, state):
        self.__init__()
        self.set_title(state["title"])
        self.set_icon(state["icon"])
        if state["central_widget"]:
            self.setCentralWidget(state["central_widget"])
        self.resize(state["size"])
        if state["is_maximized"]:
            self.showMaximized()
        self.resize(*state["size"])
        self.box = self.layout()

    def set_widget(self, widget: QtWidgets.QWidget):
        self.setCentralWidget(widget)

    def createPopupMenu(self) -> widgets.Menu:
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
        for tb in self.get_toolbars():
            action = widgets.Action(text=tb.windowTitle(), parent=self)
            action.set_checkable(True)
            action.toggled.connect(tb.setVisible)
            action.set_checked(tb.isVisible())
            menu.add_action(action)
        return menu

    def add_toolbar(self, toolbar: QtWidgets.QToolBar, position: str = "top"):
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

    def load_window_state(self, recursive=False) -> bool:
        settings = core.Settings()
        name = self.get_id()
        geom = settings.get(f"{name}.geometry")
        state = settings.get(f"{name}.state")
        restored = False
        if geom is not None and state is not None:
            try:
                logger.debug(f"Loading window state for {name}...")
                self.restoreGeometry(geom)
                self.restoreState(state)
                restored = True
            except TypeError:
                logger.error("Wrong type for window state. Probably Qt binding switch?")
        if recursive:
            for window in self.find_children(MainWindow, recursive=True):
                if window.get_id():
                    window.load_window_state()
        return restored

    def save_window_state(self, recursive=False):
        """
        override, gets executed when app gets closed.
        saves GUI settings
        """
        settings = core.Settings()
        name = self.get_id()
        logger.debug(f"Saving window state for {name}...")
        settings[f"{name}.geometry"] = self.saveGeometry()
        settings[f"{name}.state"] = self.saveState()
        if recursive:
            for window in self.find_children(MainWindow, recursive=True):
                if window.get_id():
                    window.save_window_state()

    def add_widget_as_dock(
        self, name: str, title: str, vertical: bool = True, position: str = "left"
    ) -> widgets.DockWidget:
        dock_widget = widgets.DockWidget(self, name=name, title=title)
        widget = widgets.Widget()
        widget.set_id(f"{name}.widget")
        orientation = "vertical" if vertical else "horizontal"
        layout = widgets.BoxLayout(orientation, widget, margin=0)
        dock_widget.setWidget(widget)
        self.add_dockwidget(dock_widget, position)
        dock_widget.box = layout
        return dock_widget

    def add_dockwidget(self, dockwidget, position: str = "left"):
        position = DOCK_POSITIONS[position]
        self.addDockWidget(QtCore.Qt.DockWidgetArea(position), dockwidget)

    def remove_dockwidgets(self, dockwidgets: List[QtWidgets.QDockWidget]):
        for i in dockwidgets:
            self.removeDockWidget(i)

    def show_blocking(self):
        self.set_modality("application")
        self.show()

    def get_docks(self) -> List[QtWidgets.QDockWidget]:
        return self.find_children(QtWidgets.QDockWidget, recursive=False)

    def get_toolbars(self) -> List[QtWidgets.QToolBar]:
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
