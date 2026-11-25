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
