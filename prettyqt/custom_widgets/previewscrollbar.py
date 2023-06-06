from __future__ import annotations

from prettyqt import core, gui, widgets


class PreviewScrollBar(widgets.ScrollBar):
    def __init__(self, *args, parent=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._scrollarea = parent
        self._size = 150

    def sizeHint(self):
        expand = (
            core.QSize(self._size, 1) if self.is_vertical() else core.QSize(1, self._size)
        )
        return super().sizeHint().expandedTo(expand)

    def paintEvent(self, event):
        # viewport = self._scrollarea.viewport()
        doc = self._scrollarea.document()
        super().paintEvent(event)
        with gui.Painter(self) as painter:
            scale = max(self.height() / self._scrollarea.get_pixel_height(), 0.4)
            painter.scale(scale, scale)
            offset = 0
            block = doc.firstBlock()
            while block.isValid():
                r = self._scrollarea.blockBoundingRect(block)
                if not block.isVisible():
                    offset += r.height()
                    block = block.next()
                    continue
                else:
                    layout = block.layout()
                    layout.draw(painter, core.QPointF(0, offset))
                offset += r.height()
                block = block.next()


if __name__ == "__main__":
    app = widgets.app()
    widget = widgets.PlainTextEdit("\n".join(f"abc{i}" for i in range(1000)))
    widget.set_syntaxhighlighter("python")
    scrollbar = PreviewScrollBar("vertical", parent=widget)
    doc = widget.document()
    print(widget.viewport())
    print(widget.get_pixel_height())
    print(doc.pageSize())
    widget.setVerticalScrollBar(scrollbar)
    widget.show()
    with app.debug_mode():
        app.main_loop()
