from __future__ import annotations

from prettyqt import core, gui, widgets
from prettyqt.qt import QtCore, QtGui
from prettyqt.utils import colors


class BaseOverlayWidget(widgets.Widget):
    """Border which surrounds a widget and follows it."""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_NoSystemBackground)
        # self.set_flags(tool=True)
        self._do_resize()
        self._border_width = 4
        self._border_color = gui.Color(255, 0, 0)
        self._fill_color = None
        parent.installEventFilter(self)

    def set_fill_color(self, color: colors.ColorType):
        self._fill_color = colors.get_color(color)

    def set_border_color(self, color: colors.ColorType):
        self._border_color = colors.get_color(color)

    def get_fill_color(self) -> gui.Color:
        return self._fill_color

    def get_border_color(self) -> gui.Color:
        return self._border_color

    def eventFilter(self, source, event):
        match event.type():
            case QtCore.QEvent.Type.Resize:
                self._do_resize()
            # case QtCore.QEvent.Type.ChildAdded:
            #     self._do_resize()
        return False

    def _do_resize(self):
        parent = self.parent()
        self.setGeometry(0, 0, parent.width(), parent.height())

    border_color = core.Property(QtGui.QColor, get_border_color, set_border_color)
    fill_color = core.Property(QtGui.QColor, get_fill_color, set_border_color)


class OverlayBorder(BaseOverlayWidget):
    def paintEvent(self, ev):
        with gui.Painter(self) as p:
            pen = gui.Pen(self._border_color, self._border_width)
            p.setPen(pen)
            if self._fill_color:
                p.setBrush(gui.Brush(self._fill_color))
            p.drawRect(self.geometry())


class FocusWidget(BaseOverlayWidget):
    def __init__(self, parent, focus_widget, overlay_color=None, **kwargs):
        super().__init__(parent, **kwargs)
        self._parent = parent
        self._focus_widget = focus_widget
        self._fill_color = overlay_color or gui.Color(0, 0, 0, 150)

    def paintEvent(self, ev):
        with gui.Painter(self) as p:
            pen = gui.Pen(gui.Color(255, 255, 255, 0), 0)
            p.setPen(pen)
            p.setBrush(gui.Brush(self._fill_color))
            inside_rect = gui.Region(self._focus_widget.geometry())
            outside_rect = gui.Region(self.geometry())
            to_draw = outside_rect.subtracted(inside_rect)
            data_path = gui.PainterPath()
            data_path.set_fill_rule("winding")
            data_path.addRegion(to_draw)
            p.drawPath(data_path)


if __name__ == "__main__":
    app = widgets.app()
    container = widgets.Widget()
    container.set_layout("horizontal")
    widget = widgets.PlainTextEdit()
    widget2 = widgets.PlainTextEdit()
    container.box.add(widget)
    container.box.add(widget2)
    errorbox = FocusWidget(container, widget2)
    errorbox.show()
    container.show()
    app.main_loop()
