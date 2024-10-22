from __future__ import annotations

import os

from prettyqt import constants, gui, widgets
from prettyqt.utils import datatypes


class SplashScreenMixin(widgets.WidgetMixin):
    def __init__(self, *args, **kwargs):
        match args:
            case (os.PathLike(), *rest):
                super().__init__(gui.Pixmap(os.fspath(args[0])), *rest, **kwargs)
            case _:
                super().__init__(*args, **kwargs)
        self.set_flags(stay_on_top=True, frameless=True)
        self.setEnabled(False)

    def __enter__(self):
        self.show()
        return self

    def __exit__(self, typ, value, traceback):
        self.hide()

    def setPixmap(self, pixmap: str | os.PathLike[str] | gui.QPixmap | None):
        match pixmap:
            case os.PathLike():
                pixmap = gui.Pixmap(os.fspath(pixmap))
            case None:
                pixmap = gui.Pixmap()
        super().setPixmap(pixmap)

    def set_pixmap_width(self, width: int):
        pixmap = self.pixmap()
        pixmap = pixmap.scaledToWidth(width)
        super().setPixmap(pixmap)

    def show_message(
        self,
        text: str,
        color: datatypes.ColorType = "black",
        h_align: constants.HorizontalAlignmentStr = "center",
        v_align: constants.VerticalAlignmentStr = "bottom",
    ):
        super().showMessage(
            text,
            color=gui.Color(color),
            alignment=constants.H_ALIGNMENT[h_align] | constants.V_ALIGNMENT[v_align],
        )


class SplashScreen(SplashScreenMixin, widgets.QSplashScreen):
    """Splash screen that can be shown during application startup."""


if __name__ == "__main__":
    app = widgets.app()
    splash = SplashScreen(gui.Pixmap())
    splash.show()
    splash.show_message("test")
    app.exec()
