# -*- coding: utf-8 -*-

from qtpy import QtCore

from prettyqt import core
from prettyqt.utils import bidict, InvalidParamError


HISTORY_TYPES = bidict(
    shallow=QtCore.QHistoryState.ShallowHistory,
    deep=QtCore.QHistoryState.DeepHistory,
)

QtCore.QHistoryState.__bases__ = (core.AbstractState,)


class HistoryState(QtCore.QHistoryState):
    def set_history_type(self, typ: str):
        """Set history type to use.

        Allowed values are "shallow", "deep"

        Args:
            typ: history type to use

        Raises:
            InvalidParamError: history type does not exist
        """
        if typ not in HISTORY_TYPES:
            raise InvalidParamError(typ, HISTORY_TYPES)
        self.setHistoryType(HISTORY_TYPES[typ])

    def get_history_type(self) -> str:
        """Return current history type.

        Possible values: "shallow", "deep"

        Returns:
            history type
        """
        return HISTORY_TYPES.inv[self.historyType()]


if __name__ == "__main__":
    reg = HistoryState("This is a test", boundary_type="word")
    for p in reg:
        print(p)
