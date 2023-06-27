from __future__ import annotations

import collections
from collections.abc import Sequence
import logging
from typing import Literal

from prettyqt import constants, core, gui, widgets
from prettyqt.utils import bidict, listdelegators


DOCK_OPTION = bidict(
    animated_docks=widgets.QMainWindow.DockOption.AnimatedDocks,
    allow_nested_docks=widgets.QMainWindow.DockOption.AllowNestedDocks,
    allow_tabbed_docks=widgets.QMainWindow.DockOption.AllowTabbedDocks,
    force_tabbed_docks=widgets.QMainWindow.DockOption.ForceTabbedDocks,
    vertical_tabs=widgets.QMainWindow.DockOption.VerticalTabs,
    grouped_dragging=widgets.QMainWindow.DockOption.GroupedDragging,
)

DockOptionStr = Literal[
    "animated_docks",
    "allow_nested_docks",
    "allow_tabbed_docks",
    "force_tabbed_docks",
    "vertical_tabs",
    "grouped_dragging",
]

DEFAULT_OPTS = (
    widgets.QMainWindow.DockOption.AllowTabbedDocks
    | widgets.QMainWindow.DockOption.AllowNestedDocks
    | widgets.QMainWindow.DockOption.GroupedDragging
    | widgets.QMainWindow.DockOption.AnimatedDocks
)

logger = logging.getLogger(__name__)


class PopupMenuAction(gui.Action):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.triggered.connect(self._show_menu)
        self._mainwindow: MainWindow = self.parent()  # type: ignore

    def _show_menu(self):
        menu = self._mainwindow.createPopupMenu()
        self.setMenu(menu)
        menu.exec(gui.Cursor.pos())


class FullScreenAction(gui.Action):
    def __init__(
        self,
        parent: widgets.MainWindow,
        text: str = "Fullscreen",
        shortcut: str = "F11",
    ):
        super().__init__(
            text=text,
            # icon="mdi.fullscreen",
            checkable=True,
            shortcut=shortcut,
            parent=parent,
            checked=parent.isFullScreen(),
        )
        self.triggered.connect(parent.toggle_fullscreen)
        parent.installEventFilter(self)

    def eventFilter(self, source, event):
        """Needed to adjust checkstate when windowstate changes programatically."""
        if event.type() == core.Event.Type.WindowStateChange:
            self.setChecked(source.isFullScreen())
        return False


