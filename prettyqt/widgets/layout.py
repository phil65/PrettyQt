# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets, QtCore

from prettyqt import widgets, core
from prettyqt.utils import bidict


MODES = bidict(maximum=QtWidgets.QLayout.SetMaximumSize,
               fixed=QtWidgets.QLayout.SetFixedSize)

ALIGNMENTS = bidict(left=QtCore.Qt.AlignLeft,
                    right=QtCore.Qt.AlignRight,
                    top=QtCore.Qt.AlignTop,
                    bottom=QtCore.Qt.AlignBottom)


QtWidgets.QLayout.__bases__ = (core.Object, QtWidgets.QLayoutItem)


class Layout(QtWidgets.QLayout):

    def __repr__(self):
        return f"{self.__class__.__name__}: {len(self)} children"

    def set_margin(self, margin: int):
        self.setContentsMargins(margin, margin, margin, margin)

    def set_size_mode(self, mode: str):
        """set the size mode of the layout

        Allowed values are "maximum", "fixed"

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

        Possible values: "maximum", "fixed"

        Returns:
            size mode
        """
        return MODES.inv[self.sizeConstraint()]

    def set_alignment(self, alignment: str):
        """set the alignment of the layout

        Allowed values are "left", "right", "top", "bottom"

        Args:
            mode: alignment for the layout

        Raises:
            ValueError: alignment does not exist
        """
        if alignment not in ALIGNMENTS:
            raise ValueError(f"{alignment!r} not a valid alignment.")
        self.setAlignment(ALIGNMENTS[alignment])

    def get_alignment(self) -> str:
        """returns current alignment

        Possible values: "left", "right", "top", "bottom"

        Returns:
            alignment
        """
        return MODES.inv[self.alignment()]

    def add(self, item) -> int:
        if isinstance(item, QtWidgets.QWidget):
            return self.addWidget(item)
        elif isinstance(item, QtWidgets.QLayout):
            w = widgets.Widget()
            w.set_layout(item)
            return self.addWidget(w)
        else:
            raise TypeError("add_item only supports widgets and layouts")
