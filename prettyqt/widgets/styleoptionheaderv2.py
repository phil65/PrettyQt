from prettyqt import constants, widgets


class StyleOptionHeaderV2(widgets.StyleOptionHeaderMixin, widgets.QStyleOptionHeaderV2):
    """Describes the parameters for drawing a header (v2)."""

    def get_text_elide_mode(self) -> constants.TextElideModeStr:
        """Return text elide mode."""
        return constants.TEXT_ELIDE_MODE.inverse[self.textElideMode]
