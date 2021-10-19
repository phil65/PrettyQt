"""Tests for `prettyqt` package."""

import pytest

from prettyqt.qt import QtCore
from prettyqt.utils import InvalidParamError


statemachine = pytest.importorskip("statemachine")


def test_historystate():
    state = statemachine.HistoryState()
    state.set_history_type("deep")
    assert state.get_history_type() == "deep"
    with pytest.raises(InvalidParamError):
        state.set_history_type("test")


def test_signaltransition():
    trans = statemachine.SignalTransition()
    trans.set_transition_type("parallel")
    assert trans.get_transition_type() == "parallel"
    with pytest.raises(InvalidParamError):
        trans.set_transition_type("test")


def test_state():
    state = statemachine.State()
    state.set_child_mode("parallel")
    assert state.get_child_mode() == "parallel"
    with pytest.raises(InvalidParamError):
        state.set_child_mode("test")


def test_statemachine():
    machine = statemachine.StateMachine()
    state = statemachine.State()
    machine += state
    assert machine.get_error() == "none"
    machine.set_global_restore_policy("dont_restore")
    assert machine.get_global_restore_policy() == "dont_restore"
    with pytest.raises(InvalidParamError):
        machine.set_global_restore_policy("test")
    event = QtCore.QEvent(QtCore.QEvent.ActionAdded)
    machine.post_event(event)
    with pytest.raises(InvalidParamError):
        machine.post_event(event, "test")
