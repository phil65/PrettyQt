from __future__ import annotations

from typing import Literal

from prettyqt.qt import QtCore
from prettyqt.utils import bidict


PriorityStr = Literal[
    "idle", "lowest", "low", "normal", "high", "highest", "time_critical", "inherit"
]

PRIORITY: bidict[PriorityStr, QtCore.QThread.Priority] = bidict(
    idle=QtCore.QThread.Priority.IdlePriority,
    lowest=QtCore.QThread.Priority.LowestPriority,
    low=QtCore.QThread.Priority.LowPriority,
    normal=QtCore.QThread.Priority.NormalPriority,
    high=QtCore.QThread.Priority.HighPriority,
    highest=QtCore.QThread.Priority.HighestPriority,
    time_critical=QtCore.QThread.Priority.TimeCriticalPriority,
    inherit=QtCore.QThread.Priority.InheritPriority,
)


class Thread(QtCore.QThread):
    """Platform-independent way to manage threads."""

    def get_priority(self) -> PriorityStr:
        return PRIORITY.inverse[self.priority()]
