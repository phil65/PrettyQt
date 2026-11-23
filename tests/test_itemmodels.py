"""Tests for `prettyqt` package."""

import dataclasses

# from importlib import metadata
import inspect
import logging
import re

import pytest

from prettyqt import constants, core, itemmodels, widgets
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


# regression tests


def test_from_checkstate():
    from_cs = core.AbstractItemModelMixin.from_checkstate
    assert from_cs(constants.CheckState.Checked) is True
    assert from_cs(constants.CheckState.Unchecked) is False
    assert from_cs(2) is True
    assert from_cs(0) is False
    assert from_cs(True) is True


def test_listmixin_list_interface_and_sort(qapp):
    model = itemmodels.MappingModel([{"a": 3}, {"a": 1}, {"a": 2}])
    model.sort(0, constants.ASCENDING)
    assert [i["a"] for i in model.items] == [1, 2, 3]
    model.sort(0, constants.DESCENDING)
    assert [i["a"] for i in model.items] == [3, 2, 1]
    model.extend([{"a": 4}, {"a": 5}])
    assert [i["a"] for i in model.items] == [3, 2, 1, 4, 5]
    model[0:2] = [{"a": 10}, {"a": 11}]
    assert model[1] == {"a": 11}
    assert model.pop() == {"a": 5}
    model.add_items([])  # must not emit invalid insert signals
    assert [i["a"] for i in model.items] == [10, 11, 1, 4]


def test_auto_model_positional_items(qapp):
    """AbstractItemView.set_model_for constructs models with data as first argument."""
    view = widgets.TableView()
    view.set_model_for([{"a": 1, "b": 2}])
    assert view.model().rowCount() == 1
    rec = logging.LogRecord("n", logging.INFO, "p", 1, "msg", (), None)
    assert itemmodels.LogRecordModel([rec]).rowCount() == 1


def test_dataclass_models(qapp):
    @dataclasses.dataclass(frozen=True)
    class Frozen:
        a: int
        b: bool = False

    @dataclasses.dataclass
    class Mutable:
        a: int
        b: bool = False

    frozen = itemmodels.DataClassModel([Frozen(1)])
    assert not frozen.flags(frozen.index(0, 0)) & constants.IS_EDITABLE
    items = [Mutable(1)]
    model = itemmodels.DataClassModel(items)
    assert model.flags(model.index(0, 1)) & constants.IS_CHECKABLE
    model.setData(
        model.index(0, 1), constants.CheckState.Checked, constants.CHECKSTATE_ROLE
    )
    assert items[0].b is True
    model.setData(
        model.index(0, 1), constants.CheckState.Unchecked, constants.CHECKSTATE_ROLE
    )
    assert items[0].b is False
    fields = itemmodels.DataClassFieldsModel(Mutable(1))
    assert fields.headerData(0, constants.HORIZONTAL) == "Value"
    assert fields.index(0, 1).data() == "int"
    assert fields.index(0, 2).data() == ""  # no default


def test_xmlmodel_large_document(qapp):
    xml = (
        "<root>" + "".join(f"<a i='{i}'>{'x' * 50}</a>" for i in range(5000)) + "</root>"
    )
    model = itemmodels.XmlModel(xml)
    root = model.index(0, 0)
    model.fetchMore(root)
    assert model.rowCount(root) == 5000  # noqa: PLR2004


def test_jsonmodel_edit_writes_through(qapp):
    data = {"a": [1, 2]}
    model = itemmodels.JsonModel(data)
    root = model.index(0, 0)
    model.fetchMore(root)
    a = model.index(0, 0, root)
    model.fetchMore(a)
    assert model.setData(model.index(1, 1, a), 99)
    assert data == {"a": [1, 99]}
    assert not model.flags(model.index(0, 1, root)) & constants.IS_EDITABLE


def test_tupletreemodel_paths_and_missing_parents(qapp):
    import pathlib

    model = itemmodels.TupleTreeModel({pathlib.PurePath("x/y"): "leaf"})
    root = model.index(0, 0)
    model.fetchMore(root)
    x = model.index(0, 0, root)
    model.fetchMore(x)
    assert x.data() == "x"
    assert model.index(0, 0, x).data() == "leaf"


def test_moduleinfomodel_children(qapp):
    model = itemmodels.ModuleInfoModel(itemmodels)
    root = model.index(0, 0)
    model.fetchMore(root)
    assert model.rowCount(root) > 10  # noqa: PLR2004


def test_pythonobjecttreemodel_refresh(qapp):
    obj = {"a": [1, 2, 3], "b": 1}
    model = itemmodels.PythonObjectTreeModel(obj)
    a = model.index(0, 0)
    model.fetchMore(a)
    count = model.rowCount(a)
    obj["a"] = [1]
    obj["zz"] = 5
    del obj["b"]
    model.refresh_tree()
    assert model.rowCount(a) == count - 2
    assert [model.index(i, 0).data() for i in range(2)] == ["a", "zz"]


