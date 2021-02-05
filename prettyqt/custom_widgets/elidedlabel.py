from __future__ import annotations

from prettyqt import core, gui, widgets
from prettyqt.qt import QtWidgets


class ElidedLabel(widgets.Frame):
    elision_changed = core.Signal(bool)

    def __init__(
        self,
        text: str = "",
        parent: QtWidgets.QWidget | None = None,
    ):
        super().__init__(parent=parent)
        self.elided = False
        self.content = text
        self.set_size_policy("expanding", "preferred")

    def __repr__(self):
        return f"{type(self).__name__}({self.text()!r})"

    def set_text(self, text: str):
        self.content = text
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = gui.Painter(self)
        metrics = painter.get_font_metrics()
        did_elide = False
        line_spacing = metrics.lineSpacing()
        y = 0
        layout = gui.TextLayout(self.content, painter.font())
        with layout.process_layout():
            while True:
                line = layout.createLine()

                if not line.isValid():
                    break

                line.setLineWidth(self.width())
                next_line_y = y + line_spacing

                if self.height() >= next_line_y + line_spacing:
                    line.draw(painter, core.Point(0, y))
                    y = next_line_y
                else:
                    last_line = self.content[line.textStart() :]
                    elided_line = metrics.elided_text(last_line, "right", self.width())
                    painter.drawText(0, y + metrics.ascent(), elided_line)
                    line = layout.createLine()
                    did_elide = line.isValid()
                    break
        if did_elide != self.elided:
            self.elided = did_elide
            self.elision_changed.emit(did_elide)

    # def paintEvent(self, event):
    #     painter = gui.Painter(self)
    #     metrics = gui.FontMetrics(self.font())
    #     elided = metrics.elided_text(self.text(), "right", self.width())
    #     painter.drawText(self.rect(), self.alignment(), elided)


if __name__ == "__main__":
    app = widgets.app()
    widget = ElidedLabel("test")
    widget.show()
    app.main_loop()
