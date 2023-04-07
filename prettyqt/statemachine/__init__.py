"""Core module.

Contains QtCore-based classes
"""

# from prettyqt.qt.QtCore import Signal

from __future__ import annotations


from .abstracttransition import AbstractTransition, AbstractTransitionMixin
from .signaltransition import SignalTransition
from .eventtransition import EventTransition, EventTransitionMixin
from .abstractstate import AbstractState, AbstractStateMixin
from .finalstate import FinalState
from .historystate import HistoryState
from .state import State
from .statemachine import StateMachine


__all__ = [
    "AbstractState",
    "AbstractStateMixin",
    "FinalState",
    "HistoryState",
    "State",
    "StateMachine",
    "AbstractTransition",
    "AbstractTransitionMixin",
    "SignalTransition",
    "EventTransition",
    "EventTransitionMixin",
]
