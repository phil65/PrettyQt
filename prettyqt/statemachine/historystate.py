from __future__ import annotations

from typing import Literal

from prettyqt import statemachine
from prettyqt.qt import QtStateMachine
from prettyqt.utils import InvalidParamError, bidict


HISTORY_TYPE = bidict(
    shallow=QtStateMachine.QHistoryState.HistoryType.ShallowHistory,
    deep=QtStateMachine.QHistoryState.HistoryType.DeepHistory,
)

HistoryTypeStr = Literal["shallow", "deep"]

QtStateMachine.QHistoryState.__bases__ = (statemachine.AbstractState,)


class HistoryState(QtStateMachine.QHistoryState):
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
