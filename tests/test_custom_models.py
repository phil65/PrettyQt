"""Tests for `prettyqt` package."""

from importlib import metadata

import regex as re

from prettyqt import custom_models


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


# def test_basemodelmixin(qtmodeltester):
#     class TestModel(custom_models.BaseModelMixin, core.AbstractTableModel):
#         def rowCount(self, index=None):
#             return 1

#         def columnCount(self, index=None):
#             return 1


#     model = TestModel()
#     qtmodeltester.check(model, force_py=True)
