from __future__ import annotations

import logging
from typing import Literal

from prettyqt import core
from prettyqt.utils import datatypes

logger = logging.getLogger(__name__)

NameFormatStr = Literal["hex_rgb", "hex_argb"]
NameStr = NameFormatStr | Literal["svg_rgb", "svg_argb", "qcss_rgb", "qcss_argb"]


class TextAnimation(core.PropertyAnimation):
    ID = "text"

    def __init__(
        self,
        start: datatypes.VariantType | None = None,
        end: datatypes.VariantType | None = None,
        duration: int = 1000,
        easing: core.easingcurve.TypeStr = "in_out_sine",
        fmt: NameStr = "html",
        mask: str = "{text}",
        parent: core.QObject | None = None,
    ):
        self._fmt = fmt
        self._mask = mask
        super().__init__(parent)
        self._child_anim = core.VariantAnimation()
        self._child_anim.valueChanged.connect(self.updateCurrentValue)
        self.set_easing(easing)
        self.set_duration(duration)
        if start is not None:
            self._child_anim.set_start_value(start)
        if end is not None:
            self._child_anim.set_end_value(end)
        self.setStartValue("")
        self.setStartValue("")

    def start(self, *args, **kwargs):
        self._child_anim.start(*args, **kwargs)
        super().start(*args, **kwargs)

    # TODO: also do stop etc.

    def set_start_value(self, value: datatypes.VariantType):
        self._child_anim.set_start_value(value)

    def set_end_value(self, value: datatypes.VariantType):
        self._child_anim.set_end_value(value)

    def set_easing(self, easing: core.easingcurve.TypeStr | core.QEasingCurve.Type):
        super().set_easing(easing)
        self._child_anim.set_easing(easing)

    def set_duration(self, duration: int):
        super().setDuration(duration)
        self._child_anim.set_duration(duration)

    def updateCurrentValue(self, value: datatypes.VariantType):
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
        app.exec()
