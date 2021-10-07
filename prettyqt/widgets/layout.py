from __future__ import annotations

from typing import Literal

from prettyqt import constants, core, widgets
from prettyqt.qt import QtCore, QtWidgets
from prettyqt.utils import InvalidParamError, bidict


SIZE_CONSTRAINT = bidict(
    default=QtWidgets.QLayout.SizeConstraint.SetDefaultConstraint,
    fixed=QtWidgets.QLayout.SizeConstraint.SetFixedSize,
    minimum=QtWidgets.QLayout.SizeConstraint.SetMinimumSize,
    maximum=QtWidgets.QLayout.SizeConstraint.SetMaximumSize,
    min_and_max=QtWidgets.QLayout.SizeConstraint.SetMinAndMaxSize,
    none=QtWidgets.QLayout.SizeConstraint.SetNoConstraint,
)

SizeConstraintStr = Literal[
    "default", "fixed", "minimum", "maximum", "min_and_max", "none"
]


QtWidgets.QLayout.__bases__ = (core.Object, widgets.LayoutItem)


class Layout(QtWidgets.QLayout):
    def __getitem__(
        self, index: str | int
    ) -> QtWidgets.QWidget | QtWidgets.QLayout | None:
        if isinstance(index, int):
            item = self.itemAt(index)
            widget = item.widget()
            if widget is None:
                widget = item.layout()
        elif isinstance(index, str):
            return self.find_child(typ=QtCore.QObject, name=index)
        return widget

    def __delitem__(self, index: int):
        item = self.itemAt(index)
        self.removeItem(item)

    def __len__(self) -> int:
        return self.count()

    def __repr__(self):
        return f"{type(self).__name__}()"

    def __iter__(self):
        return iter(self[i] for i in range(self.count()))

    def __contains__(self, item: QtWidgets.QWidget | QtWidgets.QLayoutItem):
        return self.indexOf(item) >= 0

    def serialize_fields(self):
        return dict(
            size_mode=self.get_size_mode(),
            spacing=self.spacing(),
            enabled=self.isEnabled(),
        )

    def get_children(self) -> list[QtWidgets.QWidget | QtWidgets.QLayout]:
        return list(self)

    def set_margin(self, margin: int):
        self.setContentsMargins(margin, margin, margin, margin)

    def set_spacing(self, pixels: int):
        self.setSpacing(pixels)

    def set_size_mode(self, mode: SizeConstraintStr):
        """Set the size mode of the layout.

        Args:
            mode: size mode for the layout

        Raises:
            InvalidParamError: size mode does not exist
        """
        if mode not in SIZE_CONSTRAINT:
            raise InvalidParamError(mode, SIZE_CONSTRAINT)
        self.setSizeConstraint(SIZE_CONSTRAINT[mode])

    def get_size_mode(self) -> SizeConstraintStr:
        """Return current size mode.

        Returns:
            size mode
        """
        return SIZE_CONSTRAINT.inverse[self.sizeConstraint()]

    def set_alignment(
        self,
        alignment: constants.AlignmentStr,
        item: QtWidgets.QWidget | QtWidgets.QLayout | None = None,
    ):
        """Set the alignment for widget / layout to alignment.

        Returns true if w is found in this layout (not including child layouts).

        Args:
            alignment: alignment for the layout
            item: set alignment for specific child only

        Raises:
            InvalidParamError: alignment does not exist
        """
        if alignment not in constants.ALIGNMENTS:
            raise InvalidParamError(alignment, constants.ALIGNMENTS)
        if item is not None:
            return self.setAlignment(item, constants.ALIGNMENTS[alignment])
        else:
            return self.setAlignment(constants.ALIGNMENTS[alignment])

    def add(self, *item: QtWidgets.QWidget | QtWidgets.QLayout):
        for i in item:
            if isinstance(i, QtWidgets.QWidget):
                self.addWidget(i)
            elif isinstance(i, QtWidgets.QLayout):
                w = widgets.Widget()
                w.set_layout(i)
                self.addWidget(w)
            else:
                raise TypeError("add_item only supports widgets and layouts")
