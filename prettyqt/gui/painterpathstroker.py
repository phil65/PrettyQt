from __future__ import annotations

from prettyqt import constants, gui


class PainterPathStroker(gui.QPainterPathStroker):
    def set_cap_style(self, style: constants.CapStyleStr | constants.PenCapStyle):
        """Set cap style to use.

        Args:
            style: cap style to use
        """
        self.setCapStyle(constants.CAP_STYLE.get_enum_value(style))

    def get_cap_style(self) -> constants.CapStyleStr | constants.PenCapStyle:
        """Return current cap style.

        Returns:
            cap style
        """
        return constants.CAP_STYLE.inverse[self.capStyle()]

    def set_join_style(self, style: constants.JoinStyleStr | constants.PenJoinStyle):
        """Set join style to use.

        Args:
            style: join style to use
        """
        self.setJoinStyle(constants.JOIN_STYLE.get_enum_value(style))

    def get_join_style(self) -> constants.JoinStyleStr:
        """Return current join style.

        Returns:
            join style
        """
        return constants.JOIN_STYLE.inverse[self.joinStyle()]

    def create_stroke(self, path: gui.QPainterPath) -> gui.PainterPath:
        return gui.PainterPath(self.createStroke(path))


if __name__ == "__main__":
    p = PainterPathStroker()
