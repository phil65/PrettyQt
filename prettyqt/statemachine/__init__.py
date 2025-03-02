"""Provides classes for creating and executing state graphs."""

from __future__ import annotations

from prettyqt.qt.QtStateMachine import *  # noqa: F403

from .abstractstate import AbstractState, AbstractStateMixin
from .abstracttransition import AbstractTransition, AbstractTransitionMixin
from .eventtransition import EventTransition
from .finalstate import FinalState
from .historystate import HistoryState
from .signaltransition import SignalTransition
from .state import State
from .statemachine import StateMachine
from prettyqt.qt import QtStateMachine

QT_MODULE = QtStateMachine

__all__ = [
    "AbstractState",
    "AbstractStateMixin",
    "AbstractTransition",
    "AbstractTransitionMixin",
    "EventTransition",
    "FinalState",
    "HistoryState",
    "SignalTransition",
    "State",
    "StateMachine",
]
