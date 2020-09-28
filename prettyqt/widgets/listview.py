# -*- coding: utf-8 -*-

from qtpy import QtWidgets

from prettyqt import widgets
from prettyqt.utils import bidict, InvalidParamError


VIEW_MODES = bidict(list=QtWidgets.QListView.ListMode, icon=QtWidgets.QListView.IconMode)


QtWidgets.QListView.__bases__ = (widgets.AbstractItemView,)


class ListView(QtWidgets.QListView):
    def set_view_mode(self, mode: str):
        """Set view mode.

        possible values are "list", "icon"

        Args:
            mode: view mode to use

        Raises:
            InvalidParamError: invalid view mode
        """
        if mode not in VIEW_MODES:
            raise InvalidParamError(mode, VIEW_MODES)
        self.setViewMode(VIEW_MODES[mode])

    def get_view_mode(self) -> str:
        """Return view mode.

        possible values are "list", "icon"

        Returns:
            view mode
        """
        return VIEW_MODES.inv[self.viewMode()]


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    dlg = ListView()
    dlg.show()
    app.main_loop()
