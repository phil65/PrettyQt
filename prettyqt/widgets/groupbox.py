from __future__ import annotations

from prettyqt import constants, widgets
from prettyqt.utils import get_repr


class GroupBox(widgets.WidgetMixin, widgets.QGroupBox):
    """Group box frame with a title.

    A group box provides a frame, a title on top, a keyboard shortcut,
    and displays various other widgets inside itself.
    The keyboard shortcut moves keyboard focus to one of the group box's child widgets.
    """

    def __repr__(self):
        return get_repr(self, self.title())

    def set_title(self, title: str):
        self.setTitle(title)

    def set_alignment(
        self, alignment: constants.HorizontalAlignmentStr | constants.AlignmentFlag
    ):
        """Set the title alignment of the groupbox.

        Args:
            alignment: title alignment for the groupbox
        """
        self.setAlignment(constants.H_ALIGNMENT.get_enum_value(alignment))

    def get_alignment(self) -> constants.HorizontalAlignmentStr:
        """Return current title alignment.

        Returns:
            title alignment
        """
        return constants.H_ALIGNMENT.inverse[self.alignment()]

    def set_enabled(self, state):
        for widget in self.layout():
            widget.setEnabled(state)


if __name__ == "__main__":
    app = widgets.app()
    widget = GroupBox()
    ly = widgets.HBoxLayout()
    ly += widgets.RadioButton("test")
    widget.set_layout(ly)
    widget.show()
    app.exec()
