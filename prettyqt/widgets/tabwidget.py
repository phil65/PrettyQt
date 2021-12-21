from __future__ import annotations

from typing import Literal

from prettyqt import core, gui, iconprovider, widgets
from prettyqt.qt import QtCore, QtGui, QtWidgets
from prettyqt.utils import InvalidParamError, bidict, types


TAB_SHAPES = bidict(
    rounded=QtWidgets.QTabWidget.TabShape.Rounded,
    triangular=QtWidgets.QTabWidget.TabShape.Triangular,
)

TabShapeStr = Literal["rounded", "triangular"]

TAB_POSITION = bidict(
    north=QtWidgets.QTabWidget.TabPosition.North,
    south=QtWidgets.QTabWidget.TabPosition.South,
    west=QtWidgets.QTabWidget.TabPosition.West,
    east=QtWidgets.QTabWidget.TabPosition.East,
)

TabPositionStr = Literal["north", "south", "west", "east"]

QtWidgets.QTabWidget.__bases__ = (widgets.Widget,)


class TabWidget(QtWidgets.QTabWidget):
    """Widget for managing the tabs section."""

    def __init__(
        self,
        parent: QtWidgets.QWidget | None = None,
        closable: bool = False,
        detachable: bool = False,
    ) -> None:

        # Basic initalization
        super().__init__(parent)
        self.tabCloseRequested.connect(self.remove_tab)
        self.tab_bar = widgets.TabBar(self)

        self.setTabBar(self.tab_bar)

        # Used to keep a reference to detached tabs since their QMainWindow
        # does not have a parent
        self.detached_tabs: dict[str, DetachedTab] = {}
        if detachable:
            self.set_detachable()
        self.set_closable(closable)

    def __len__(self) -> int:
        return self.count()

    def __getitem__(self, index: int) -> QtWidgets.QWidget:
        if isinstance(index, int):
            return self.widget(index)
        else:
            result = self.findChild(QtWidgets.QWidget, index)
            if result is None:
                raise KeyError("Widget not found")
            return result

    def __contains__(self, item: QtWidgets.QWidget):
        return self.indexOf(item) >= 0

    def serialize_fields(self):
        return dict(
            tabbar=self.tabBar(),
            widgets=self.get_children(),
            movable=self.isMovable(),
            document_mode=self.documentMode(),
            current_index=self.currentIndex(),
            tab_shape=self.get_tab_shape(),
            # elide_mode=self.get_elide_mode(),
            icon_size=self.iconSize(),
            tab_position=self.get_tab_position(),
        )

    def __setstate__(self, state):
        super().__setstate__(state)
        self.setTabBar(state["tabbar"])
        self.setDocumentMode(state.get("document_mode", False))
        self.setMovable(state.get("movable", False))
        self.set_tab_shape(state.get("tab_shape", "rounded"))
        self.setIconSize(state["icon_size"])
        for (widget, name, icon, tooltip, whatsthis) in state["widgets"]:
            i = self.add_tab(widget, name, icon)
            self.setTabToolTip(i, tooltip)
            self.setTabWhatsThis(i, whatsthis)
        self.setCurrentIndex(state.get("index", 0))

    def __reduce__(self):
        return type(self), (), self.__getstate__()

    def update_tab_bar_visibility(self):
        """Update visibility of the tabBar depending of the number of tabs.

        0 or 1 tab -> tabBar hidden, 2+ tabs - >tabBar visible
        need to be called explicitly, or be connected to tabInserted/tabRemoved
        """
        self.tabBar().setVisible(self.count() > 1)

    def set_icon_size(self, size: int | types.SizeType):
        """Set size of the icons."""
        if isinstance(size, int):
            size = core.Size(size, size)
        elif isinstance(size, tuple):
            size = core.Size(*size)
        self.setIconSize(size)

    def set_document_mode(self, state: bool = True) -> None:
        self.setDocumentMode(state)

    def set_tab_shape(self, shape: TabShapeStr):
        """Set tab shape for the tabwidget.

        Args:
            shape: tab shape to use

        Raises:
            InvalidParamError: tab shape does not exist
        """
        if shape not in TAB_SHAPES:
            raise InvalidParamError(shape, TAB_SHAPES)
        self.setTabShape(TAB_SHAPES[shape])

    def get_tab_shape(self) -> TabShapeStr:
        """Return tab shape.

        Returns:
            tab shape
        """
        return TAB_SHAPES.inverse[self.tabShape()]

    def set_tab_position(self, position: TabPositionStr):
        """Set tab position for the tabwidget.

        Args:
            position: tab position to use

        Raises:
            InvalidParamError: tab position does not exist
        """
        if position not in TAB_POSITION:
            raise InvalidParamError(position, TAB_POSITION)
        self.setTabPosition(TAB_POSITION[position])

    def get_tab_position(self) -> TabPositionStr:
        """Return tab position.

        Returns:
            tab position
        """
        return TAB_POSITION.inverse[self.tabPosition()]

    def get_children(self) -> list[tuple]:
        return [
            (
                self.widget(i),
                self.tabText(i),
                self.tab_icon(i),
                self.tabToolTip(i),
                self.tabWhatsThis(i),
            )
            for i in range(self.count())
        ]

    def tab_icon(self, i: int) -> gui.Icon | None:
        icon = self.tabIcon(i)
        if icon.isNull():
            return None
        return gui.Icon(icon)

    def set_detachable(self):
        self.tab_bar.on_detach.connect(self.detach_tab)
        core.CoreApplication.call_on_exit(self.close_detached_tabs)
        self.setMovable(True)

    def set_closable(self, closable: bool = True):
        self.setTabsClosable(closable)

    @core.Slot(int, QtCore.QPoint)
    def detach_tab(self, index: int, point: types.PointType):
        """Detach tab by removing its contents and placing them in a DetachedTab window.

        Args:
            index (int): index location of the tab to be detached
            point (QtCore.QPoint): screen pos for creating the new DetachedTab window

        Returns:
            None: Description
        """
        # Get the tab content
        if isinstance(point, tuple):
            point = QtCore.QPoint(*point)
        name = self.tabText(index)
        icon = self.tab_icon(index)
        if icon is None:
            icon = self.window().windowIcon()
        widget = self.widget(index)

        try:
            widget_rect = widget.frameGeometry()
        except AttributeError:
            return

        # Create a new detached tab window
        detached_tab = DetachedTab(name, widget)
        detached_tab.set_modality("none")
        detached_tab.set_icon(icon)
        detached_tab.setGeometry(widget_rect)
        detached_tab.on_close.connect(self.attach_tab)
        detached_tab.move(point)
        detached_tab.show()

        # Create a reference to maintain access to the detached tab
        self.detached_tabs[name] = detached_tab

    def add_tab(
        self,
        item: QtWidgets.QWidget | QtWidgets.QLayout,
        label: str,
        icon: types.IconType = None,
        position: int | None = None,
        show: bool = False,
    ) -> int:
        if isinstance(item, QtWidgets.QLayout):
            widget = widgets.Widget()
            widget.set_layout(item)
        else:
            widget = item
        if position is None:
            position = len(self)
        if not icon:
            index = self.insertTab(position, widget, label)
        else:
            icon = iconprovider.get_icon(icon)
            index = self.insertTab(position, widget, icon, label)
        if show:
            self.setCurrentIndex(index)
        return index

    def attach_tab(
        self,
        widget: QtWidgets.QWidget | QtWidgets.QLayout,
        name: str,
        icon: types.IconType = None,
        insert_at: int | None = None,
    ):
        """Re-attach tab.

        Re-attach the tab by removing the content from the DetachedTab window,
        closing it, and placing the content back into the DetachableTabWidget.

        Args:
            widget (Union[QtWidgets.QWidget, QtWidgets.QLayout]): the content widget
                from the DetachedTab window
            name (str): the name of the detached tab
            icon (types.IconType, optional): the window icon for the detached tab
            insert_at (Optional[int], optional): insert the re-attached tab at the
                given index
        """
        widget.setParent(self)

        # Remove the reference
        del self.detached_tabs[name]

        # Determine if the given image and the main window icon are the same.
        # If they are, then do not add the icon to the tab
        self.add_tab(widget, name, icon=icon, position=insert_at, show=True)

    def close_detached_tabs(self):
        """Close all tabs that are currently detached."""
        tabs = list(self.detached_tabs.values())
        for tab in tabs:
            tab.close()

    @core.Slot(int)
    def remove_tab(self, index: int):
        widget = self.widget(index)
        self.removeTab(index)
        if widget is not None:
            widget.deleteLater()

    @core.Slot(QtWidgets.QWidget, str)
    def open_widget(self, widget: QtWidgets.QWidget, title: str = "Unnamed"):
        """Create a tab containing delivered widget."""
        self.add_tab(widget, title, icon="mdi.widgets", show=True)

    def set_tab(self, index: int, position: str, widget: QtWidgets.QWidget | None = None):
        self.tabBar().set_tab(index, position, widget)


class DetachedTab(widgets.MainWindow):
    """Window containing a detached tab.

    When a tab is detached, the contents are placed into this QMainWindow.
    The tab can be re-attached by closing the dialog

    Attributes:
        on_close: signal, emitted when window is closed (widget, title, icon)
    """

    on_close = core.Signal(QtWidgets.QWidget, str, QtGui.QIcon)

    def __init__(self, name: str, widget: QtWidgets.QWidget):
        super().__init__(None)

        self.set_id(name)
        self.set_title(name)

        self.widget = widget
        self.setCentralWidget(self.widget)
        self.widget.show()

    #  If the window is closed, emit the on_close and give the
    #  content widget back to the DetachableTabWidget
    def closeEvent(self, event):
        self.on_close.emit(self.widget, self.get_id(), self.windowIcon())


if __name__ == "__main__":
    app = widgets.app()
    tab_widget = TabWidget()
    widget = widgets.Widget()
    tab_widget.add_tab(widget, "Test")
    widget_2 = widgets.Widget()
    tab_widget.add_tab(widget_2, "Test 2")
    tab_widget.show()
    app.main_loop()
