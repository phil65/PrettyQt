from qtpy import QtWidgets

from prettyqt import widgets


QtWidgets.QGraphicsTextItem.__bases__ = (widgets.GraphicsObject,)


class GraphicsTextItem(QtWidgets.QGraphicsTextItem):
    def __repr__(self):
        return f"{self.__class__.__name__}({self.toPlainText()!r})"

    def serialize_fields(self):
        return dict(
            open_external_links=self.openExternalLinks(),
            text_width=self.textWidth(),
            plain_text=self.toPlainText(),
        )
