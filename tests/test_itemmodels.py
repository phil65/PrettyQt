"""Tests for `prettyqt` package."""

import dataclasses

# from importlib import metadata
import inspect
import re

import pytest

from prettyqt import core, itemmodels
from prettyqt.itemmodels import fsspecmodel
from prettyqt.utils import InvalidParamError


clsmembers = inspect.getmembers(itemmodels, inspect.isclass)
clsmembers = [tpl for tpl in clsmembers if core.QObject in tpl[1].mro()]


models = [tpl for tpl in clsmembers if not issubclass(tpl[1], core.QAbstractItemModel)]
proxies = [tpl for tpl in clsmembers if not issubclass(tpl[1], core.QAbstractProxyModel)]


def test_xmlmodel(qtmodeltester):
    xml = """<root>
<element key='value'>text</element>
<element><sub>text</sub></element>
<empty-element xmlns="http://testns/" />
</root>
"""
    model = itemmodels.XmlModel(xml)
    qtmodeltester.check(model, force_py=True)


def test_dataclassmodel(qtmodeltester):
    @dataclasses.dataclass
    class Test:
        a: int
        b: str

    test = Test(a=1, b="abc")
    model = itemmodels.DataClassModel([test])
    qtmodeltester.check(model, force_py=True)


def test_dataclassfieldsmodel(qtmodeltester):
    @dataclasses.dataclass
    class Test:
        a: int
        b: str

    test = Test(a=1, b="abc")
    model = itemmodels.DataClassFieldsModel(test)
    qtmodeltester.check(model, force_py=True)


def test_regexmatchesmodel(qtmodeltester):
    comp = re.compile("[0-9]")
    text = "aa356aa356"
    matches = list(comp.finditer(text))
    model = itemmodels.RegexMatchesModel(matches)
    qtmodeltester.check(model, force_py=True)


# def test_importlibtreemodel(qtmodeltester):
#     model = itemmodels.ImportlibTreeModel(metadata.distribution("prettyqt"))
#     qtmodeltester.check(model)
# itemmodels.ImportlibDistributionModel.from_package("prettyqt")
# itemmodels.ImportlibDistributionModel.from_system()


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
    model = itemmodels.JsonModel(dct)
    qtmodeltester.check(model, force_py=True)


def test_fsspecmodel(qtbot, qtmodeltester):
    model = fsspecmodel.FSSpecTreeModel()
    idx = model.index(0, 0)
    model.get_paths([idx])
    model.data(idx, model.Roles.FilePathRole)
    model.watch_for_changes(False)
    model.use_custom_icons(False)
    model.resolve_sym_links(False)
    model.set_name_filters(["test"], hide=True)
    model.set_filter("drives")
    with pytest.raises(InvalidParamError):
        model.set_filter("test")
    # qtmodeltester.check(model, force_py=True)
