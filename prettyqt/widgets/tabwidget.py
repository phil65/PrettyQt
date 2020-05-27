# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

import qtawesome as qta
from qtpy import QtCore, QtGui, QtWidgets

from prettyqt import core, gui, widgets
from prettyqt.utils import bidict

TAB_SHAPES = bidict(rounded=QtWidgets.QTabWidget.Rounded,
                    triangular=QtWidgets.QTabWidget.Triangular)


QtWidgets.QTabWidget.__bases__ = (widgets.Widget,)


class TabWidget(QtWidgets.QTabWidget):
    """
    Widget for managing the tabs section
    """

    def __init__(self, parent=None, closable=False, detachable=False):

        # Basic initalization
        super().__init__(parent)
        self.tabCloseRequested.connect(self.remove_tab)
        self.tab_bar = widgets.TabBar(self)

        self.setTabBar(self.tab_bar)

        # Used to keep a reference to detached tabs since their QMainWindow
        # does not have a parent
        self.detached_tabs = dict()
        if detachable:
            self.set_detachable()
        self.set_closable(closable)

    def __len__(self):
        return self.count()

    def __getitem__(self, index):
        if isinstance(index, int):
            return self.widget(index)
        else:
            return self.findChild(QtWidgets.QWidget, index)

    def __getstate__(self):
        return dict(tabbar=self.tabBar(),
                    widgets=self.get_children(),
                    movable=self.isMovable(),
                    document_mode=self.documentMode(),
                    current_index=self.currentIndex(),
                    tab_shape=self.get_tab_shape(),
                    # elide_mode=self.get_elide_mode(),
                    icon_size=self.iconSize())

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

    def set_tab_shape(self, shape: str):
        """set tab shape for the tabwidget

        Valid values are "rounded" and "triangular"

        Args:
            shape: tab shape to use

        Raises:
            ValueError: tab shape does not exist
        """
        if shape not in TAB_SHAPES:
            raise ValueError("Invalid value for shape.")
        self.setTabShape(TAB_SHAPES[shape])

    def get_tab_shape(self) -> str:
        """returns tab shape

        possible values are "roundes", "triangular"

        Returns:
            tab shape
        """
        return TAB_SHAPES.inv[self.tabShape()]

    def get_children(self):
        return [(self.widget(i), self.tabText(i), self.tab_icon(i),
                 self.tabToolTip(i), self.tabWhatsThis(i))
                for i in range(self.count())]

    def tab_icon(self, i):
        return gui.Icon(self.tabIcon(i))

    def set_detachable(self):
        self.tab_bar.on_detach.connect(self.detach_tab)
        widgets.app().aboutToQuit.connect(self.close_detached_tabs)
        self.setMovable(True)

    def set_closable(self, closable: bool = True):
        self.setTabsClosable(closable)

    @core.Slot(int, QtCore.QPoint)
    def detach_tab(self, index: int, point: QtCore.QPoint):
        """
        Detach the tab by removing it's contents and placing them in
        a DetachedTab window

        @param index    index location of the tab to be detached
        @param point    screen pos for creating the new DetachedTab window
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

    def add_tab(self, item, label, icon=None):
        if isinstance(item, QtWidgets.QLayout):
            widget = widgets.Widget()
            widget.set_layout(item)
        else:
            widget = item
        if not icon:
            return self.addTab(widget, label)
        else:
            if isinstance(icon, str):
                icon = qta.icon(icon)
            return self.addTab(widget, icon, label)

    def insert_tab(self, pos, widget, label, icon=None):
        if not icon:
            return self.insertTab(pos, widget, label)
        else:
            if isinstance(icon, str):
                icon = qta.icon(icon)
            return self.insertTab(pos, widget, icon, label)

    def attach_tab(self, widget, name, icon, insert_at=None):
        """
        Re-attach the tab by removing the content from the DetachedTab window,
        closing it, and placing the content back into the DetachableTabWidget

        @param    widget    the content widget from the DetachedTab window
        @param    name             the name of the detached tab
        @param    icon             the window icon for the detached tab
        @param    insert_at         insert the re-attached tab at the given index
        """

        widget.setParent(self)

        # Remove the reference
        del self.detached_tabs[name]

        # Determine if the given image and the main window icon are the same.
        # If they are, then do not add the icon to the tab
        if insert_at is None:
            index = self.add_tab(widget, name, icon=icon)
        else:
            index = self.insert_tab(insert_at, widget, name, icon=icon)
        # Make this tab the current tab
        self.setCurrentIndex(index)

    def close_detached_tabs(self):
        """Close all tabs that are currently detached
        """
        for detached_tab in self.detached_tabs.values():
            detached_tab.close()

    @core.Slot(int)
    def remove_tab(self, index: int):
        widget = self.widget(index)
        self.removeTab(index)
        if widget is not None:
            widget.deleteLater()

    @core.Slot(object, str)
    def open_widget(self, widget: QtWidgets.QWidget, title: str = "Unnamed"):
        """
        create a tab containing delivered widget
        """
        index = self.add_tab(widget, title, icon="mdi.widgets")
        self.setCurrentIndex(index)

    def set_tab(self, index, position: str, widget=None):
        self.tabBar().set_tab(index, position, widget)


class DetachedTab(widgets.MainWindow):
    """window containing a detached tab

    When a tab is detached, the contents are placed into this QMainWindow.
    The tab can be re-attached by closing the dialog

    Attributes:
        on_close: signal, emitted when window is closed (widget, title, icon)
    """
    on_close = core.Signal(QtWidgets.QWidget, str, QtGui.QIcon)

    def __init__(self, name, widget):
        super().__init__(None)

        self.id = name
        self.title = name

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
