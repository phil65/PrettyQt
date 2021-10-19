"""Core module.

Contains QtCore-based classes
"""

# from prettyqt.qt.QtCore import Signal

from __future__ import annotations


from .abstracttransition import AbstractTransition
from .signaltransition import SignalTransition
from .eventtransition import EventTransition
from .abstractstate import AbstractState
from .finalstate import FinalState
from .historystate import HistoryState
from .state import State
from .statemachine import StateMachine


__all__ = [
    "AbstractState",
    "FinalState",
    "HistoryState",
    "State",
    "StateMachine",
    "AbstractTransition",
    "SignalTransition",
    "EventTransition",
]
