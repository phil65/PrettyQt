from typing import Optional, Union

from qtpy import QtLocation


class PlaceAttribute(QtLocation.QPlaceAttribute):
    def __init__(
        self,
        other_or_label: Union[None, str, QtLocation.QPlaceAttribute] = None,
        value: Optional[str] = None,
    ):
        if isinstance(other_or_label, QtLocation.QPlaceAttribute):
            super().__init__(other_or_label)
        else:
            super().__init__()
            self.setLabel(other_or_label)
            self.setText(value)

    def __repr__(self):
        return f"{type(self).__name__}({self.label()!r}, {self.text()!r})"

    def __str__(self):
        return f"{self.label()}: {self.text()}"

    def __bool__(self):
        return not self.isEmpty()


if __name__ == "__main__":
    attr = PlaceAttribute("test", "us")
    print(repr(attr))
