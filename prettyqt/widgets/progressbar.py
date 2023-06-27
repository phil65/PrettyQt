from __future__ import annotations

from typing import Literal

from prettyqt import constants, widgets
from prettyqt.qt import QtWidgets
from prettyqt.utils import bidict


TEXT_DIRECTIONS = bidict(
    top_to_bottom=QtWidgets.QProgressBar.Direction.TopToBottom,
    bottom_to_top=QtWidgets.QProgressBar.Direction.BottomToTop,
)

TextDirectionStr = Literal["top_to_bottom", "bottom_to_top"]


class ProgressBar(widgets.WidgetMixin, QtWidgets.QProgressBar):
    def __init__(self, *args, text_visible: bool = True, **kwargs):
        super().__init__(*args, text_visible=text_visible, **kwargs)

    def set_alignment(self, alignment: constants.AlignmentStr | constants.AlignmentFlag):
        """Set the alignment of the layout.

        Args:
            alignment: alignment for the layout
        """
        self.setAlignment(constants.ALIGNMENTS.get_enum_value(alignment))

    def get_alignment(self) -> constants.AlignmentStr:
        """Return current alignment.

        Returns:
            alignment
        """
        return constants.ALIGNMENTS.inverse[self.alignment()]

    def set_text_direction(
        self, text_direction: TextDirectionStr | QtWidgets.QProgressBar.Direction
    ):
        """Set the text direction of the layout.

        Args:
            text_direction: text direction for the layout
        """
        self.setTextDirection(TEXT_DIRECTIONS.get_enum_value(text_direction))

    def get_text_direction(self) -> TextDirectionStr:
        """Return current text direction.

        Returns:
            Text direction
        """
        return TEXT_DIRECTIONS.inverse[self.textDirection()]

    def set_orientation(
        self, orientation: constants.OrientationStr | constants.Orientation
    ):
        """Set the orientation of the progress bar.

        Args:
            orientation: orientation for the progress bar
        """
        self.setOrientation(constants.ORIENTATION.get_enum_value(orientation))

    def get_orientation(self) -> constants.OrientationStr:
        """Return current orientation.

        Returns:
            orientation
        """
        return constants.ORIENTATION.inverse[self.orientation()]

    def set_range(self, start: int, end: int):
        self.setRange(start, end)

    def set_value(self, value: int):
        self.setValue(value)

    def get_value(self) -> int:
        return self.value()


if __name__ == "__main__":
    app = widgets.app()
    widget = ProgressBar()
    widget.show()
    app.exec()
