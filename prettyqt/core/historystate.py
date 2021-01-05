from __future__ import annotations

from typing import Literal

from prettyqt import core
from prettyqt.qt import QtCore
from prettyqt.utils import InvalidParamError, bidict


HISTORY_TYPE = bidict(
    shallow=QtCore.QHistoryState.ShallowHistory,
    deep=QtCore.QHistoryState.DeepHistory,
)

HistoryTypeStr = Literal["shallow", "deep"]

QtCore.QHistoryState.__bases__ = (core.AbstractState,)


class HistoryState(QtCore.QHistoryState):
    def set_history_type(self, typ: HistoryTypeStr):
        """Set history type to use.

        Args:
            typ: history type to use

        Raises:
            InvalidParamError: history type does not exist
        """
        if typ not in HISTORY_TYPE:
            raise InvalidParamError(typ, HISTORY_TYPE)
        self.setHistoryType(HISTORY_TYPE[typ])

    def get_history_type(self) -> HistoryTypeStr:
        """Return current history type.

        Returns:
            history type
        """
        return HISTORY_TYPE.inverse[self.historyType()]


if __name__ == "__main__":
    state = HistoryState()
