from __future__ import annotations

from typing import Literal, overload

from prettyqt import core, gui, iconprovider, widgets
from prettyqt.qt import QtCore, QtGui, QtWidgets
from prettyqt.utils import InvalidParamError, animator, bidict, datatypes, listdelegators


TabShapeStr = Literal["rounded", "triangular"]

TAB_SHAPES: bidict[TabShapeStr, QtWidgets.QTabWidget.TabShape] = bidict(
    rounded=QtWidgets.QTabWidget.TabShape.Rounded,
    triangular=QtWidgets.QTabWidget.TabShape.Triangular,
)

TabPositionStr = Literal["north", "south", "west", "east"]

TAB_POSITION: bidict[TabPositionStr, QtWidgets.QTabWidget.TabPosition] = bidict(
    north=QtWidgets.QTabWidget.TabPosition.North,
    south=QtWidgets.QTabWidget.TabPosition.South,
    west=QtWidgets.QTabWidget.TabPosition.West,
    east=QtWidgets.QTabWidget.TabPosition.East,
)


class TabWidget(widgets.WidgetMixin, QtWidgets.QTabWidget):
    """Widget for managing the tabs section."""

    def __init__(
        self, closable: bool = False, detachable: bool = False, **kwargs
    ) -> None:
        # Basic initalization
        super().__init__(**kwargs)
        self.animator = animator.Animator(self)
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

    @overload
    def __getitem__(self, index: int) -> QtWidgets.QWidget:
        ...

    @overload
    def __getitem__(
        self, index: slice
    ) -> listdelegators.BaseListDelegator[QtWidgets.QWidget]:
        ...

    def __getitem__(
        self, index: int | slice
    ) -> QtWidgets.QWidget | listdelegators.BaseListDelegator[QtWidgets.QWidget]:
        match index:
            case int():
                if index >= self.count():
                    raise IndexError(index)
                return self.widget(index)
            case slice():
                rng = range(index.start or 0, index.stop or self.count(), index.step or 1)
                return listdelegators.BaseListDelegator(self.widget(i) for i in rng)
            case _:
                raise TypeError(index)

    def __contains__(self, item: QtWidgets.QWidget):
        return self.indexOf(item) >= 0

    def update_tab_bar_visibility(self):
        """Update visibility of the tabBar depending of the number of tabs.

        0 or 1 tab -> tabBar hidden, 2+ tabs - >tabBar visible
        need to be called explicitly, or be connected to tabInserted/tabRemoved
        """
        self.tabBar().setVisible(self.count() > 1)

    def set_icon_size(self, size: int | datatypes.SizeType):
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
        return None if icon.isNull() else gui.Icon(icon)

    def set_detachable(self):
        self.tab_bar.tab_doubleclicked.connect(self.detach_tab)
        core.CoreApplication.call_on_exit(self.close_detached_tabs)
        self.setMovable(True)

    def set_closable(self, closable: bool = True):
        self.setTabsClosable(closable)

    @core.Slot(int, QtCore.QPoint)
    def detach_tab(self, index: int, point: datatypes.PointType):
        """Detach tab by removing its contents and placing them in a DetachedTab window.

        Args:
            index (int): index location of the tab to be detached
            point (QtCore.QPoint): screen pos for creating the new DetachedTab window

        """
        # Get the tab content
        if isinstance(point, tuple):
            point = QtCore.QPoint(*point)
        name = self.tabText(index)
        icon = self.tab_icon(index) or self.window().windowIcon()
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
        icon: datatypes.IconType = None,
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
        icon: datatypes.IconType = None,
        insert_at: int | None = None,
    ):
        """Re-attach tab.

        Re-attach the tab by removing the content from the DetachedTab window,
        closing it, and placing the content back into the DetachableTabWidget.

        Args:
            widget (Union[QtWidgets.QWidget, QtWidgets.QLayout]): the content widget
                from the DetachedTab window
            name (str): the name of the detached tab
            icon (datatypes.IconType, optional): the window icon for the detached tab
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
    def remove_tab(self, index_or_widget: int | QtWidgets.QWidget):
        index = (
            self.indexOf(index_or_widget)
            if isinstance(index_or_widget, QtWidgets.QWidget)
            else index_or_widget
        )
        widget = (
            self.widget(index_or_widget)
            if isinstance(index_or_widget, int)
            else index_or_widget
        )
        self.removeTab(index)
        if widget is not None:
            widget.deleteLater()

    @core.Slot(QtWidgets.QWidget, str)
    def open_widget(self, widget: QtWidgets.QWidget, title: str = "Unnamed"):
        """Create a tab containing delivered widget."""
        self.add_tab(widget, title, icon="mdi.widgets", show=True)

    def set_tab(self, index: int, position: str, widget: QtWidgets.QWidget | None = None):
        self.tabBar().set_tab(index, position, widget)

    def create_tab_preview(self, index: int, width: int = 200) -> widgets.Label:
        widget = widgets.Label(self)
        widget.setScaledContents(True)
        px = self.widget(index).grab().scaledToWidth(width)
        widget.setPixmap(px)
        widget.resize(width, width)
        return widget


class DetachedTab(widgets.MainWindow):
    """Window containing a detached tab.

    When a tab is detached, the contents are placed into this QMainWindow.
    The tab can be re-attached by closing the dialog

    Attributes:
        on_close: signal, emitted when window is closed (widget, title, icon)
    """

    on_close = core.Signal(QtWidgets.QWidget, str, QtGui.QIcon)

    def __init__(self, name: str, widget: QtWidgets.QWidget, **kwargs):
        super().__init__(**kwargs)

        self.set_id(name)
        self.set_title(name)

        self.widget = widget
        self.setCentralWidget(self.widget)
        self.widget.show()

    #  If the window is closed, emit the on_close and give the
    #  content widget back to the DetachableTabWidget
    def closeEvent(self, event):
        self.on_close.emit(self.widget, self.get_id(), self.windowIcon())


# import sys
# import ctypes
# from win32con import WM_ACTIVATE, WM_CLOSE, WM_CREATE

# WM_DWMSENDICONICTHUMBNAIL = 0x0323
# WM_DWMSENDICONICLIVEPREVIEWBITMAP = 0x0326


# class TopTabWidget(TabWidget):
#     """Widget for managing the tabs section."""

#     def __init__(
#         self,
#         parent: QtWidgets.QWidget | None = None,
#         closable: bool = False,
#         detachable: bool = False,
#     ) -> None:
#         # Basic initalization
#         super().__init__(parent)

#     def nativeEvent(self, event, message):
#         return_value, result = super().nativeEvent(event, message)
#         if sys.platform != "win32":
#             return return_value, bool(result)
#         # if you use Windows OS
#         if event in [b"windows_generic_MSG", b"windows_dispatcher_MSG"]:
#             msg = ctypes.wintypes.MSG.from_address(int(message))
#             if True:
#                 print(msg.message)
#                 # if msg.message == 274:
#                 #     raise ValueError()
#                 if msg.message == WM_CREATE:
#                     pass
#                 if msg.message == WM_ACTIVATE:
#                     print("WM_ACTIVATE", msg.hWnd)
#                 if msg.message == WM_CLOSE:
#                     print("WM_CLOSE", msg.hWnd)
#                     # see https://github.com/microsoft/Windows-classic-samples/
#                     # blob/main/Samples/Win7Samples/winui/shell/
#                     # appshellintegration/TabThumbnails/TabWnd.cpp
#                     # if (LOWORD(wParam) == WA_ACTIVE)
#                     print(self.window(), self)
#                     self.window().remove_tab(self)
#                     taskbaritem.taskbar.UnregisterTab(int(msg.hWnd))
#                     # item.unregister_tab()
#                 if msg.message == WM_DWMSENDICONICTHUMBNAIL:
#                     print("WM_DWMSENDICONICTHUMBNAIL", msg.hWnd)
#                     pix = self.grab()
#                     pix = pix.scaled(QtCore.Qt.AspectRatioMode.KeepAspectRatio)

#                     pix.toImage().toHBITMAP()

#                     # DwmSetIconicThumbnail(id, hbitmap, 0);
#                     # DeleteObject(hbitmap);
#                     # return true;

#                 if msg.message == WM_DWMSENDICONICLIVEPREVIEWBITMAP:
#                     print("WM_DWMSENDICONICLIVEPREVIEWBITMAP", msg.hWnd)
#                     widget = self.window()
#                     SIZE = 50
#                     pix = widget.grab().scaled(
#                         SIZE, QtCore.Qt.AspectRatioMode.KeepAspectRatio
#                     )
#                     pix.toImage().toHBITMAP()

#                 # DwmSetIconicLivePreviewBitmap(id, hbitmap, 0);
#                 # DeleteObject(hbitmap);
#                 # return true;

#         # case WM_CREATE:
#         # {
#         #     // Set DWM window attributes to indicate we'll provide the iconic bitmap,
#         #     // and to always render the thumbnail using the iconic bitmap.
#         #     BOOL fForceIconic = TRUE;
#         #     BOOL fHasIconicBitmap = TRUE;

#         #     DwmSetWindowAttribute(
#         #         _hwnd,
#         #         DWMWA_FORCE_ICONIC_REPRESENTATION,
#         #         &fForceIconic,
#         #         sizeof(fForceIconic));

#         #     DwmSetWindowAttribute(
#         #         _hwnd,
#         #         DWMWA_HAS_ICONIC_BITMAP,
#         #         &fHasIconicBitmap,
#         #         sizeof(fHasIconicBitmap));

#         #     // Tell the taskbar about this tab window
#         #     _pMainDlg->RegisterTab(this);
#         #     break;

#         return return_value, bool(result)

#     # def add_tab(self, *args, **kwargs):
#     #     result = super().add_tab(*args, **kwargs)
#     #     widgets.app().register_tab(args[0])
#     #     return result


# if __name__ == "__main__":
#     app = widgets.app()
#     # mainwindow = widgets.MainWindow()
#     # mainwindow.show()
#     tab_widget = TopTabWidget()
#     tab_widget.show()
#     tab_widget.set_detachable()
#     widget = TopTabWidget()
#     widget.show()
#     img = widget.grab().toImage().toHBITMAP()
#     widget_2 = TopTabWidget()
#     print("IDs", widget.get_win_id(), widget_2.get_win_id())

#     from prettyqt.utils.platforms.windows import taskbaritem

#     tb = taskbaritem.TaskBarItem(tab_widget.get_win_id())
#     tb.register_tab(widget.winId())
#     tb.register_tab(widget_2.winId())
#     tb2 = taskbaritem.TaskBarItem(widget.get_win_id())
#     tb2.set_iconic_thumbnail(img)
#     tb.set_iconic_thumbnail(img)
#     tab_widget.add_tab(widget, "Test")
#     tab_widget.add_tab(widget_2, "Test 2")
#     app.exec()

if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    tabwidget = TabWidget()
    widget2 = widgets.RadioButton("Test")
    widget3 = widgets.PlainTextEdit("Test 243434")
    tabwidget.add_tab(widget2, label="test")
    tabwidget.add_tab(widget3, label="test")
    tabwidget.show()
    app.sleep(2)
    tabwidget.animator.slide_in_next()
    app.sleep(2)
    tabwidget.animator.fade_in(0)
    app.sleep(2)
    tabwidget.animator.fade_in(1)
    app.exec()
