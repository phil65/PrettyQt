"""Tests for `prettyqt` package."""

# import regex as re

from prettyqt import custom_models


def test_regexmatchesmodel(qtmodeltester):
    # comp = re.compile("[0-9]")
    # text = "aa356aa356"
    matches = []  # list(comp.finditer(text))
    model = custom_models.RegexMatchesModel(matches)
    qtmodeltester.check(model, force_py=True)


def test_importlibdistributionmodel(qtmodeltester):
    model = custom_models.ImportlibDistributionModel([])
    qtmodeltester.check(model, force_py=True)
    custom_models.ImportlibDistributionModel.from_package("prettyqt")
    custom_models.ImportlibDistributionModel.from_system()


# def test_basemodelmixin(qtmodeltester):
#     class TestModel(custom_models.BaseModelMixin, core.AbstractTableModel):
#         def rowCount(self, index=None):
#             return 1

#         def columnCount(self, index=None):
#             return 1


#     model = TestModel()
#     qtmodeltester.check(model, force_py=True)
