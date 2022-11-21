from __future__ import annotations

from typing import Any

from deprecated import deprecated

from prettyqt import constants, widgets
from prettyqt.qt import QtWidgets


QtWidgets.QDockWidget.__bases__ = (widgets.Widget,)


class DockWidget(QtWidgets.QDockWidget):
    """Customized DockWidget class.

    Contains a custom TitleBar with maximize button
    """

    def __init__(self, *args, **kwargs):
        name = kwargs.pop("name", None)
        title = kwargs.pop("title", None)
        super().__init__(*args, **kwargs)
        if name:
            self.set_id(name)
        if title:
            self.set_title(title)
        self.set_allowed_areas("all")

    def __setstate__(self, state: dict[str, Any]) -> None:
        self.set_widget(state["widget"])

    def __reduce__(self):
        return type(self), (), self.__getstate__()

    def serialize_fields(self) -> dict[str, Any]:
        return dict(widget=self.widget())

    def set_widget(self, widget: QtWidgets.QWidget):
        self.setWidget(widget)

    def set_allowed_areas(self, area: constants.DockPositionsStr):
        self.setAllowedAreas(constants.DOCK_POSITIONS[area])

    def setup_title_bar(self):
        title_bar = widgets.Widget()
        layout = widgets.BoxLayout("horizontal")
        layout.set_margin(0)
        layout.set_alignment("right")
        title_bar.set_layout(layout)
        maximize_button = widgets.PushButton()
        layout.add(maximize_button)
        maximize_button.set_style_icon("titlebar_max_button")
        maximize_button.clicked.connect(self.maximize)
        close_button = widgets.PushButton()
        close_button.set_style_icon("titlebar_close_button")
        layout.add(close_button)
        close_button.clicked.connect(self.close)
        self.setTitleBarWidget(title_bar)

    @deprecated(reason="This method is deprecated, use 'maximize' instead.")
    def maximise(self):
        self.maximize()

    def maximize(self):
        if not self.isFloating():
            self.setFloating(True)
        if not self.isMaximized():
            self.showMaximized()
        else:
            self.showMinimized()


if __name__ == "__main__":
    app = widgets.app()
    win = widgets.MainWindow()
    dock_widget = DockWidget(name="aa", title="Test")
    dock_widget.setup_title_bar()
    win.add_dockwidget(dock_widget, "left")
    win.show()
    app.main_loop()
