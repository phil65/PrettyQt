from __future__ import annotations

from typing import Literal

from prettyqt import constants, widgets
from prettyqt.qt import QtWidgets
from prettyqt.utils import InvalidParamError, bidict


TEXT_DIRECTIONS = bidict(
    top_to_bottom=QtWidgets.QProgressBar.Direction.TopToBottom,
    bottom_to_top=QtWidgets.QProgressBar.Direction.BottomToTop,
)

TextDirectionStr = Literal["top_to_bottom", "bottom_to_top"]


QtWidgets.QProgressBar.__bases__ = (widgets.Widget,)


class ProgressBar(QtWidgets.QProgressBar):
    """Progress dialog.

    wrapper for QtWidgets.QProgressBar
    """

    def __init__(
        self, text_visible: bool = True, parent: QtWidgets.QWidget | None = None
    ):
        super().__init__(parent=parent)
        self.setTextVisible(text_visible)

    def serialize_fields(self):
        return dict(
            alignment=self.get_alignment(),
            format=self.format(),
            # inverted_appearance=self.invertedAppearance(),
            minimum=self.minimum(),
            maximum=self.maximum(),
            orientation=self.get_orientation(),
            text=self.text(),
            # text_direction=self.get_text_direction(),
            text_visible=self.isTextVisible(),
            value=self.value(),
        )

    def set_alignment(self, alignment: constants.AlignmentStr):
        """Set the alignment of the layout.

        Args:
            alignment: alignment for the layout

        Raises:
            InvalidParamError: alignment does not exist
        """
        if alignment not in constants.ALIGNMENTS:
            raise InvalidParamError(alignment, constants.ALIGNMENTS)
        self.setAlignment(constants.ALIGNMENTS[alignment])

    def get_alignment(self) -> constants.AlignmentStr:
        """Return current alignment.

        Returns:
            alignment
        """
        return constants.ALIGNMENTS.inverse[self.alignment()]

    def set_text_direction(self, text_direction: TextDirectionStr):
        """Set the text direction of the layout.

        Args:
            text_direction: text direction for the layout

        Raises:
            InvalidParamError: text direction does not exist
        """
        if text_direction not in TEXT_DIRECTIONS:
            raise InvalidParamError(text_direction, TEXT_DIRECTIONS)
        self.setTextDirection(TEXT_DIRECTIONS[text_direction])

    def get_text_direction(self) -> TextDirectionStr:
        """Return current text direction.

        Returns:
            Text direction
        """
        return TEXT_DIRECTIONS.inverse[self.textDirection()]

    def set_orientation(self, orientation: constants.OrientationStr):
        """Set the orientation of the progress bar.

        Args:
            orientation: orientation for the progress bar

        Raises:
            InvalidParamError: orientation does not exist
        """
        if orientation not in constants.ORIENTATION:
            raise InvalidParamError(orientation, constants.ORIENTATION)
        self.setOrientation(constants.ORIENTATION[orientation])

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
    app.main_loop()
