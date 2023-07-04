from __future__ import annotations

from prettyqt import constants, core, custom_models, gui
from prettyqt.utils import colors, datatypes


class SliceAppearanceProxyModel(custom_models.SliceIdentityProxyModel):
    ID = "slice_appearance"
    ICON = "mdi.palette-outline"

    def __init__(
        self,
        foreground: gui.QColor | gui.QBrush | str | None = None,
        background: gui.QColor | gui.QBrush | str | None = None,
        font: str | gui.QFont | None = None,
        alignment: constants.AlignmentFlag | constants.AlignmentStr | None = None,
        override: bool = True,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self._foreground = gui.QColor()
        self.set_foreground(foreground)
        self._background = gui.QColor()
        self.set_background(background)
        self._font = gui.QFont()
        self.set_font(font)
        self._alignment = constants.ALIGN_CENTER_LEFT
        self.set_alignment(alignment)
        self._override = override

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
                    return self._foreground if self._foreground.isValid() else None
                case constants.BACKGROUND_ROLE:
                    return self._background if self._background.isValid() else None
                case constants.FONT_ROLE:
                    return self._font
                case constants.ALIGNMENT_ROLE:
                    return self._alignment
        return super().data(index, role)

    def set_font(self, font: gui.QFont | str | None):
        self._font = gui.QFont(font) if font else gui.QFont()
        self.update_all()

    def get_font(self) -> gui.QFont:
        return self._font or gui.QFont()

    def set_foreground(self, foreground: datatypes.ColorAndBrushType | None):
        match foreground:
            case None:
                foreground = gui.QColor()
            case gui.QBrush():
                foreground = foreground.color()
            case _:
                foreground = colors.get_color(foreground).as_qt()
        self._foreground = foreground
        self.update_all()

    def get_foreground(self) -> gui.QColor:
        return self._foreground

    def set_background(self, background: datatypes.ColorAndBrushType | None):
        match background:
            case None:
                background = gui.QColor()
            case gui.QBrush():
                background = background.color()
            case _:
                background = colors.get_color(background).as_qt()
        self._background = background
        self.update_all()

    def get_background(self) -> gui.QColor:
        return self._background

    def set_alignment(
        self, alignment: constants.AlignmentFlag | constants.AlignmentStr | None
    ):
        match alignment:
            case None:
                alignment = constants.ALIGN_CENTER_LEFT
            case str() | constants.AlignmentFlag():
                alignment = constants.ALIGNMENTS.get_enum_value(alignment)
        self._alignment = alignment
        self.update_all()

    def get_alignment(self) -> constants.AlignmentFlag:
        return self._alignment

    font_value = core.Property(gui.QFont, get_font, set_font)
    foreground_value = core.Property(gui.QColor, get_foreground, set_foreground)
    background_value = core.Property(gui.QColor, get_background, set_background)
    alignment_value = core.Property(constants.AlignmentFlag, get_alignment, set_alignment)


if __name__ == "__main__":
    from prettyqt import debugging, gui, widgets

    app = widgets.app()
    table = debugging.example_table()
    table.proxifier[:, 1].style()
    table.show()
    with app.debug_mode():
        app.exec()
