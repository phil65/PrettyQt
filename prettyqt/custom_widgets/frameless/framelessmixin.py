from __future__ import annotations

from typing import Literal

from prettyqt import widgets
from prettyqt.custom_widgets.frameless.windows import utils
from prettyqt.qt import QtCore, QtGui, QtWidgets


class TitleBarButton(widgets.PushButton):
    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)
        self.setFixedSize(48, 32)
        self.set_icon_size((28, 28))


class MaximizeButton(TitleBarButton):
    def __init__(self, parent: QtWidgets.QWidget | None) -> None:
        super().__init__(parent)
        self.setStyleSheet(
            """
        QPushButton {
            background-position: center;
            background-repeat: no-repeat;
            border: none;
            outline: none;
            color: #d1d3d2;
        }

        QPushButton::hover {
            background-color: #1D1D24;
        }
        """
        )

        self.set_icon("mdi.window-maximize")

    def set_state(self, state: Literal["hover", "normal"]) -> None:
        if state == "hover":
            self.setStyleSheet(
                """
                    QPushButton {
                        background-position: center;
                        background-repeat: no-repeat;
                        border: none;
                        outline: none;
                        color: #d1d3d2;
                        background-color: #1D1D24;
                    }
                    """
            )
        elif state == "normal":
            self.setStyleSheet(
                """
                    QPushButton {
                        background-position: center;
                        background-repeat: no-repeat;
                        border: none;
                        outline: none;
                        color: #d1d3d2;
                        background: transparent;
                    }
                    """
            )
        self.update()


class MinimizeButton(TitleBarButton):
    def __init__(self, parent: QtWidgets.QWidget | None) -> None:
        super().__init__(parent)
        self.setStyleSheet(
            """
                QPushButton {
            background-position: center;
            background-repeat: no-repeat;
            border: none;
            outline: none;
            color: #d1d3d2;
        }

        QPushButton::hover {
            background-color: #1D1D24;
        }
        """
        )
        self.set_icon("mdi.window-minimize")


class CloseButton(TitleBarButton):
    def __init__(self, parent: QtWidgets.QWidget | None) -> None:
        super().__init__(parent)
        self.setStyleSheet(
            """
        QPushButton {
            background-position: center;
            background-repeat: no-repeat;
            border: none;
            outline: none;
            color: #d1d3d2;
        }

        QPushButton:hover {
            background-color: #e81123;
        }"""
        )
        self.set_icon("mdi.window-close")


class TitleBar(widgets.Frame):
    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)
        self.setFixedHeight(32)

        self.button_box = widgets.Widget(self)

        self.maximize_button = MaximizeButton(self.button_box)
        self.minimize_button = MinimizeButton(self.button_box)
        self.close_button = CloseButton(self.button_box)

        self.bbox_layout = widgets.BoxLayout("horizontal", parent=self.button_box)
        self.bbox_layout.set_margin(0)
        self.bbox_layout.setSpacing(0)
        for btn in [self.minimize_button, self.maximize_button, self.close_button]:
            self.bbox_layout.addWidget(btn)

        self.horizontal_layout = widgets.BoxLayout("horizontal", parent=self)
        self.horizontal_layout.set_margin(0)
        self.horizontal_layout.setSpacing(0)
        self.horizontal_spacer = widgets.SpacerItem(20, 20, "expanding", "minimum")
        self.horizontal_layout.addSpacerItem(self.horizontal_spacer)
        self.horizontal_layout.addWidget(self.button_box)
        self.minimize_button.clicked.connect(self.on_minimize_button_clicked)
        self.maximize_button.clicked.connect(self.on_maximize_button_clicked)
        self.close_button.clicked.connect(self.on_close_button_clicked)

        self.window().installEventFilter(self)

    def on_close_button_clicked(self) -> None:
        self.window().close()

    def on_maximize_button_clicked(self):
        if self.topLevelWidget().isMaximized():
            self.window().showNormal()
            self.set_maximize_button_icon("maximize")
        else:
            self.window().showMaximized()
            self.set_maximize_button_icon("restore")

    def on_minimize_button_clicked(self) -> None:
        self.window().showMinimized()

    def set_maximize_button_icon(self, icon: Literal["maximize", "restore"]) -> None:
        if icon == "maximize":
            self.maximize_button.set_icon("mdi.window-maximize")
        elif icon == "restore":
            self.maximize_button.set_icon("mdi.window-restore")

    def eventFilter(self, obj, e):
        if obj is self.window() and e.type() == QtCore.QEvent.Type.WindowStateChange:
            if self.window().isMaximized():
                self.set_maximize_button_icon("restore")

            else:
                self.set_maximize_button_icon("maximize")
        return super().eventFilter(obj, e)

    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        utils.start_system_move(self.window().winId())


class FramelessMixin:
    def __init__(self, parent: QtWidgets.QWidget | None = None, **kwargs) -> None:
        super().__init__(parent, **kwargs)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Window | QtCore.Qt.WindowType.FramelessWindowHint
        )
        self.title_bar = TitleBar(self)
        win_id = self.winId()
        utils.add_shadow_effect(win_id)
        utils.add_window_animation(win_id)

        self.resize(800, 800)

    def set_nonresizable(self):
        utils.set_window_nonresizable(self.winId())
        self.title_bar.maximize_button.hide()

    def is_resizable(self) -> None:
        return utils.is_window_resizable(self.winId())

    def showEvent(self, event) -> None:
        self.title_bar.raise_()
        super().showEvent(event)

    def nativeEvent(self, event_type: QtCore.QByteArray, message: int):
        ret_tuple = utils._native_event(self, message)
        if ret_tuple is not None:
            ret, value = ret_tuple
            if ret:
                return ret, value
        super().nativeEvent(event_type, message)

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self.title_bar.resize(self.width(), self.title_bar.height())


if __name__ == "__main__":
    app = widgets.app()
    app.set_style("Fusion")

    class MainWindow(FramelessMixin, widgets.MainWindow):
        pass

    m = MainWindow()
    button = widgets.PushButton("test")
    m.setCentralWidget(button)
    m.show()
    m.resize(240, 160)
    app.main_loop()
