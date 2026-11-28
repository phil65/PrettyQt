"""Tests for `prettyqt.constants`."""

from typing import get_args

import pytest

from prettyqt import constants
from prettyqt.utils import InvalidParamError


BIDICT_LITERAL_PAIRS = [
    ("ALIGNMENTS", constants.ALIGNMENTS, constants.AlignmentStr),
    ("CHECK_STATE", constants.CHECK_STATE, constants.CheckStateStr),
    ("ITEM_DATA_ROLE", constants.ITEM_DATA_ROLE, constants.ItemDataRoleStr),
    ("MOUSE_BUTTON", constants.MOUSE_BUTTON, constants.MouseButtonStr),
    (
        "WINDOW_FRAME_SECTION",
        constants.WINDOW_FRAME_SECTION,
        constants.WindowFrameSectionStr,
    ),
    ("CURSOR_SHAPE", constants.CURSOR_SHAPE, constants.CursorShapeStr),
    ("FOCUS_REASONS", constants.FOCUS_REASONS, constants.FocusReasonStr),
    ("TOOLBUTTON_STYLE", constants.TOOLBUTTON_STYLE, constants.ToolButtonStyleStr),
    ("KEY", constants.KEY, constants.KeyStr),
    ("WIDGET_ATTRIBUTE", constants.WIDGET_ATTRIBUTE, constants.WidgetAttributeStr),
    (
        "APPLICATION_ATTRIBUTE",
        constants.APPLICATION_ATTRIBUTE,
        constants.ApplicationAttributeStr,
    ),
]


@pytest.mark.parametrize(
    ("name", "mapping", "literal_type"),
    BIDICT_LITERAL_PAIRS,
    ids=[p[0] for p in BIDICT_LITERAL_PAIRS],
)
def test_bidict_bidirectional_and_literal_match(name, mapping, literal_type):
    assert len(mapping) > 0, f"{name} should not be empty"
    assert len(mapping) == len(mapping.inverse), f"{name} inverse length mismatch"
    for key, val in mapping.items():
        assert mapping.inverse[val] == key, f"{name} inverse mismatch for {key!r}"
    expected_keys = set(get_args(literal_type))
    if name == "ITEM_DATA_ROLE" and not hasattr(
        constants.ItemDataRole, "RangeModelDataRole"
    ):
        expected_keys.discard("range_model_data")
    assert set(mapping.keys()) == expected_keys, f"{name} keys do not match Literal type"


def test_bidict_get_enum_value():
    assert constants.CHECK_STATE.get_enum_value("checked") == constants.CheckState.Checked
    assert (
        constants.CHECK_STATE.get_enum_value(constants.CheckState.Unchecked)
        == constants.CheckState.Unchecked
    )
    with pytest.raises(InvalidParamError):
        constants.CHECK_STATE.get_enum_value("not_a_valid_state")  # type: ignore[arg-type]
