from __future__ import annotations

import logging
from typing import Literal

from prettyqt import core

logger = logging.getLogger(__name__)

NameFormatStr = Literal["hex_rgb", "hex_argb"]
NameStr = NameFormatStr | Literal["svg_rgb", "svg_argb", "qcss_rgb", "qcss_argb"]


class TextAnimation(core.PropertyAnimation):
    ID = "text"

    def __init__(
        self,
        start,
        end,
        duration: int = 1000,
        easing: core.easingcurve.TypeStr = "in_out_sine",
        fmt: NameStr = "html",
        mask: str = "{text}",
        parent: core.QObject | None = None,
    ):
        self._fmt = fmt
        super().__init__(parent)
        self.set_easing(easing)
        self.set_duration(duration)
        self._child_anim = core.VariantAnimation()
        self._child_anim.set_easing(easing)
        self._child_anim.set_start_value(start)
        self._child_anim.set_end_value(end)
        self._child_anim.set_duration(duration)
        self._child_anim.valueChanged.connect(self.updateCurrentValue)
        self._child_anim.start()
        self._mask = mask
        self.set_start_value("")
        self.set_end_value("")

    def start(self, *args, **kwargs):
        # self._child_anim.start(*args, **kwargs)
        super().start(*args, **kwargs)

    def updateCurrentValue(self, value):
        match value:
            case None:
                return
            case gui.QColor():
                color = gui.Color(value)
                text = color.get_name(self._fmt) if self._fmt else color.toString()
                value = self._mask.format(text=text)
            case int() | float():
                value = self._mask.format(text=str(value))
            case core.QPoint() | core.QPointF():
                return f"{value.x()}, {value.y()}"
            case core.QSize() | core.QSizeF():
                return f"{value.width()}, {value.width()}"
        logger.debug(value)
        super().updateCurrentValue(value)


if __name__ == "__main__":
    from prettyqt import gui, widgets

    app = widgets.app()
    w = widgets.RadioButton()
    mask = "QWidget {{background-color:{text};}}"
    anim = TextAnimation(
        gui.QColor("red"), gui.QColor("blue"), parent=w, mask=mask, fmt="qcss_rgb"
    )
    anim.apply_to(w.styleSheet)
    anim.start()
    w.show()
    with app.debug_mode():
        app.main_loop()
