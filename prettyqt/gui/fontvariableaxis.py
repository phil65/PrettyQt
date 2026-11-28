from prettyqt.qt import QtGui
from prettyqt.utils import get_repr


class FontVariableAxis(QtGui.QFontVariableAxis):
    """Represents a variable axis in a font."""

    def __repr__(self):
        return get_repr(
            self,
            self.name(),
            self.minimumValue(),
            self.maximumValue(),
            self.defaultValue(),
        )

    def get_tag(self) -> str:
        """Return the axis tag as a 4-character string."""
        return bytes(self.tag().toString().data()).decode()

    def set_tag(self, tag: str | QtGui.QFont.Tag):
        """Set the axis tag from a string or QFont.Tag."""
        if isinstance(tag, str):
            parsed = QtGui.QFont.Tag.fromString(tag)
            if parsed is None:
                raise ValueError(tag)
            tag = parsed
        self.setTag(tag)


if __name__ == "__main__":
    axis = FontVariableAxis()
    axis.set_tag("wght")
    print(repr(axis), axis.get_tag())
