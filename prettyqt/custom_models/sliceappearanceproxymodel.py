from __future__ import annotations

from prettyqt import constants, core, gui, custom_models


class SliceAppearanceProxyModel(custom_models.SliceIdentityProxyModel):
    ID = "slice_appearance"

    def __init__(
        self,
        foreground=None,
        background=None,
        font=None,
        alignment=None,
        override: bool = True,
        **kwargs,
    ):
        self._foreground = foreground
        self._background = background
        self._font = font
        self._alignment = alignment
        self._override = override
        super().__init__(**kwargs)

    def data(
        self,
        index: core.ModelIndex,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ):
        data = super().data(index, role)
        if not self.indexer_contains(index):
            return data
        if self._override or data is None:
            match role:
                case constants.FOREGROUND_ROLE:
                    return self._foreground
                case constants.BACKGROUND_ROLE:
                    return self._background
                case constants.FONT_ROLE:
                    return self._font
                case constants.ALIGNMENT_ROLE:
                    return self._alignment
        return super().data(index, role)

    def set_font(self, font: gui.QFont | str):
        self._font = gui.QFont(font)
        self.update_all()

    def get_font(self) -> gui.QFont:
        return self._font

    def set_foreground(self, foreground: gui.QColor | gui.QBrush | str):
        if isinstance(foreground, str):
            foreground = gui.QColor(foreground)
        self._foreground = foreground
        self.update_all()

    def get_foreground(self) -> gui.QColor:
        return self._foreground

    def set_background(self, background: gui.QColor | gui.QBrush | str):
        if isinstance(background, str):
            background = gui.QColor(background)
        self._background = background
        self.update_all()

    def get_background(self) -> gui.QFont:
        return self._background

    def set_alignment(
        self, alignment: constants.AlignmentFlag | constants.AlignmentStr
    ):
        if isinstance(alignment, str):
            alignment = constants.ALIGNMENTS[alignment]
        self._alignment = alignment
        self.update_all()

    def get_alignment(self) -> constants.AlignmentFlag:
        return self._alignment

    font_value = core.Property(gui.QFont, get_font, set_font)
    foreground_value = core.Property(
        object, get_foreground, set_foreground
    )
    background_value = core.Property(
        object, get_background, set_background
    )
    alignment_value = core.Property(
        constants.AlignmentFlag, get_alignment, set_alignment
    )


if __name__ == "__main__":
    from prettyqt import debugging, gui, widgets

    app = widgets.app()
    table = debugging.example_table()
    table.proxifier[:, 0].style(foreground="red")
    table.show()
    with app.debug_mode():
        app.main_loop()
