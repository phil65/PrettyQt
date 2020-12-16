from typing import Any, Dict

from qtpy import QtWidgets

from prettyqt import constants, widgets


QtWidgets.QDockWidget.__bases__ = (widgets.Widget,)


class DockWidget(QtWidgets.QDockWidget):
    """Customized DockWidget class.

    Contains a custom TitleBar with maximise button
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

    def __setstate__(self, state: Dict[str, Any]) -> None:
        self.set_widget(state["widget"])

    def __reduce__(self):
        return type(self), (), self.__getstate__()

    def serialize_fields(self) -> Dict[str, Any]:
        return dict(widget=self.widget())

    def set_widget(self, widget):
        self.setWidget(widget)

    def set_allowed_areas(self, area: constants.DockPositionsStr):
        self.setAllowedAreas(constants.DOCK_POSITIONS[area])

    def setup_title_bar(self):
        title_bar = widgets.Widget()
        layout = widgets.BoxLayout("horizontal")
        layout.set_margin(0)
        layout.set_alignment("right")
        title_bar.set_layout(layout)
        maximise_button = widgets.PushButton()
        layout += maximise_button
        maximise_button.set_style_icon("titlebar_max_button")
        maximise_button.clicked.connect(self.maximise)
        close_button = widgets.PushButton()
        close_button.set_style_icon("titlebar_close_button")
        layout += close_button
        close_button.clicked.connect(self.close)
        self.setTitleBarWidget(title_bar)

    def maximise(self):
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
