# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets

SELECTION_MODES = dict(single=QtWidgets.QAbstractItemView.SingleSelection,
                       extended=QtWidgets.QAbstractItemView.ExtendedSelection,
                       multi=QtWidgets.QAbstractItemView.MultiSelection,
                       none=QtWidgets.QAbstractItemView.NoSelection)


class TreeView(QtWidgets.QTreeView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # visual settings
        self.setAnimated(True)
        self.setRootIsDecorated(False)
        self.setAllColumnsShowFocus(True)

        # misc
        self.setUniformRowHeights(True)
        self.set_selection_mode("extended")

    def h_header(self):
        return self.header()

    def set_selection_mode(self, mode: str):
        """set selection mode for given item view

        Allowed values are "single", "extended", "multi" or "none"

        Args:
            mode: selection mode to use

        Raises:
            ValueError: mode does not exist
        """
        if mode not in SELECTION_MODES:
            raise ValueError("Format must be either 'single', 'extended',"
                             "'multi' or 'None'")
        self.setSelectionMode(SELECTION_MODES[mode])


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dlg = QtWidgets.QMainWindow()
    status_bar = TreeView()
    dlg.show()
    app.exec_()
