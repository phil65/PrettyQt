# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from bidict import bidict

from qtpy import QtWidgets
from prettyqt import widgets


VIEW_MODES = bidict(dict(list=QtWidgets.QListView.ListMode,
                         icon=QtWidgets.QListView.IconMode))


class ListView(QtWidgets.QListView):

    def set_view_mode(self, mode: str):
        """set view mode

        possible values are "list", "icon"

        Args:
            mode: view mode to use

        Raises:
            ValueError: invalid view mode
        """
        if mode not in VIEW_MODES:
            raise ValueError(f"Invalid value. Valid values: {VIEW_MODES.keys()}")
        self.setViewMode(VIEW_MODES[mode])

    def get_view_mode(self) -> str:
        """returns view mode

        possible values are "list", "icon"

        Returns:
            view mode
        """
        return VIEW_MODES.inv[self.viewMode()]


ListView.__bases__[0].__bases__ = (widgets.AbstractItemView,)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    dlg = ListView()
    dlg.show()
    app.exec_()
