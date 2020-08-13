# -*- coding: utf-8 -*-

from typing import Union, Optional, Dict

from qtpy import QtCore, QtGui, QtWidgets

from prettyqt import core, gui, widgets
from prettyqt.utils import bidict, InvalidParamError, autoslot


TAB_SHAPES = bidict(
    rounded=QtWidgets.QTabWidget.Rounded, triangular=QtWidgets.QTabWidget.Triangular
)

TAB_POSITIONS = bidict(
    north=QtWidgets.QTabWidget.North,
    south=QtWidgets.QTabWidget.South,
    west=QtWidgets.QTabWidget.West,
    east=QtWidgets.QTabWidget.East,
)

QtWidgets.QTabWidget.__bases__ = (widgets.Widget,)


class TabWidget(QtWidgets.QTabWidget):
    """Widget for managing the tabs section."""

    def __init__(
        self,
        parent: Optional[QtWidgets.QWidget] = None,
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
        self.detached_tabs: Dict[str, DetachedTab] = dict()
        if detachable:
            self.set_detachable()
        self.set_closable(closable)

    def __len__(self) -> int:
        return self.count()

    def __getitem__(self, index: int) -> QtWidgets.QWidget:
        if isinstance(index, int):
            return self.widget(index)
        else:
            return self.findChild(QtWidgets.QWidget, index)

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
        self.__init__()
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

    def set_document_mode(self, state: bool = True) -> None:
        self.setDocumentMode(state)

    def set_tab_shape(self, shape: str) -> None:
        """Set tab shape for the tabwidget.

        Valid values are "rounded" and "triangular"

        Args:
            shape: tab shape to use

        Raises:
            InvalidParamError: tab shape does not exist
        """
        if shape not in TAB_SHAPES:
            raise InvalidParamError(shape, TAB_SHAPES)
        self.setTabShape(TAB_SHAPES[shape])

    def get_tab_shape(self) -> str:
        """Return tab shape.

        possible values are "rounded", "triangular"

        Returns:
            tab shape
        """
        return TAB_SHAPES.inv[self.tabShape()]

    def set_tab_position(self, position: str) -> None:
        """Set tab position for the tabwidget.

        Valid values are "north", "south", "east", "west"

        Args:
            position: tab position to use

        Raises:
            InvalidParamError: tab position does not exist
        """
        if position not in TAB_POSITIONS:
            raise InvalidParamError(position, TAB_POSITIONS)
        self.setTabPosition(TAB_POSITIONS[position])

    def get_tab_position(self) -> str:
        """Return tab position.

        possible values are "north", "south", "east", "west"

        Returns:
            tab position
        """
        return TAB_POSITIONS.inv[self.tabPosition()]

    def get_children(self) -> list:
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

    def tab_icon(self, i: int) -> gui.Icon:
        return gui.Icon(self.tabIcon(i))

    def set_detachable(self) -> None:
        self.tab_bar.on_detach.connect(self.detach_tab)
        widgets.Application.call_on_exit(self.close_detached_tabs)
        self.setMovable(True)

    def set_closable(self, closable: bool = True) -> None:
        self.setTabsClosable(closable)

    @autoslot.AutoSlot
    def detach_tab(self, index: int, point: QtCore.QPoint) -> None:
        """Detach tab by removing its contents and placing them in a DetachedTab window.

        Args:
            index (int): index location of the tab to be detached
            point (QtCore.QPoint): screen pos for creating the new DetachedTab window

        Returns:
            None: Description
        """
        # Get the tab content
        name = self.tabText(index)
        icon = self.tabIcon(index)
        if icon.isNull():
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
        item: Union[QtWidgets.QWidget, QtWidgets.QLayout],
        label: str,
        icon: gui.icon.IconType = None,
        position: Optional[int] = None,
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
            icon = gui.icon.get_icon(icon)
            index = self.insertTab(position, widget, icon, label)
        if show:
            self.setCurrentIndex(index)
        return index

    def attach_tab(
        self,
        widget: Union[QtWidgets.QWidget, QtWidgets.QLayout],
        name: str,
        icon: gui.icon.IconType = None,
        insert_at: Optional[int] = None,
    ):
        """Re-attach tab.

        Re-attach the tab by removing the content from the DetachedTab window,
        closing it, and placing the content back into the DetachableTabWidget.

        Args:
            widget (Union[QtWidgets.QWidget, QtWidgets.QLayout]): the content widget
                from the DetachedTab window
            name (str): the name of the detached tab
            icon (gui.icon.IconType, optional): the window icon for the detached tab
            insert_at (Optional[int], optional): insert the re-attached tab at the
                given index
        """
        widget.setParent(self)

        # Remove the reference
        del self.detached_tabs[name]

        # Determine if the given image and the main window icon are the same.
        # If they are, then do not add the icon to the tab
        self.add_tab(widget, name, icon=icon, position=insert_at, show=True)

    def close_detached_tabs(self) -> None:
        """Close all tabs that are currently detached."""
        tabs = list(self.detached_tabs.values())
        for tab in tabs:
            tab.close()

    @autoslot.AutoSlot
    def remove_tab(self, index: int) -> None:
        widget = self.widget(index)
        self.removeTab(index)
        if widget is not None:
            widget.deleteLater()

    @autoslot.AutoSlot
    def open_widget(self, widget: QtWidgets.QWidget, title: str = "Unnamed"):
        """Create a tab containing delivered widget."""
        self.add_tab(widget, title, icon="mdi.widgets", show=True)

    def set_tab(
        self, index: int, position: str, widget: Optional[QtWidgets.QWidget] = None
    ) -> None:
        self.tabBar().set_tab(index, position, widget)


class DetachedTab(widgets.MainWindow):
    """Window containing a detached tab.

    When a tab is detached, the contents are placed into this QMainWindow.
    The tab can be re-attached by closing the dialog

    Attributes:
        on_close: signal, emitted when window is closed (widget, title, icon)
    """

    on_close = core.Signal(QtWidgets.QWidget, str, QtGui.QIcon)

    def __init__(self, name, widget):
        super().__init__(None)

        self.set_id(name)
        self.set_title(name)

        self.widget = widget
        self.setCentralWidget(self.widget)
        self.widget.show()

    #  If the window is closed, emit the on_close and give the
    #  content widget back to the DetachableTabWidget
    def closeEvent(self, event):
        self.on_close.emit(self.widget, self.id, self.windowIcon())


if __name__ == "__main__":
    app = widgets.app()
    tab_widget = TabWidget()
    widget = widgets.Widget()
    tab_widget.add_tab(widget, "Test")
    widget_2 = widgets.Widget()
    tab_widget.add_tab(widget_2, "Test 2")
    tab_widget.show()
    app.exec_()
