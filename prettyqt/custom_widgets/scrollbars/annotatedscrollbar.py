from __future__ import annotations

from prettyqt import constants, core, gui, widgets
from prettyqt.utils import colors, datatypes

CC_ScrollBar = widgets.QStyle.ComplexControl.CC_ScrollBar
SubControl = widgets.QStyle.SubControl


class AnnotatedScrollBar(widgets.ScrollBar):
    """ScrollBar which can highlight user-defined ranges."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._annotation_color = gui.QColor("gold")
        self._annotations = []
        self._document_height = 100

    def set_annotations(self, annotations: list[tuple[int, int]]):
        self._annotations = annotations

    def get_annotations(self) -> list[tuple[int, int]]:
        return self._annotations

    def add_annotation(self, annotation: tuple[int, int]):
        self._annotations.append(annotation)

    def paintEvent(self, event):
        super().paintEvent(event)
        with gui.Painter(self) as p:
            opt = widgets.QStyleOptionSlider()
            self.initStyleOption(opt)
            gr = self.style().subControlRect(
                CC_ScrollBar, opt, SubControl.SC_ScrollBarGroove, self
            )
            sr = self.style().subControlRect(
                CC_ScrollBar, opt, SubControl.SC_ScrollBarSlider, self
            )
            p.setClipRegion(
                gui.QRegion(gr) - gui.QRegion(sr), constants.ClipOperation.IntersectClip
            )
            x, y, w, h = gr.getRect()
            c = gui.QColor(self._annotation_color)
            p.setBrush(c)
            c.setAlphaF(0.3)
            p.setPen(gui.QPen(c, 2.0))
            yscale = 1.0 / self._document_height
            rects = [
                core.QRect(
                    x + 1,
                    y + h * start * yscale - 0.5,
                    w - 2,
                    h * (end - start) * yscale + 1,
                )
                for start, end in self._annotations
            ]
            p.drawRects(rects)

    def set_annotation_color(self, color: datatypes.ColorType):
        self._annotation_color = colors.get_color(color).as_qt()

    def get_annotation_color(self) -> gui.QColor:
        return self._annotation_color

    annotation_color = core.Property(
        gui.QColor, get_annotation_color, set_annotation_color
    )
    annotations = core.Property(list, get_annotations, set_annotations)


if __name__ == "__main__":
    app = widgets.app()
    widget = widgets.PlainTextEdit("\n".join(f"abc{i}" for i in range(1000)))
    scrollbar = AnnotatedScrollBar("vertical", parent=widget)
    scrollbar.set_annotations([(10, 20), (50, 51), (82, 85)])
    widget.setVerticalScrollBar(scrollbar)
    widget.show()
    with app.debug_mode():
        app.exec()
