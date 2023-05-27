from __future__ import annotations

import collections
from collections.abc import Sequence
import logging
from typing import Literal

from prettyqt import constants, core, gui, widgets
from prettyqt.qt import QtGui, QtWidgets
from prettyqt.utils import InvalidParamError


logger = logging.getLogger(__name__)


class MainWindow(widgets.WidgetMixin, QtWidgets.QMainWindow):
    """Class for our mainWindow.

    Includes all docks, a centralwidget and a toolbar
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMenuBar(widgets.MenuBar())
        self.setDockOptions(
            self.DockOption.AllowTabbedDocks  # type: ignore
            | self.DockOption.AllowNestedDocks
            | self.DockOption.GroupedDragging
            | self.DockOption.AnimatedDocks
        )

    def __getitem__(self, index: str) -> QtWidgets.QWidget:
        result = self.find_child(QtWidgets.QWidget, index)
        if result is None:
            raise KeyError("Widget not found")
        return result

    def set_widget(self, widget: QtWidgets.QWidget | None) -> QtWidgets.QWidget | None:
        """Set widget and return previous one if existing."""
        previous = self.takeCentralWidget()
        if widget:
            self.setCentralWidget(widget)
        return previous

    def createPopupMenu(self) -> widgets.Menu:
        # qactions = self.createPopupMenu()
        menu = widgets.Menu(parent=self)
        for i, item in enumerate(self.get_docks()):
            action = gui.Action(text=item.windowTitle(), parent=self)
            action.set_checkable(True)
            action.set_checked(item.isVisible())
            action.set_shortcut(f"Ctrl+Shift+{i}")
            action.set_shortcut_context("application")
            action.toggled.connect(item.setVisible)
            menu.add(action)
        menu.add_separator()
        for tb in self.get_toolbars():
            action = gui.Action(text=tb.windowTitle(), parent=self)
            action.set_checkable(True)
            action.toggled.connect(tb.setVisible)
            action.set_checked(tb.isVisible())
            menu.add(action)
        return menu

    def add(self, widget: QtWidgets.QWidget, **kwargs):
        match widget:
            case QtWidgets.QToolBar():
                self.add_toolbar(widget, **kwargs)
            case QtWidgets.QDockWidget():
                self.add_dockwidget(widget, **kwargs)
            case QtWidgets.QWidget():
                self.centralWidget().layout().add(widget, **kwargs)

    def add_toolbar(
        self,
        toolbar: QtWidgets.QToolBar,
        position: constants.ToolbarAreaStr | Literal["auto"] = "auto",
    ):
        """Adds a toolbar to the mainmenu at specified area.

        Args:
            toolbar: toolbar to use
            position: position of the toolbar
        """
        if position == "auto":
            position = self._get_preferred_toolbar_position()
        self.addToolBar(constants.TOOLBAR_AREA[position], toolbar)

    def add_toolbar_break(self, position: constants.ToolbarAreaStr = "top"):
        """Adds a toolbar break to the given area behind the last item.

        Args:
            position: position of the toolbar

        Raises:
            InvalidParamError: position does not exist
        """
        if position not in constants.TOOLBAR_AREA:
            raise InvalidParamError(position, constants.TOOLBAR_AREA)
        self.addToolBarBreak(constants.TOOLBAR_AREA[position])

    def load_window_state(self, recursive: bool = False) -> bool:
        settings = core.Settings()
        name = self.get_id()
        geom = settings.get(f"{name}.geometry")
        state = settings.get(f"{name}.state")
        restored = False
        if geom is not None and state is not None:
            try:
                logger.debug(f"Loading window state for {self.windowTitle()!r}...")
                self.restoreGeometry(geom)
                if isinstance(state, str):
                    state = state.encode()
                self.restoreState(state)
                restored = True
            except TypeError:
                logger.error("Wrong type for window state. Probably Qt binding switch?")
        if recursive:
            for window in self.find_children(MainWindow, recursive=True):
                if window.get_id():
                    window.load_window_state()
        return restored

    def save_window_state(self, recursive: bool = False):
        """Save current window state as QSetting.

        Args:
            recursive (bool, optional): Description
        """
        settings = core.Settings()
        name = self.get_id()
        logger.debug(f"Saving window state for {self.windowTitle()!r}...")
        settings[f"{name}.geometry"] = self.saveGeometry()
        settings[f"{name}.state"] = self.saveState()
        if recursive:
            for window in self.find_children(MainWindow, recursive=True):
                if window.get_id():
                    window.save_window_state()

    def add_widget_as_dock(
        self,
        name: str,
        title: str,
        layout: widgets.layout.LayoutTypeStr = "horizontal",
        position: constants.DockPositionStr = "left",
    ) -> widgets.DockWidget:
        dock_widget = widgets.DockWidget(self, object_name=name, window_title=title)
        widget = widgets.Widget()
        widget.set_id(f"{name}.widget")
        widget.set_layout(layout, margin=0)
        dock_widget.setWidget(widget)
        self.add_dockwidget(dock_widget, position)
        return dock_widget

    def add_dockwidget(
        self,
        widget: QtWidgets.QtWidgets.QWidget,
        position: constants.DockPositionStr | Literal["auto"] = "auto",
        **kwargs,
    ):
        if position == "auto":
            position = self._get_preferred_dock_position()
        if not isinstance(widget, QtWidgets.QDockWidget):
            dock_widget = widgets.DockWidget(self, **kwargs)
            dock_widget.set_widget(widget)
            self.addDockWidget(constants.DOCK_POSITION[position], dock_widget)
            return dock_widget
        else:
            self.addDockWidget(constants.DOCK_POSITION[position], widget)

    def remove(
        self,
        widgets: Sequence[QtWidgets.QDockWidget | QtWidgets.QToolbar | QtGui.QAction]
        | QtWidgets.QDockWidget
        | QtWidgets.QToolbar
        | QtGui.QAction,
    ):
        if not isinstance(widgets, list):
            widgets = [widgets]
        for i in widgets:
            match i:
                case QtWidgets.QDockWidget():
                    self.removeDockWidget(i)
                case QtWidgets.QToolBar():
                    self.removeToolBar(i)
                case QtGui.QAction():
                    self.removeAction(i)

    def show_blocking(self):
        self.set_modality("application")
        self.show()

    def get_dock_area(self, widget: QtWidgets.QDockWidget) -> constants.DockPositionStr:
        area = self.dockWidgetArea(widget)
        return constants.DOCK_POSITIONS.inverse[area]

    def get_toolbar_area(self, widget: QtWidgets.QToolBar) -> constants.ToolbarAreaStr:
        area = self.toolBarArea(widget)
        return constants.TOOLBAR_AREA.inverse[area]

    def get_docks(
        self, position: constants.DockPositionStr | None = None
    ) -> list[QtWidgets.QDockWidget]:
        docks = self.find_children(QtWidgets.QDockWidget, recursive=False)
        if position is None:
            return docks
        else:
            return [i for i in docks if self.get_dock_area(i) == position]

    def _get_preferred_dock_position(
        self,
        preference: constants.DockPositionStr = "left",
    ) -> constants.DockPositionStr:
        """Get location with least amount of docks. If same score, use preference."""
        areas = [self.get_dock_area(i) for i in self.get_docks()]
        # by prepending the prio order, we can choose order because
        # collections.Counter takes insertion order into account.
        positions = ["bottom", "top", "right", "left"]
        positions.remove(preference)
        positions.append(preference)
        counter = collections.Counter(positions + areas)
        return counter.most_common()[-1][0]

    def _get_preferred_toolbar_position(
        self,
        preference: constants.ToolbarAreaStr = "top",
    ) -> constants.ToolbarAreaStr:
        """See _get_preferred_dock_position."""
        areas = [self.get_toolbar_area(i) for i in self.get_toolbars()]
        positions = ["right", "left", "bottom", "top"]
        positions.remove(preference)
        positions.append(preference)
        counter = collections.Counter(positions + areas)
        return counter.most_common()[-1][0]

    def get_toolbars(
        self, position: constants.ToolbarAreaStr | None = None
    ) -> list[QtWidgets.QToolBar]:
        toolbars = self.find_children(QtWidgets.QToolBar, recursive=False)
        if position is None:
            return toolbars
        else:
            return [i for i in toolbars if self.get_toolbar_area(i) == position]


if __name__ == "__main__":
    app = widgets.app()
    form = MainWindow()
    dock = form.add_dockwidget(widgets.Widget())
    dock = form.add_dockwidget(widgets.Widget())
    dock = form.add_dockwidget(widgets.Widget())
    dock = form.add_dockwidget(widgets.Widget())
    print(dock.get_current_area())
    form.show()
    app.main_loop()
