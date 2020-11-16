# -*- coding: utf-8 -*-

from typing import Union, Optional

from qtpy import QtLocation


class PlaceContactDetail(QtLocation.QPlaceContactDetail):
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
            self.setValue(value)

    def __repr__(self):
        return f"{type(self).__name__}({self.label()!r}, {self.value()!r})"

    def __str__(self):
        return f"{self.label()}: {self.value()}"


if __name__ == "__main__":
    detail = PlaceContactDetail("a", "b")
    print(repr(detail))
    print(detail.Email)
