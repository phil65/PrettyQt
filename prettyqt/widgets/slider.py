# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtCore, QtWidgets
from prettyqt import core

TICK_POSITIONS = dict(none=QtWidgets.QSlider.NoTicks,
                      both_sides=QtWidgets.QSlider.NoTicks,
                      above=QtWidgets.QSlider.NoTicks,
                      below=QtWidgets.QSlider.NoTicks,
                      left=QtWidgets.QSlider.NoTicks,
                      right=QtWidgets.QSlider.NoTicks)


class Slider(QtWidgets.QSlider):

    value_changed = core.Signal(int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.valueChanged.connect(self.value_changed)

    def __getstate__(self):
        return dict(range=(self.minimum(), self.maximum()),
                    value=self.value(),
                    tooltip=self.toolTip(),
                    statustip=self.statusTip(),
                    enabled=self.isEnabled(),
                    has_tracking=self.hasTracking(),
                    inverted_controls=self.invertedControls(),
                    inverted_appearance=self.invertedAppearance(),
                    single_step=self.singleStep(),
                    page_step=self.pageStep())

    def __setstate__(self, state):
        super().__init__()
        self.setRange(*state["range"])
        self.setValue(state["value"])
        self.setToolTip(state["tooltip"])
        self.setStatusTip(state["statustip"])
        self.setEnabled(state["enabled"])
        self.setSingleStep(state["single_step"])
        self.setPageStep(state["page_step"])
        self.setTracking(state["has_tracking"])
        self.setInvertedControls(state["inverted_controls"])
        self.setInvertedAppearance(state["inverted_appearance"])

    def is_horizontal(self) -> bool:
        """check if silder is horizontal

        Returns:
            True if horizontal, else False
        """
        return self.orientation() == QtCore.Qt.Horizontal

    def is_vertical(self) -> bool:
        """check if silder is vertical

        Returns:
            True if vertical, else False
        """
        return self.orientation() == QtCore.Qt.Vertical

    def set_horizontal(self):
        """set slider orientation to horizontal
        """
        self.setOrientation(QtCore.Qt.Horizontal)

    def set_vertical(self):
        """set slider orientation to vertical
        """
        self.setOrientation(QtCore.Qt.Vertical)

    def set_tick_position(self, position: str):
        if position not in TICK_POSITIONS:
            raise ValueError(f"{position} not a valid tick position.")
        self.setTickPosition(TICK_POSITIONS[position])

    def get_value(self):
        return self.value()
