# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from bidict import bidict

from qtpy import QtCore, QtWidgets
from prettyqt import core, widgets

TICK_POSITIONS = bidict(dict(none=QtWidgets.QSlider.NoTicks,
                             both_sides=QtWidgets.QSlider.TicksBothSides,
                             above=QtWidgets.QSlider.TicksAbove,
                             below=QtWidgets.QSlider.TicksBelow))


class AbstractSlider(QtWidgets.QAbstractSlider):

    value_changed = core.Signal(int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.valueChanged.connect(self.on_value_change)

    def on_value_change(self):
        self.value_changed.emit(self.value())

    def __getstate__(self):
        return dict(range=(self.minimum(), self.maximum()),
                    value=self.value(),
                    has_tracking=self.hasTracking(),
                    inverted_controls=self.invertedControls(),
                    inverted_appearance=self.invertedAppearance(),
                    single_step=self.singleStep(),
                    page_step=self.pageStep())

    def __setstate__(self, state):
        self.__init__()
        self.setRange(*state["range"])
        self.setValue(state["value"])
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

    def get_value(self):
        return self.value()

    def set_value(self, value: int):
        return self.set_value()


AbstractSlider.__bases__[0].__bases__ = (widgets.Widget,)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    slider = AbstractSlider()
    slider.setRange(0, 100)
    slider.value_changed.connect(print)
    slider.show()
    app.exec_()
