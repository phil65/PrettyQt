"""Tests for `prettyqt` package."""

import pytest

from prettyqt.qt import QtCore
from prettyqt.utils import InvalidParamError


statemachine = pytest.importorskip("prettyqt.statemachine")


def test_historystate():
    state = statemachine.HistoryState(history_type="deep")
    assert state.get_history_type() == "deep"
    state.set_history_type("shallow")
    assert state.get_history_type() == "shallow"
    with pytest.raises(InvalidParamError):
        state.set_history_type("test")


def test_signaltransition():
    trans = statemachine.SignalTransition(transition_type="internal")
    assert trans.get_transition_type() == "internal"
    trans.set_transition_type("external")
    assert trans.get_transition_type() == "external"
    with pytest.raises(InvalidParamError):
        trans.set_transition_type("test")


def test_key_and_mouse_event_transitions():
    key_trans = statemachine.KeyEventTransition()
    key_trans.set_transition_type("internal")
    assert key_trans.get_transition_type() == "internal"
    mouse_trans = statemachine.MouseEventTransition()
    mouse_trans.set_transition_type("external")
    assert mouse_trans.get_transition_type() == "external"


def test_state():
    assert issubclass(statemachine.State, statemachine.StateMixin)
    state = statemachine.State(child_mode="parallel")
    assert state.get_child_mode() == "parallel"
    state.set_child_mode("exclusive")
    assert state.get_child_mode() == "exclusive"
    with pytest.raises(InvalidParamError):
        state.set_child_mode("test")


def test_statemachine():
    machine = statemachine.StateMachine(global_restore_policy="dont_restore")
    assert machine.get_global_restore_policy() == "dont_restore"
    state = statemachine.State()
    machine += state
    assert machine.get_error() == "none"
    machine.set_global_restore_policy("restore")
    assert machine.get_global_restore_policy() == "restore"
    with pytest.raises(InvalidParamError):
        machine.set_global_restore_policy("test")
    event = QtCore.QEvent(QtCore.QEvent.Type.ActionAdded)
    machine.post_event(event)
    with pytest.raises(InvalidParamError):
        machine.post_event(event, "test")
    assert "no_common_ancestor_for_transition" in statemachine.statemachine.ERROR
    assert "state_machine_child_mode_set_to_parallel" in statemachine.statemachine.ERROR
