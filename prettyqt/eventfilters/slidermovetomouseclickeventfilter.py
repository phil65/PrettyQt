from __future__ import annotations

from prettyqt import constants, core, eventfilters, widgets

CC = widgets.QStyle.ComplexControl
SC = widgets.QStyle.SubControl


class SliderMoveToMouseClickEventFilter(eventfilters.BaseEventFilter):
    ID = "slider_move_to_mouse_click"

    def _move_to_mouse_position(
        self, scrollbar: widgets.QScrollBar, point: core.QPoint
    ):
        opt = widgets.StyleOptionSlider()
        scrollbar.initStyleOption(opt)
        control = scrollbar.style().hitTestComplexControl(
            CC.CC_ScrollBar, opt, point, scrollbar
        )
        if control not in {SC.SC_ScrollBarAddPage, SC.SC_ScrollBarSubPage}:
            return
        # scroll here
        gr = scrollbar.style().subControlRect(
            CC.CC_ScrollBar, opt, SC.SC_ScrollBarGroove, scrollbar
        )
        sr = scrollbar.style().subControlRect(
            CC.CC_ScrollBar, opt, SC.SC_ScrollBarSlider, scrollbar
        )
        if scrollbar.orientation() == constants.Orientation.Horizontal:
            pos = point.x()
            slider_length = sr.width()
            slider_min = gr.x()
            slider_max = gr.right() - slider_length + 1
            if scrollbar.layoutDirection() == constants.LayoutDirection.RightToLeft:
                opt.upsideDown = not opt.upsideDown
        else:
            pos = point.y()
            slider_length = sr.height()
            slider_min = gr.y()
            slider_max = gr.bottom() - slider_length + 1
        value = widgets.QStyle.sliderValueFromPosition(
            scrollbar.minimum(),
            scrollbar.maximum(),
            pos - slider_min - slider_length // 2,
            slider_max - slider_min,
            opt.upsideDown,
        )
        scrollbar.setValue(value)

    def eventFilter(self, source: widgets.QScrollBar, event: core.QEvent):
        match event.type():
            case core.QEvent.Type.MouseMove:
                if event.buttons() & constants.MouseButton.LeftButton:
                    point = event.position().toPoint()
                    self._move_to_mouse_position(source, point)
            case core.QEvent.Type.MouseButtonPress:
                if event.button() == constants.MouseButton.LeftButton:
                    point = event.position().toPoint()
                    self._move_to_mouse_position(source, point)
        return False


if __name__ == "__main__":
    app = widgets.app()
    widget = widgets.PlainTextEdit("gfdgdf\n" * 1000)
    eventfilter = SliderMoveToMouseClickEventFilter(widget.v_scrollbar)
    widget.v_scrollbar.installEventFilter(eventfilter)
    widget.show()
    app.exec()
