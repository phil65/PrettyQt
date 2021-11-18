from __future__ import annotations

from typing import Literal

from prettyqt import widgets
from prettyqt.qt import QtCore, QtGui, QtWidgets


SideStr = Literal["left", "top", "right", "bottom"]


# Aero snap still doesn't work https://bugreports.qt.io/browse/QTBUG-84466


class TitleBarIcon(widgets.PushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)

        self.setStyleSheet(
            "margin: 0;" "padding: 0px;" "font-size: 16px;" "width: 44px;" "height: 30px;"
        )

        self.set_margin(0)


class CustomTitleBar(widgets.Frame):
    def __init__(self, window_widget: QtWidgets.QWidget):
        super().__init__(window_widget)

        self.window_widget = window_widget
        self.minimize_button = TitleBarIcon("🗕")
        self.maximize_button = TitleBarIcon("🗖")
        self.exit_button = TitleBarIcon("✕")

        self.minimize_button.clicked.connect(
            lambda: window_widget.setWindowState(QtCore.Qt.WindowMinimized)
        )
        self.maximize_button.clicked.connect(
            lambda: (
                window_widget.showNormal()
                if window_widget.isMaximized()
                else window_widget.showMaximized()
            )
        )
        self.exit_button.clicked.connect(window_widget.close)

        self.set_layout("horizontal")
        spacer_item = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding)
        self.box.addSpacerItem(spacer_item)
        for widget in [
            self.minimize_button,
            self.maximize_button,
            self.exit_button,
        ]:
            self.box.addWidget(widget)

        self.setStyleSheet("width: 100%;" "padding: 0;" "margin: 0;")
        self.setContentsMargins(0, 0, 0, 0)
        self.box.setContentsMargins(0, 0, 0, 0)
        self.box.setSpacing(0)

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.window_widget.windowHandle().startSystemMove()


class FramelessWindow(widgets.Widget):
    gripSize = 6

    def __init__(self, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent)

        # Remove window title bar and frame
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint)

        self.title_bar = CustomTitleBar(self)
        self.main_widget = widgets.MainWindow()

        # Set up layout
        self.main_layout = widgets.BoxLayout("vertical")
        self.main_layout.addWidget(self.title_bar)
        self.main_layout.addWidget(self.main_widget)

        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.grip_layout = widgets.GridLayout()

        self.grip_layout.addLayout(self.main_layout, 1, 1)
        self.grip_layout.addWidget(EdgeGrip(QtCore.Qt.TopEdge), 0, 1)
        self.grip_layout.addWidget(EdgeGrip(QtCore.Qt.RightEdge), 1, 2)
        self.grip_layout.addWidget(EdgeGrip(QtCore.Qt.BottomEdge), 2, 1)
        self.grip_layout.addWidget(EdgeGrip(QtCore.Qt.LeftEdge), 1, 0)
        self.grip_layout.addWidget(EdgeGrip(QtCore.Qt.TopEdge | QtCore.Qt.LeftEdge), 0, 0)
        self.grip_layout.addWidget(
            EdgeGrip(QtCore.Qt.TopEdge | QtCore.Qt.RightEdge), 0, 2
        )
        self.grip_layout.addWidget(
            EdgeGrip(QtCore.Qt.BottomEdge | QtCore.Qt.LeftEdge), 2, 0
        )
        self.grip_layout.addWidget(
            EdgeGrip(QtCore.Qt.BottomEdge | QtCore.Qt.RightEdge), 2, 2
        )

        self.grip_layout.setContentsMargins(0, 0, 0, 0)
        self.grip_layout.setSpacing(0)
        self.setLayout(self.grip_layout)

    def __getattr__(self, attr: str):
        return getattr(self.main_widget, attr)


class EdgeGrip(widgets.Widget):
    def __init__(self, edges: QtCore.Qt.Edges | QtCore.Qt.Edge, grip_size=6, parent=None):
        super().__init__(parent)
        self.edges = edges
        self.grip_size = grip_size
        # Sides
        if edges == QtCore.Qt.TopEdge:
            self.setCursor(QtCore.Qt.SizeVerCursor)
            self.setFixedHeight(self.grip_size)
        elif edges == QtCore.Qt.RightEdge:
            self.setCursor(QtCore.Qt.SizeHorCursor)
            self.setFixedWidth(self.grip_size)
        elif edges == QtCore.Qt.BottomEdge:
            self.setCursor(QtCore.Qt.SizeVerCursor)
            self.setFixedHeight(self.grip_size)
        elif edges == QtCore.Qt.LeftEdge:
            self.setCursor(QtCore.Qt.SizeHorCursor)
            self.setFixedWidth(self.grip_size)
        # Corners
        elif edges == QtCore.Qt.TopEdge | QtCore.Qt.LeftEdge:
            self.setCursor(QtCore.Qt.SizeFDiagCursor)
        elif edges == QtCore.Qt.TopEdge | QtCore.Qt.RightEdge:
            self.setCursor(QtCore.Qt.SizeBDiagCursor)
        elif edges == QtCore.Qt.BottomEdge | QtCore.Qt.LeftEdge:
            self.setCursor(QtCore.Qt.SizeBDiagCursor)
        elif edges == QtCore.Qt.BottomEdge | QtCore.Qt.RightEdge:
            self.setCursor(QtCore.Qt.SizeFDiagCursor)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.parent().windowHandle().startSystemResize(self.edges)


if __name__ == "__main__":
    app = widgets.app()
    m = FramelessWindow()
    button = widgets.PushButton("test")
    m.set_widget(button)
    m.show()
    m.resize(240, 160)
    app.main_loop()
