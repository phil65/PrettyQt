from __future__ import annotations

from prettyqt import eventfilters
from prettyqt.qt import QtCore, QtWidgets

CC = QtWidgets.QStyle.ComplexControl
SC = QtWidgets.QStyle.SubControl


class SliderMoveToMouseClickEventFilter(eventfilters.BaseEventFilter):
    def _move_to_mouse_position(self, scrollbar, point: QtCore.QPoint):
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
        if scrollbar.orientation() == QtCore.Qt.Orientation.Horizontal:
            pos = point.x()
            slider_length = sr.width()
            slider_min = gr.x()
            slider_max = gr.right() - slider_length + 1
            if scrollbar.layoutDirection() == QtCore.Qt.LayoutDirection.RightToLeft:
                opt.upsideDown = not opt.upsideDown
        else:
            pos = point.y()
            slider_length = sr.height()
            slider_min = gr.y()
            slider_max = gr.bottom() - slider_length + 1
        scrollbar.setValue(
            QtWidgets.QStyle.sliderValueFromPosition(
                scrollbar.minimum(),
                scrollbar.maximum(),
                pos - slider_min - slider_length // 2,
                slider_max - slider_min,
                opt.upsideDown,
            )
        )

    def eventFilter(self, source, event):
        match event.type():
            case QtCore.QEvent.Type.MouseMove:
                if event.buttons() & QtCore.Qt.MouseButton.LeftButton:
                    point = event.position().toPoint()
                    self._move_to_mouse_position(source, point)
            case QtCore.QEvent.Type.MouseButtonPress:
                if event.button() == QtCore.Qt.MouseButton.LeftButton:
                    point = event.position().toPoint()
                    self._move_to_mouse_position(source, point)
        return False


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    widget = widgets.PlainTextEdit("gfdgdf\n" * 1000)
    eventfilter = SliderMoveToMouseClickEventFilter(widget.v_scrollbar)
    widget.v_scrollbar.installEventFilter(eventfilter)
    widget.show()
    app.main_loop()