from __future__ import annotations

from prettyqt import core, gui, widgets


class PreviewScrollBar(widgets.ScrollBar):
    def __init__(self, *args, parent=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._scrollarea = parent
        self._size = 150
        self._line_margin = 160
        self._scale = 0.3
        self.installEventFilter("slider_move_to_mouse_click")

    def sizeHint(self):
        expand = (
            core.QSize(self._size, 1) if self.is_vertical() else core.QSize(1, self._size)
        )
        return super().sizeHint().expandedTo(expand)

    def paintEvent(self, event):
        # viewport = self._scrollarea.viewport()
        doc = self._scrollarea.document()
        v_scroll = self._scrollarea.v_scrollbar
        super().paintEvent(event)
        with gui.Painter(self) as painter:
            painter.save()
            bg_color = gui.Palette().get_color("window")
            painter.setBrush(bg_color)
            painter.drawRect(self.geometry())
            painter.restore()
            painter.save()
            # scale = self.height() / self._scrollarea.get_pixel_height()
            first_vis_line, last_vis_line = self._scrollarea.get_visible_line_span()
            start_line = max(0, first_vis_line - self._line_margin)
            end_line = min(last_vis_line + self._line_margin, doc.blockCount())
            start_block = doc.findBlockByLineNumber(start_line)
            end_block = doc.findBlockByLineNumber(end_line)
            painter.scale(self._scale, self._scale)
            offset = 0
            while start_block != end_block:
                r = self._scrollarea.blockBoundingRect(start_block)
                if not start_block.isVisible():
                    offset += r.height()
                    start_block = start_block.next()
                    continue
                else:
                    layout = start_block.layout()
                    layout.draw(painter, core.QPointF(0, offset))
                offset += r.height()
                start_block = start_block.next()
            painter.restore()
            # pos = v_scroll.value() / v_scroll.maximum()
            rect_height = (
                (last_vis_line - first_vis_line) / doc.blockCount() * v_scroll.height()
            )
            rect_y_pos = first_vis_line / doc.blockCount() * v_scroll.height()
            painter.setBrush(gui.QColor(120, 120, 120, 120))
            painter.drawRoundedRect(
                0, int(rect_y_pos), self._size, int(rect_height), 5, 5
            )


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
