from typing import Literal, Tuple, Union

from qtpy import QtCore, QtWidgets

from prettyqt import widgets
from prettyqt.utils import InvalidParamError, bidict


VIEW_MODE = bidict(list=QtWidgets.QListView.ListMode, icon=QtWidgets.QListView.IconMode)

ViewModeStr = Literal["list", "icon"]

QtWidgets.QListView.__bases__ = (widgets.AbstractItemView,)


class ListView(QtWidgets.QListView):
    def set_view_mode(self, mode: ViewModeStr):
        """Set view mode.

        Args:
            mode: view mode to use

        Raises:
            InvalidParamError: invalid view mode
        """
        if mode not in VIEW_MODE:
            raise InvalidParamError(mode, VIEW_MODE)
        self.setViewMode(VIEW_MODE[mode])

    def get_view_mode(self) -> ViewModeStr:
        """Return view mode.

        Returns:
            view mode
        """
        return VIEW_MODE.inverse[self.viewMode()]

    def set_grid_size(self, size: Union[QtCore.QSize, Tuple[int, int]]):
        if isinstance(size, tuple):
            size = QtCore.QSize(*size)
        self.setGridSize(size)


if __name__ == "__main__":
    app = widgets.app()
    dlg = ListView()
    dlg.show()
    app.main_loop()
