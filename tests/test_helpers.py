"""Tests for `prettyqt` package."""

import pytest

from prettyqt import constants
from prettyqt.utils import helpers


def test_string_to_num_array():
    assert helpers.string_to_num_array("1, 3, 5") == [1, 3, 5]
    with pytest.raises(ValueError):  # noqa: PT011
        helpers.string_to_num_array("1, 2, f")


def test_bidict_tolerates_duplicate_values():
    from prettyqt.utils import bidict

    mapping = bidict(a=constants.ALIGN_LEFT, b=constants.ALIGN_LEFT)
    assert dict(mapping) == {"a": constants.ALIGN_LEFT}
    assert mapping.inverse[constants.ALIGN_LEFT] == "a"


def test_bidict_tolerates_enum_aliases():
    import enum

    from prettyqt.utils import bidict

    class Flag(enum.IntFlag):
        none = 0
        bullet = 1
        all = 1  # alias, like AutoAll on PySide6 6.12 / Windows / Python 3.15

    mapping = bidict(none=Flag.none, bullet_list=Flag.bullet, all=Flag.all)
    assert mapping["bullet_list"] is Flag.bullet
    assert mapping.inverse[Flag.all] == "bullet_list"
    assert "all" not in mapping


def test_datatypes_to_point():
    from prettyqt import core
    from prettyqt.utils import datatypes

    assert datatypes.to_point((1, 2)) == core.QPoint(1, 2)
    assert datatypes.to_point(core.QPointF(1.4, 2.6)) == core.QPoint(1, 3)


def test_datatypes_to_keysequence_standard_key(qapp):
    from prettyqt import gui
    from prettyqt.utils import datatypes

    seq = datatypes.to_keysequence(gui.QKeySequence.StandardKey.Copy)
    assert seq == gui.QKeySequence(gui.QKeySequence.StandardKey.Copy)


@pytest.mark.parametrize("hide_ipython", [False, True])
def test_errormessagebox_tb_formatter(monkeypatch, hide_ipython):
    import sys

    from prettyqt.debugging import errormessagebox

    if hide_ipython:
        monkeypatch.setitem(sys.modules, "IPython.core.ultratb", None)
    else:
        pytest.importorskip("IPython")
    formatter = errormessagebox.get_tb_formatter()
    with pytest.raises(ValueError, match="boom") as info:
        raise ValueError("boom")
    assert "boom" in formatter(info.value, False)
    assert formatter(info.value, True).startswith("<span")
