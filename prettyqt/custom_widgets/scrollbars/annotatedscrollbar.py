from __future__ import annotations

from typing import TYPE_CHECKING

from prettyqt import constants, core, gui, widgets
from prettyqt.utils import colors


if TYPE_CHECKING:
    from prettyqt.utils import datatypes


CC_ScrollBar = widgets.QStyle.ComplexControl.CC_ScrollBar
SubControl = widgets.QStyle.SubControl


class AnnotatedScrollBar(widgets.ScrollBar):
    r"""ScrollBar which can highlight user-defined ranges.

    ``` py
    widget = widgets.PlainTextEdit("\n".join(str(i) for i in range(1000)))
    widget.v_scrollbar = AnnotatedScrollBar(constants.VERTICAL)
    widget.v_scrollbar.set_annotations([(10, 20), (50, 60), (82, 85)])
    ```

    <figure markdown>
      ![Image title](../../images/annotatedscrollbar.png)
      <figcaption>Annotated ScrollBar</figcaption>
    </figure>
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._annotation_color = gui.QColor("gold")
        self._annotations = []
        self._document_length = 100

    @classmethod
    def create_example(cls):
        widget = widgets.PlainTextEdit("\n".join(str(i) for i in range(1000)))
        widget.v_scrollbar = AnnotatedScrollBar(constants.VERTICAL)
        widget.v_scrollbar.set_annotations([(10, 20), (50, 60), (82, 85)])
        return widget

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
            scale = 1.0 / self._document_length
            if self.orientation() == constants.VERTICAL:
                rects = [
                    core.QRect(
                        x + 1,
                        y + h * start * scale - 0.5,
                        w - 2,
                        h * (end - start) * scale + 1,
                    )
                    for start, end in self._annotations
                ]
            else:
                rects = [
                    core.QRect(
                        x + w * start * scale - 0.5,
                        y + 1,
                        w * (end - start) * scale + 1,
                        h - 2,
                    )
                    for start, end in self._annotations
                ]
            p.drawRects(rects)

    def set_annotation_color(self, color: datatypes.ColorType):
        self._annotation_color = colors.get_color(color).as_qt()

    def get_annotation_color(self) -> gui.QColor:
        return self._annotation_color

    def set_document_length(self, length: int):
        self._document_length = length

    def get_document_length(self) -> int:
        return self._document_length

    annotation_color = core.Property(
        gui.QColor,
        get_annotation_color,
        set_annotation_color,
        doc="Color for the annotated regions",
    )
    annotations = core.Property(
        list,
        get_annotations,
        set_annotations,
        doc="Current set of annotations",
    )
    document_length = core.Property(
        int,
        get_document_length,
        set_document_length,
        doc="Total document length",
    )


if __name__ == "__main__":
    app = widgets.app()
    widget = widgets.PlainTextEdit("\n".join(str(i) for i in range(1000)))
    widget.v_scrollbar = AnnotatedScrollBar(constants.VERTICAL)
    widget.v_scrollbar.set_annotations([(10, 20), (50, 60), (82, 85)])
    widget.show()
    with app.debug_mode():
        app.exec()
