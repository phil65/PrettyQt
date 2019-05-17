# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from bidict import bidict

from qtpy import QtWidgets
from prettyqt import widgets

TICK_POSITIONS = bidict(dict(none=QtWidgets.QSlider.NoTicks,
                             both_sides=QtWidgets.QSlider.TicksBothSides,
                             above=QtWidgets.QSlider.TicksAbove,
                             below=QtWidgets.QSlider.TicksBelow))


class Slider(QtWidgets.QSlider):

    def __getstate__(self):
        return dict(range=(self.minimum(), self.maximum()),
                    value=self.value(),
                    tooltip=self.toolTip(),
                    statustip=self.statusTip(),
                    enabled=self.isEnabled(),
                    has_tracking=self.hasTracking(),
                    tick_position=self.get_tick_position(),
                    tick_interval=self.tickInterval(),
                    inverted_controls=self.invertedControls(),
                    inverted_appearance=self.invertedAppearance(),
                    single_step=self.singleStep(),
                    page_step=self.pageStep())

    def __setstate__(self, state):
        self.__init__()
        self.setRange(*state["range"])
        self.setValue(state["value"])
        self.setToolTip(state.get("tooltip", ""))
        self.setStatusTip(state.get("statustip", ""))
        self.setEnabled(state.get("enabled", True))
        self.setSingleStep(state["single_step"])
        self.setPageStep(state["page_step"])
        self.setTracking(state["has_tracking"])
        self.setInvertedControls(state["inverted_controls"])
        self.setInvertedAppearance(state["inverted_appearance"])
        self.set_tick_position(state["tick_position"])
        self.setTickInterval(state["tick_interval"])

    def set_tick_position(self, position: str):
        if position not in TICK_POSITIONS:
            raise ValueError(f"{position} not a valid tick position.")
        self.setTickPosition(TICK_POSITIONS[position])

    def get_tick_position(self) -> str:
        return TICK_POSITIONS.inv[self.tickPosition()]


Slider.__bases__[0].__bases__ = (widgets.AbstractSlider,)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    slider = Slider()
    slider.setRange(0, 100)
    slider.value_changed.connect(print)
    slider.show()
    app.exec_()
