from __future__ import annotations

from collections.abc import Sequence
import logging

from prettyqt import constants, core, widgets
from prettyqt.qt import QtWidgets
from prettyqt.utils import InvalidParamError


logger = logging.getLogger(__name__)

QtWidgets.QMainWindow.__bases__ = (widgets.Widget,)


class MainWindow(QtWidgets.QMainWindow):
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

    def serialize_fields(self):
        return dict(
            central_widget=self.centralWidget(),
            is_maximized=self.isMaximized(),
        )

    def __setstate__(self, state):
        if state["central_widget"]:
            self.setCentralWidget(state["central_widget"])
        if state["is_maximized"]:
            self.showMaximized()
        self.box = self.layout()

    def __reduce__(self):
        return type(self), (), self.__getstate__()

    def set_widget(self, widget: QtWidgets.QWidget | None):
        if widget is None:
            self.takeCentralWidget()
        else:
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
            menu.add(action)
        menu.add_separator()
        for tb in self.get_toolbars():
            action = widgets.Action(text=tb.windowTitle(), parent=self)
            action.set_checkable(True)
            action.toggled.connect(tb.setVisible)
            action.set_checked(tb.isVisible())
            menu.add(action)
        return menu

    def add_toolbar(
        self, toolbar: QtWidgets.QToolBar, position: constants.ToolbarAreaStr = "top"
    ):
        """Adds a toolbar to the mainmenu at specified area.

        Args:
            toolbar: toolbar to use
            position: position of the toolbar

        Raises:
            InvalidParamError: position does not exist
        """
        if position not in constants.TOOLBAR_AREA:
            raise InvalidParamError(position, constants.TOOLBAR_AREA)
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
        vertical: bool = True,
        position: constants.DockPositionStr = "left",
    ) -> widgets.DockWidget:
        dock_widget = widgets.DockWidget(self, name=name, title=title)
        widget = widgets.Widget()
        widget.set_id(f"{name}.widget")
        layout = widgets.BoxLayout(
            "vertical" if vertical else "horizontal", widget, margin=0
        )
        dock_widget.setWidget(widget)
        self.add_dockwidget(dock_widget, position)
        dock_widget.box = layout
        return dock_widget

    def add_dockwidget(
        self,
        dockwidget: QtWidgets.QDockWidget,
        position: constants.DockPositionStr = "left",
    ):
        self.addDockWidget(constants.DOCK_POSITION[position], dockwidget)

    def remove_dockwidgets(self, dockwidgets: Sequence[QtWidgets.QDockWidget]):
        for i in dockwidgets:
            self.removeDockWidget(i)

    def show_blocking(self):
        self.set_modality("application")
        self.show()

    def get_docks(self) -> list[QtWidgets.QDockWidget]:
        return self.find_children(QtWidgets.QDockWidget, recursive=False)

    def get_toolbars(self) -> list[QtWidgets.QToolBar]:
        return self.find_children(QtWidgets.QToolBar, recursive=False)

    def toggle_fullscreen(self):
        """Toggle between fullscreen and regular size."""
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()


if __name__ == "__main__":
    app = widgets.app()
    form = MainWindow()
    form.show()
    app.main_loop()