def test_astmodel_rename_variable(qapp):
    model = itemmodels.AstModel("def f(x):\n    return x + 1\n")
    model.rename_variable("x", "y")
    assert "def f(y)" in model.code
    assert "y + 1" in model.code


def test_rank_proxy(qapp):
    from prettyqt import gui
    from prettyqt.itemmodels.proxies.rankproxymodel import RankProxyModel

    source = gui.StandardItemModel.from_dict({"score": [85, 92, 78, 92, 88]})
    expected = {
        "average": ["4", "1.5", "5", "1.5", "3"],
        "min": ["4", "1", "5", "1", "3"],
        "dense": ["3", "1", "4", "1", "2"],
        "ordinal": ["4", "1", "5", "2", "3"],
    }
    for method, ranks in expected.items():
        proxy = RankProxyModel(0, method=method, ascending=False)
        proxy.setSourceModel(source)
        assert [proxy.index(i, 0).data() for i in range(5)] == ranks
    source.setData(source.index(2, 0), 100)
    assert proxy.index(2, 0).data() == "1"


def test_melt_unmelt_roundtrip(qapp):
    from prettyqt import gui
    from prettyqt.itemmodels.proxies.unmeltproxymodel import UnmeltProxyModel

    data = dict(first=["John", "Mary"], last=["Doe", "Bo"], height=[5.5, 6.0])
    source = gui.StandardItemModel.from_dict(data)
    melt = itemmodels.MeltProxyModel([1])  # non-zero id column
    melt.setSourceModel(source)
    assert melt.rowCount() == 4  # noqa: PLR2004
    assert [melt.index(0, c).data() for c in range(3)] == ["Doe", "first", "John"]
    unmelt = UnmeltProxyModel([0], 1, 2)
    unmelt.setSourceModel(melt)
    assert [unmelt.index(1, c).data() for c in range(3)] == ["Bo", "Mary", 6.0]


def test_slice_filter_proxy(qapp):
    from prettyqt import gui

    source = gui.StandardItemModel.from_dict({"a": list(range(6))})
    proxy = itemmodels.SliceFilterProxyModel(indexer=(slice(1, None, 2), 0))
    proxy.setSourceModel(source)
    assert [proxy.index(i, 0).data() for i in range(proxy.rowCount())] == [1, 3, 5]
    proxy = itemmodels.SliceFilterProxyModel(indexer=(slice(-2, None), 0))
    proxy.setSourceModel(source)
    assert proxy.rowCount() == 2  # noqa: PLR2004


def test_checkable_tree_proxy(qapp):
    from prettyqt import gui

    source = gui.StandardItemModel()
    parent = gui.StandardItem("p")
    parent.appendRow([gui.StandardItem("c0")])
    parent.appendRow([gui.StandardItem("c1")])
    source.appendRow([parent])
    proxy = itemmodels.SliceCheckableTreeProxyModel(indexer=0)
    proxy.setSourceModel(source)
    role = constants.CHECKSTATE_ROLE
    p = proxy.index(0, 0)
    proxy.setData(proxy.index(0, 0, p), constants.CheckState.Checked, role)
    assert p.data(role) == constants.CheckState.PartiallyChecked
    proxy.setData(proxy.index(1, 0, p), constants.CheckState.Checked, role)
    assert p.data(role) == constants.CheckState.Checked
    proxy.setData(p, constants.CheckState.Unchecked, role)
    assert proxy.index(0, 0, p).data(role) == constants.CheckState.Unchecked


def test_proxifier_reshape_methods(qapp):
    from prettyqt import gui

    def make_table(data):
        table = widgets.TableView()
        table.set_model(gui.StandardItemModel.from_dict(data))
        return table

    table = make_table({"score": [85, 92, 78]})
    proxy = table.proxifier.rank(column=0, method="dense", ascending=False)
    assert [proxy.index(i, 0).data() for i in range(3)] == ["2", "1", "3"]
    table = make_table({"age": [22, 44, 99]})
    proxy = table.proxifier.bins(column=0, bins=[0, 30, 50], labels=["young", "old"])
    assert [proxy.index(i, 0).data() for i in range(3)] == ["young", "old", ""]
    table = make_table({"a": [1, 2], "b": [3, 4]})
    proxy = table.proxifier.stack()
    assert proxy.rowCount() == 4  # noqa: PLR2004
    # source changes must reach the (source_model kwarg constructed) proxies.
    table.model().sourceModel().setData(table.model().sourceModel().index(0, 0), 7)
    assert proxy.index(0, 1).data() == 7  # noqa: PLR2004
