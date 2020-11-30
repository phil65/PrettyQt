# -*- coding: utf-8 -*-

from typing import Union, Optional

from qtpy import QtCore, QtWidgets

from prettyqt import core, widgets
from prettyqt.utils import bidict, InvalidParamError


MODES = bidict(
    default=QtWidgets.QLayout.SetDefaultConstraint,
    fixed=QtWidgets.QLayout.SetFixedSize,
    minimum=QtWidgets.QLayout.SetMinimumSize,
    maximum=QtWidgets.QLayout.SetMaximumSize,
    min_and_max=QtWidgets.QLayout.SetMinAndMaxSize,
    none=QtWidgets.QLayout.SetNoConstraint,
)

ALIGNMENTS = bidict(
    left=QtCore.Qt.AlignLeft,
    right=QtCore.Qt.AlignRight,
    top=QtCore.Qt.AlignTop,
    bottom=QtCore.Qt.AlignBottom,
)


QtWidgets.QLayout.__bases__ = (core.Object, widgets.LayoutItem)


class Layout(QtWidgets.QLayout):
    def __getitem__(
        self, index: Union[str, int]
    ) -> Optional[Union[QtWidgets.QWidget, QtWidgets.QLayout]]:
        if isinstance(index, int):
            item = self.itemAt(index)
            widget = item.widget()
            if widget is None:
                widget = item.layout()
        elif isinstance(index, str):
            widget = self.find_child(typ=QtCore.QObject, name=index)
        return widget

    def __delitem__(self, index: int):
        item = self.itemAt(index)
        self.removeItem(item)

    def __len__(self) -> int:
        return self.count()

    def __repr__(self):
        return f"{self.__class__.__name__}()"

    def __iter__(self):
        return iter(self[i] for i in range(self.count()))

    def __contains__(self, item: Union[QtWidgets.QWidget, QtWidgets.QLayout]):
        return item in self.get_children()

    def serialize_fields(self):
        return dict(
            size_mode=self.get_size_mode(),
            spacing=self.spacing(),
            enabled=self.isEnabled(),
        )

    def get_children(self) -> list:
        return list(self)

    def set_margin(self, margin: int):
        self.setContentsMargins(margin, margin, margin, margin)

    def set_spacing(self, pixels: int):
        self.setSpacing(pixels)

    def set_size_mode(self, mode: str):
        """Set the size mode of the layout.

        Allowed values are "default", "fixed", "minimum", "maximum", "min_and_max", "none"

        Args:
            mode: size mode for the layout

        Raises:
            InvalidParamError: size mode does not exist
        """
        if mode not in MODES:
            raise InvalidParamError(mode, MODES)
        self.setSizeConstraint(MODES[mode])

    def get_size_mode(self) -> str:
        """Return current size mode.

        Possible values: "default", "fixed", "minimum", "maximum", "min_and_max", "none"

        Returns:
            size mode
        """
        return MODES.inv[self.sizeConstraint()]

    def set_alignment(
        self,
        alignment: str,
        item: Optional[Union[QtWidgets.QWidget, QtWidgets.QLayout]] = None,
    ):
        """Set the alignment for widget / layout to alignment.

        Returns true if w is found in this layout (not including child layouts).

        Allowed values for alignment:  "left", "right", "top", "bottom"

        Args:
            alignment: alignment for the layout
            item: set alignment for specific child only

        Raises:
            InvalidParamError: alignment does not exist
        """
        if alignment not in ALIGNMENTS:
            raise InvalidParamError(alignment, ALIGNMENTS)
        if item is not None:
            return self.setAlignment(item, ALIGNMENTS[alignment])
        else:
            return self.setAlignment(ALIGNMENTS[alignment])

    def add(self, *item: Union[QtWidgets.QWidget, QtWidgets.QLayout]):
        for i in item:
            if isinstance(i, QtWidgets.QWidget):
                self.addWidget(i)
            elif isinstance(i, QtWidgets.QLayout):
                w = widgets.Widget()
                w.set_layout(i)
                self.addWidget(w)
            else:
                raise TypeError("add_item only supports widgets and layouts")
