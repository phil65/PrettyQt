# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets, QtCore


class Slider(QtWidgets.QSlider):

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
