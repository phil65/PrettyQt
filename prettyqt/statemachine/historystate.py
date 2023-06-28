from __future__ import annotations

from typing import Literal

from prettyqt import statemachine
from prettyqt.utils import bidict


HistoryTypeStr = Literal["shallow", "deep"]

HISTORY_TYPE: bidict[HistoryTypeStr, statemachine.QHistoryState.HistoryType] = bidict(
    shallow=statemachine.QHistoryState.HistoryType.ShallowHistory,
    deep=statemachine.QHistoryState.HistoryType.DeepHistory,
)


class HistoryState(statemachine.AbstractStateMixin, statemachine.QHistoryState):
    def set_history_type(
        self, typ: HistoryTypeStr | statemachine.QHistoryState.HistoryType
    ):
        """Set history type to use.

        Args:
            typ: history type to use
        """
        self.setHistoryType(HISTORY_TYPE.get_enum_value(typ))

    def get_history_type(self) -> HistoryTypeStr:
        """Return current history type.

        Returns:
            history type
        """
        return HISTORY_TYPE.inverse[self.historyType()]


if __name__ == "__main__":
    state = HistoryState()
