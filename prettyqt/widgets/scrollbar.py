# -*- coding: utf-8 -*-
"""
"""

from typing import Union, Optional

from qtpy import QtCore, QtWidgets

from prettyqt import core, widgets
from prettyqt.utils import bidict


ORIENTATIONS = bidict(horizontal=QtCore.Qt.Horizontal, vertical=QtCore.Qt.Vertical)


QtWidgets.QScrollBar.__bases__ = (widgets.AbstractSlider,)


class ScrollBar(QtWidgets.QScrollBar):

    value_changed = core.Signal(int)

    def __init__(
        self,
        orientation: Union[int, str] = "horizontal",
        parent: Optional[QtWidgets.QWidget] = None,
    ):
        if orientation in ORIENTATIONS:
            orientation = ORIENTATIONS[orientation]
        super().__init__(orientation, parent)
        self.valueChanged.connect(self.on_value_change)
