from typing import Union

from qtpy import QtWidgets

from prettyqt import widgets, gui


QtWidgets.QGraphicsWidget.__bases__ = (widgets.GraphicsObject, widgets.GraphicsLayoutItem)


class GraphicsWidget(QtWidgets.QGraphicsWidget):
    def serialize_fields(self):
        return dict(
            autofill_background=self.autoFillBackground(),
            font=gui.Font(self.font()),
            window_title=self.windowTitle(),
        )

    def set_layout(self, layout: Union[str, QtWidgets.QGraphicsLayout, None]) -> None:
        if layout is None:
            return None
        if layout == "grid":
            self.box = widgets.GraphicsGridLayout()
        elif layout in ["horizontal", "vertical"]:
            self.box = widgets.GraphicsLinearLayout(layout)
        elif layout == "anchor":
            self.box = widgets.GraphicsAnchorLayout()
        elif isinstance(layout, QtWidgets.QGraphicsLayout):
            self.box = layout
        else:
            raise ValueError("Invalid Layout")
        self.setLayout(self.box)
