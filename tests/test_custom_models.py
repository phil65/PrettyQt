"""Tests for `prettyqt` package."""

from importlib import metadata

import pytest
import regex as re

from prettyqt import custom_models
from prettyqt.utils import InvalidParamError


def test_regexmatchesmodel(qtmodeltester):
    comp = re.compile("[0-9]")
    text = "aa356aa356"
    matches = list(comp.finditer(text))
    model = custom_models.RegexMatchesModel(matches)
    qtmodeltester.check(model, force_py=True)


def test_importlibdistributionmodel(qtmodeltester):
    model = custom_models.ImportlibDistributionModel([metadata.distribution("prettyqt")])
    qtmodeltester.check(model, force_py=True)
    custom_models.ImportlibDistributionModel.from_package("prettyqt")
    custom_models.ImportlibDistributionModel.from_system()


def test_jsonmodel(qtmodeltester):
    dct = {
        "lastName": "Smith",
        "age": 25,
        "address": {"streetAddress": "21 2nd Street", "postalCode": "10021"},
        "phoneNumber": [
            {"type": "home", "number": "212 555-1234"},
            {"type": "fax", "number": ("646 555-4567")},
        ],
    }
    model = custom_models.JsonModel()
    model.load(dct)
    qtmodeltester.check(model, force_py=True)


def test_fsspecmodel(qtbot, qtmodeltester):
    model = custom_models.FSSpecTreeModel()
    idx = model.index(0, 0)
    model.get_paths([idx])
    model.data(idx, model.Roles.FilePathRole)
    model.yield_child_indexes(idx)
    model.watch_for_changes(False)
    model.use_custom_icons(False)
    model.resolve_sym_links(False)
    model.set_name_filters(["test"], hide=True)
    model.set_filter("drives")
    with pytest.raises(InvalidParamError):
        model.set_filter("test")
    # qtmodeltester.check(model, force_py=True)
