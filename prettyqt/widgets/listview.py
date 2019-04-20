# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets

SELECTION_MODES = dict(single=QtWidgets.QAbstractItemView.SingleSelection,
                       extended=QtWidgets.QAbstractItemView.ExtendedSelection,
                       multi=QtWidgets.QAbstractItemView.MultiSelection,
                       none=QtWidgets.QAbstractItemView.NoSelection)


class ListView(QtWidgets.QListView):

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

    def toggle_select_all(self):
        """
        select all items from list (deselect when all selected)
        """
        if self.selectionModel() is None:
            return None
        if self.selectionModel().hasSelection():
            self.clearSelection()
        else:
            self.selectAll()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dlg = QtWidgets.QMainWindow()
    status_bar = ListView()
    dlg.show()
    app.exec_()
