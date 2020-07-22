# -*- coding: utf-8 -*-
"""
"""

from qtpy import QtCore, QtWidgets

from prettyqt import core, widgets
from prettyqt.utils import bidict


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
    def __getitem__(self, index):
        item = self.itemAt(index)
        widget = item.widget()
        if widget is None:
            widget = item.layout()
        return widget

    def __len__(self) -> int:
        return self.count()

    def __repr__(self):
        return f"{self.__class__.__name__}: {len(self)} children"

    def __iter__(self):
        return iter(self[i] for i in range(self.count()))

    def __contains__(self, item):
        return item in self.get_children()

    def get_children(self) -> list:
        return list(self)

    def set_margin(self, margin: int):
        self.setContentsMargins(margin, margin, margin, margin)

    def set_spacing(self, pixels: int):
        self.setSpacing(pixels)

    def set_size_mode(self, mode: str):
        """set the size mode of the layout

        Allowed values are "default", "fixed", "minimum", "maximum", "min_and_max", "none"

        Args:
            mode: size mode for the layout

        Raises:
            ValueError: size mode does not exist
        """
        if mode not in MODES:
            raise ValueError(f"{mode} not a valid size mode.")
        self.setSizeConstraint(MODES[mode])

    def get_size_mode(self) -> str:
        """returns current size mode

        Possible values: "default", "fixed", "minimum", "maximum", "min_and_max", "none"

        Returns:
            size mode
        """
        return MODES.inv[self.sizeConstraint()]

    def set_alignment(self, alignment: str, item=None):
        """Sets the alignment for widget / layout to alignment and
        returns true if w is found in this layout (not including child layouts)

        Allowed values for alignment:  "left", "right", "top", "bottom"

        Args:
            alignment: alignment for the layout
            item: set alignment for specific child only

        Raises:
            ValueError: alignment does not exist
        """
        if alignment not in ALIGNMENTS:
            raise ValueError(f"{alignment!r} not a valid alignment.")
        if item is not None:
            return self.setAlignment(item, ALIGNMENTS[alignment])
        else:
            return self.setAlignment(ALIGNMENTS[alignment])

    def add(self, *item):
        for i in item:
            if isinstance(i, QtWidgets.QWidget):
                self.addWidget(i)
            elif isinstance(i, QtWidgets.QLayout):
                w = widgets.Widget()
                w.set_layout(i)
                self.addWidget(w)
            else:
                raise TypeError("add_item only supports widgets and layouts")