class MainWindow(widgets.WidgetMixin, widgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, dock_options=DEFAULT_OPTS, **kwargs)
        self.setMenuBar(widgets.MenuBar())

    def __getitem__(self, index: str) -> widgets.QWidget:
        result = self.find_child(widgets.QWidget, index)
        if result is None:
            raise KeyError("Widget not found")
        return result

    def _get_map(self):
        maps = super()._get_map()
        maps |= {
            "toolButtonStyle": constants.TOOLBUTTON_STYLE,
            "tabShape": widgets.tabwidget.TAB_SHAPES,
        }
        return maps

    def set_widget(self, widget: widgets.QWidget | None) -> widgets.QWidget | None:
        """Set widget and return previous one if existing."""
        previous = self.takeCentralWidget()
        if widget:
            self.setCentralWidget(widget)
        return previous

    def createPopupMenu(self) -> widgets.Menu:
        menu = widgets.Menu(parent=self, title="Window")
        for i, item in enumerate(self.get_docks()):
            action = gui.Action(
                text=item.windowTitle(),
                parent=self,
                checkable=True,
                checked=item.isVisible(),
                shortcut=f"Ctrl+Shift+{i}",
                shortcut_context="application",
                toggled=item.setVisible,
            )
            menu.add(action)
        menu.add_separator()
        for tb in self.get_toolbars():
            action = gui.Action(
                text=tb.windowTitle(),
                parent=self,
                checkable=True,
                toggled=tb.setVisible,
                checked=tb.isVisible(),
            )
            menu.add(action)
        return menu

    def add(self, widget: widgets.QWidget, **kwargs):
        match widget:
            case widgets.QToolBar():
                self.add_toolbar(widget, **kwargs)
            case widgets.QDockWidget():
                self.add_dockwidget(widget, **kwargs)
            case widgets.QWidget():
                self.centralWidget().layout().add(widget, **kwargs)

    def get_corner(
        self, corner: constants.CornerStr | constants.Corner
    ) -> constants.DockWidgetAreaStr:
        corner_flag = constants.CORNER.get_enum_value(corner)
        area = self.corner(corner_flag)
        return constants.DOCK_WIDGET_AREAS.inverse[area]

    def set_corner(
        self,
        corner: constants.CornerStr | constants.Corner,
        area: constants.DockWidgetAreaStr | constants.DockWidgetArea,
    ):
        corner_flag = constants.CORNER.get_enum_value(corner)
        area_flag = constants.DOCK_WIDGET_AREAS.get_enum_value(area)
        self.setCorner(corner_flag, area_flag)

    def add_toolbar(
        self,
        toolbar: widgets.QToolBar,
        area: constants.ToolbarAreaStr | constants.ToolBarArea | Literal["auto"] = "auto",
    ):
        """Adds a toolbar to the mainmenu at specified area.

        Args:
            toolbar: toolbar to use
            area: area of the toolbar
        """
        if area == "auto":
            area = self._get_preferred_toolbar_position()
        self.addToolBar(constants.TOOLBAR_AREA.get_enum_value(area), toolbar)

    def add_toolbar_break(
        self, position: constants.ToolbarAreaStr | constants.ToolBarArea = "top"
    ):
        """Adds a toolbar break to the given area behind the last item.

        Args:
            position: position of the toolbar
        """
        self.addToolBarBreak(constants.TOOLBAR_AREA.get_enum_value(position))

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
        layout: widgets.layout.LayoutTypeStr | widgets.QLayout = "horizontal",
        position: constants.DockWidgetAreaStr | constants.DockWidgetArea = "left",
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
        widget: widgets.QWidget,
        position: constants.DockWidgetAreaStr
        | constants.DockWidgetArea
        | Literal["auto"] = "auto",
        **kwargs,
    ):
        if position == "auto":
            position = self._get_preferred_dock_position()
        if not isinstance(widget, widgets.QDockWidget):
            dock_widget = widgets.DockWidget(self, **kwargs)
            dock_widget.set_widget(widget)
            self.addDockWidget(
                constants.DOCK_WIDGET_AREA.get_enum_value(position), dock_widget
            )
            return dock_widget
        else:
            self.addDockWidget(
                constants.DOCK_WIDGET_AREA.get_enum_value(position), widget
            )

    def remove(
        self,
        widgets: Sequence[widgets.QDockWidget | widgets.QToolBar | gui.QAction]
        | widgets.QDockWidget
        | widgets.QToolBar
        | gui.QAction,
    ):
        widget_list = widgets if isinstance(widgets, list) else [widgets]
        for i in widget_list:
            match i:
                case widgets.QDockWidget():
                    self.removeDockWidget(i)
                case widgets.QToolBar():
                    self.removeToolBar(i)
                case gui.QAction():
                    self.removeAction(i)

    def show_blocking(self):
        self.set_modality("application")
        self.show()

    def get_dock_area(self, widget: widgets.QDockWidget) -> constants.DockWidgetAreaStr:
        area = self.dockWidgetArea(widget)
        return constants.DOCK_WIDGET_AREAS.inverse[area]

    def get_toolbar_area(self, widget: widgets.QToolBar) -> constants.ToolbarAreaStr:
        area = self.toolBarArea(widget)
        return constants.TOOLBAR_AREA.inverse[area]

    def set_tool_button_style(
        self, style: constants.ToolButtonStyleStr | constants.ToolButtonStyle
    ):
        self.setToolButtonStyle(constants.TOOLBUTTON_STYLE.get_enum_value(style))

    def get_tool_button_style(self) -> constants.ToolButtonStyleStr:
        """Return current tool button style.

        Returns:
            tool button style
        """
        return constants.TOOLBUTTON_STYLE.inverse[self.toolButtonStyle()]

    def set_tab_shape(
        self, shape: widgets.tabwidget.TabShapeStr | widgets.QTabWidget.TabShape
    ):
        """Set tab shape for the tabwidget.

        Args:
            shape: tab shape to use
        """
        self.setTabShape(widgets.tabwidget.TAB_SHAPES.get_enum_value(shape))

    def get_tab_shape(self) -> widgets.tabwidget.TabShapeStr:
        """Return tab shape.

        Returns:
            tab shape
        """
        return widgets.tabwidget.TAB_SHAPES.inverse[self.tabShape()]

    def get_docks(
        self, position: constants.DockWidgetAreaStr | None = None
    ) -> listdelegators.BaseListDelegator[widgets.QDockWidget]:
        docks = self.find_children(widgets.QDockWidget, recursive=False)
        if position is None:
            return docks
        else:
            return [i for i in docks if self.get_dock_area(i) == position]

    def _get_preferred_dock_position(
        self,
        preference: constants.DockWidgetAreaStr = "left",
    ) -> constants.DockWidgetAreaStr:
        """Get location with least amount of docks. If same score, use preference."""
        areas = [self.get_dock_area(i) for i in self.get_docks()]
        # by prepending the prio order, we can choose order because
        # collections.Counter takes insertion order into account.
        positions = ["bottom", "top", "right", "left"]
        positions.remove(preference)
        positions.append(preference)
        counter = collections.Counter(positions + areas)  # type: ignore[operator]
        return counter.most_common()[-1][0]  # type: ignore[return-value]

    def _get_preferred_toolbar_position(
        self,
        preference: constants.ToolbarAreaStr = "top",
    ) -> constants.ToolbarAreaStr:
        """See _get_preferred_dock_position."""
        areas = [self.get_toolbar_area(i) for i in self.get_toolbars()]
        positions = ["right", "left", "bottom", "top"]
        positions.remove(preference)
        positions.append(preference)
        counter = collections.Counter(positions + areas)  # type: ignore[operator]
        return counter.most_common()[-1][0]  # type: ignore[return-value]

    def get_toolbars(
        self, position: constants.ToolbarAreaStr | None = None
    ) -> listdelegators.BaseListDelegator[widgets.QToolBar]:
        toolbars = self.find_children(widgets.QToolBar, recursive=False)
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
    action = FullScreenAction(parent=form)
    menu = widgets.Menu("test")
    menu.add_action(action)
    form.menuBar().add_menu(menu)
    form.show()
    app.exec()
