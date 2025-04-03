from __future__ import annotations

from prettyqt import core, gui, widgets


class PreviewScrollBar(widgets.ScrollBar):
    """Scrollbar showing a small preview of a (Plain)TextEdit."""

    def __init__(self, *args, parent=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._scrollarea = parent
        self._width = 150
        # self._line_margin = 152
        self._scale = 0.3
        # self.installEventFilter("slider_move_to_mouse_click")

    @classmethod
    def setup_example(cls):
        w = widgets.PlainTextEdit()
        return cls(parent=w)

    def sizeHint(self):
        expand = (
            core.QSize(self._width, 1)
            if self.is_vertical()
            else core.QSize(1, self._width)
        )
        return super().sizeHint().expandedTo(expand)

    def paintEvent(self, event):
        # viewport = self._scrollarea.viewport()
        doc = self._scrollarea.document()
        v_scroll = self._scrollarea.v_scrollbar
        super().paintEvent(event)
        with gui.Painter(self) as painter:
            painter.setRenderHint(painter.RenderHint.TextAntialiasing, True)

            # draw background
            painter.save()
            bg_color = gui.Palette().get_color("window")
            painter.setBrush(bg_color)
            painter.drawRect(self.geometry())
            painter.restore()

            # figure out positions
            painter.save()
            first_vis_line, last_vis_line = self._scrollarea.get_visible_line_span()
            # start_line = max(0, first_vis_line - self._line_margin)
            # end_line = min(last_vis_line + self._line_margin, doc.blockCount())
            # start_block = doc.findBlockByLineNumber(start_line)
            # end_block = doc.findBlockByLineNumber(end_line)
            opt = widgets.QStyleOptionSlider()
            opt.initFrom(self)
            opt.subControls = widgets.QStyle.SubControl.SC_None
            opt.activeSubControls = widgets.QStyle.SubControl.SC_None
            opt.orientation = self.orientation()
            opt.minimum = self.minimum()
            opt.maximum = self.maximum()
            opt.sliderPosition = self.sliderPosition()
            opt.sliderValue = self.value()
            opt.singleStep = self.singleStep()
            opt.pageStep = self.pageStep()
            gr = self.style().subControlRect(
                widgets.QStyle.ComplexControl.CC_ScrollBar,
                opt,
                widgets.QStyle.SubControl.SC_ScrollBarGroove,
                self,
            )
            textarea_height = 0
            b = doc.begin()
            while b != doc.end():
                r = self._scrollarea.blockBoundingRect(b)
                textarea_height += r.height()
                b = b.next()
            minimap_height = textarea_height * self._scale
            minimap_visible_height = min(minimap_height, v_scroll.height())
            # minimap_fully_visible = minimap_visible_height == minimap_height
            height_ratio = minimap_height / v_scroll.height()
            map_scroll_distance = minimap_height - minimap_visible_height
            if v_scroll.maximum():
                scroll_per_value = map_scroll_distance / v_scroll.maximum()
            else:
                scroll_per_value = 1
            # doc_x_margin = 1
            # doc_height = min(gr.height(), textarea_height)
            # yoffset = 1  # top instead of center-aligned (gr.height() - doc_height) / 2
            # doc_rect = core.QRect(
            #     core.QPoint(gr.left() + doc_x_margin, yoffset + gr.top()),
            #     QSize(gr.width() - doc_x_margin, doc_height),
            # )
            # self.map_grove_rect = doc_rect

            # max_ = max(self.maximum() + 1, 1)
            # visible_start = (
            #     self.value() * doc_height / (max_ + self.pageStep())
            #     + doc_rect.top()
            #     + 0.5
            # )
            # visible_end = (self.value() + self.pageStep()) * doc_height / (
            #     max_ + self.pageStep()
            # ) + doc_rect.top()
            # visible_rect = core.QRect(doc_rect)
            # visible_rect.moveTop(visible_start)
            # visible_rect.setHeight(visible_end - visible_start)
            # #  adjust the rectangles
            # slider_rect = self.style().subControlRect(QStyle.CC_ScrollBar, opt,
            # QStyle.SC_ScrollBarSlider, self)
            # slider_rect.setX(doc_x_margin)
            # slider_rect.setWidth(self.width() - doc_x_margin * 2)

            # if ((doc_height + 2 * doc_x_margin >= gr.height()) and
            # (slider_rect.height() > visible_rect.height() + 2))
            #     visible_rect.adjust(2, 0, -3, 0)
            #  else:
            #     visible_rect.adjust(1, 0, -1, 2)
            #     slider_rect.setTop(visible_rect.top() - 1)
            #     slider_rect.setBottom(visible_rect.bottom() + 1)

            painter.scale(self._scale, self._scale)
            offset = -(
                v_scroll.value() * scroll_per_value * (1 / self._scale)
            )  # height_ratio * (1/self._scale))
            # scale = self.height() / self._scrollarea.get_pixel_height()
            b = doc.begin()
            top = v_scroll.height() * (1 / self._scale)
            count = 0
            while b != doc.end():
                r = self._scrollarea.blockBoundingRect(b)
                if b.isVisible() and top >= offset >= 0:
                    layout = b.layout()
                    count += 1
                    layout.draw(painter, core.QPointF(0, offset))
                offset += r.height()
                b = b.next()
            painter.restore()
            # pos = v_scroll.value() / v_scroll.maximum()
            painter.setBrush(gui.QColor(120, 120, 120, 120))
            # slider_rect = self.style().subControlRect(
            #     widgets.QStyle.ComplexControl.CC_ScrollBar,
            #     opt,
            #     widgets.QStyle.SubControl.SC_ScrollBarSlider,
            #     self,
            # )
            handle_rect_height = (
                (last_vis_line - first_vis_line)
                / doc.blockCount()
                * gr.height()
                * height_ratio
            )

            handle_rect_y_pos = first_vis_line / doc.blockCount() * gr.height()
            handle_rect_y_pos *= v_scroll.height() / (
                v_scroll.height() + handle_rect_height
            )

            painter.drawRoundedRect(
                0, int(handle_rect_y_pos), self._width, int(handle_rect_height), 5, 5
            )

    def minimap_y_to_std_y(self, y: int) -> int:
        #  Check if the minimap fills the whole scrollbar
        if self.std_grove_rect.height() == self.map_grove_rect.height():
            return y
        #  check if y is on the step up/down
        if (y < self.std_grove_rect.top()) or (y > self.std_grove_rect.bottom()):
            return y
        if y < self.map_grove_rect.top():
            return self.std_grove_rect.top() + 1
        if y > self.map_grove_rect.bottom():
            return self.std_grove_rect.bottom() - 1
        #  check for div/0
        if self.map_grove_rect.height() == 0:
            return y
        new_y = (
            (y - self.map_grove_rect.top())
            * self.std_grove_rect.height()
            / self.map_grove_rect.height()
        )
        new_y += self.std_grove_rect.top()
        return new_y


if __name__ == "__main__":
    app = widgets.app()
    app.set_style("fusion")
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
        app.exec()
