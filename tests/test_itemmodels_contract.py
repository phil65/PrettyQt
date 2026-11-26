"""Run the QAbstractItemModel contract checks on all models and proxies."""

from __future__ import annotations

import dataclasses
import importlib
import inspect
import logging
import pathlib
import re
import xml.etree.ElementTree as ET

import pytest

from prettyqt import constants, core, gui, itemmodels, widgets


ROLES = [
    constants.DISPLAY_ROLE,
    constants.EDIT_ROLE,
    constants.TOOLTIP_ROLE,
    constants.DECORATION_ROLE,
    constants.CHECKSTATE_ROLE,
    constants.USER_ROLE,
    constants.FONT_ROLE,
    constants.FOREGROUND_ROLE,
    constants.BACKGROUND_ROLE,
]
XML = "<root><a k='v'>t</a><b><c/></b></root>"


@dataclasses.dataclass
class DataclassItem:
    a: int
    b: str
    c: bool = True


def pydantic_item():
    pydantic = pytest.importorskip("pydantic")

    class PydanticItem(pydantic.BaseModel):
        a: int
        b: str = "x"

    return PydanticItem(a=1)


def attrs_item():
    attrs = pytest.importorskip("attrs")

    @attrs.define
    class AttrsItem:
        a: int
        b: str = "x"

    return AttrsItem(a=1)


# modules which need an optional dependency
OPTIONAL_DEPS = {
    "pydanticmodel": "pydantic",
    "pydanticfieldsmodel": "pydantic",
    "attrsmodel": "attrs",
    "attrsfieldsmodel": "attrs",
    "lxmlmodel": "lxml",
    "gitpythontreemodel": "git",
}


def get_class(module: str, name: str):
    if dep := OPTIONAL_DEPS.get(module):
        pytest.importorskip(dep)
    return getattr(importlib.import_module(f"prettyqt.itemmodels.{module}"), name)


def walk(model, parent=None, depth: int = 0, maxdepth: int = 3, maxrows: int = 10):
    """Touch all methods for a limited part of the tree (for infinite models)."""
    parent = parent or core.ModelIndex()
    if depth > maxdepth:
        return
    if model.canFetchMore(parent):
        model.fetchMore(parent)
    is_table = isinstance(model, core.QAbstractTableModel)
    for i in range(min(model.rowCount(parent), maxrows)):
        for j in range(model.columnCount(parent)):
            idx = model.index(i, j, parent)
            assert idx.isValid()
            if not is_table:
                assert model.parent(idx) == parent
            model.flags(idx)
            for role in ROLES:
                model.data(idx, role)
        walk(model, model.index(i, 0, parent), depth + 1, maxdepth, maxrows)
    for j in range(model.columnCount(parent)):
        for role in ROLES:
            model.headerData(j, constants.HORIZONTAL, role)


@pytest.fixture
def widget(qapp):
    w = widgets.Widget()
    layout = widgets.VBoxLayout(w)
    layout.add(widgets.PushButton("x"))
    layout.addStretch()  # spacer item
    layout.add(widgets.LineEdit())
    return w


MODELS = {
    "json": lambda w: itemmodels.JsonModel({"a": [1, {"b": 2}], "c": "x", "t": (1,)}),
    "ast": lambda w: itemmodels.AstModel("def f(x):\n    return x + 1\n"),
    "parentclasstree": lambda w: itemmodels.ParentClassTreeModel(widgets.PushButton),
    "frameinfo": lambda w: itemmodels.FrameInfoModel(inspect.stack()[:3]),
    "dataclass": lambda w: itemmodels.DataClassModel([DataclassItem(1, "a")]),
    "dataclass_empty": lambda w: itemmodels.DataClassModel([]),
    "dataclassfields": lambda w: itemmodels.DataClassFieldsModel(DataclassItem(1, "a")),
    "logrecord": lambda w: itemmodels.LogRecordModel([
        logging.LogRecord("n", logging.INFO, "p", 1, "msg %s", ("a",), None)
    ]),
    "xml": lambda w: itemmodels.XmlModel(XML),
    "xml_element": lambda w: itemmodels.XmlModel(ET.fromstring(XML)),
    "mapping": lambda w: itemmodels.MappingModel([{"a": 1, "b": True}, {"a": 3}]),
    "mapping_empty": lambda w: itemmodels.MappingModel(),
    "tupletree": lambda w: itemmodels.TupleTreeModel({
        ("a",): "x",
        ("a", "b", "c"): "y",
        pathlib.PurePath("d/e"): "z",
    }),
    "regex": lambda w: itemmodels.RegexMatchesModel(list(re.finditer(r"(\d)", "1x2"))),
    "actions": lambda w: itemmodels.ActionsModel([
        gui.Action(text="a", shortcut="Ctrl+A")
    ]),
    # The source model is parented to the widget: a garbage-collected source model
    # leaves a dangling index (segfault on PySide6).
    "modelindex": lambda w: itemmodels.ModelIndexModel([
        itemmodels.JsonModel({"a": 1}, parent=w).index(0, 0)
    ]),
    "storageinfo": lambda w: itemmodels.StorageInfoModel(
        core.StorageInfo.get_mounted_volumes()[:2]
    ),
    "shortcuts": lambda w: itemmodels.ShortcutsModel([gui.Shortcut("Ctrl+B", w)]),
    "qobjectprops": lambda w: itemmodels.QObjectPropertiesModel(w),
    "widgetsdetails": lambda w: itemmodels.WidgetsDetailsModel(
        w.findChildren(widgets.QWidget)
    ),
    "widgethierarchy": lambda w: itemmodels.WidgetHierarchyModel(w),
    "layouthierarchy": lambda w: itemmodels.LayoutHierarchyModel(w),
    "pydantic": lambda w: get_class("pydanticmodel", "PydanticModel")([pydantic_item()]),
    "pydanticfields": lambda w: get_class("pydanticfieldsmodel", "PydanticFieldsModel")(
        pydantic_item()
    ),
    "attrs": lambda w: get_class("attrsmodel", "AttrsModel")([attrs_item()]),
    "attrsfields": lambda w: get_class("attrsfieldsmodel", "AttrsFieldsModel")(
        attrs_item()
    ),
    "lxml": lambda w: get_class("lxmlmodel", "LxmlModel")(XML),
    "lazylxml": lambda w: get_class("lxmlmodel", "LazyLxmlModel")(XML),
}
# lazy models with (practically) infinite trees, only walk a part of them.
INFINITE_MODELS = {
    "subclasstree": lambda w: itemmodels.SubClassTreeModel(core.QAbstractItemModel),
    "moduleinfo": lambda w: itemmodels.ModuleInfoModel(itemmodels),
    "pyobj": lambda w: itemmodels.PythonObjectTreeModel({"a": [1, 2], "b": (3,)}),
    "importlib": lambda w: itemmodels.ImportlibTreeModel("prettyqt"),
    "git": lambda w: get_class("gitpythontreemodel", "GitPythonTreeModel")(
        str(pathlib.Path(__file__).parent.parent)
    ),
}


@pytest.mark.parametrize("name", list(MODELS))
def test_model_contract(name, widget, qtmodeltester):
    model = MODELS[name](widget)
    walk(model)
    qtmodeltester.check(model, force_py=True)
    qtmodeltester.check(model, force_py=False)


@pytest.mark.parametrize("name", list(INFINITE_MODELS))
def test_infinite_model_contract(name, widget):
    if name == "git" and not (pathlib.Path(__file__).parent.parent / ".git").exists():
        pytest.skip("no git checkout")
    walk(INFINITE_MODELS[name](widget), maxdepth=2)


def table_source():
    model = gui.StandardItemModel()
    for i in range(6):
        model.appendRow([
            gui.StandardItem(f"name{i % 3}"),
            gui.StandardItem(str(i)),
            gui.StandardItem(str(i * 1.5)),
        ])
    model.setHorizontalHeaderLabels(["Name", "Int", "Float"])
    return model


def tree_source():
    model = gui.StandardItemModel()
    for i in range(3):
        parent = gui.StandardItem(f"p{i}")
        for j in range(3):
            child = gui.StandardItem(f"c{i}{j}")
            child.appendRow([gui.StandardItem(f"g{i}{j}"), gui.StandardItem("x")])
            parent.appendRow([child, gui.StandardItem(str(j))])
        model.appendRow([parent, gui.StandardItem(str(i))])
    model.setHorizontalHeaderLabels(["Name", "Val"])
    return model


PROXIES = {
    "Appearance": lambda: itemmodels.AppearanceProxyModel(),
    "ChangeHeaders": lambda: itemmodels.ChangeHeadersProxyModel({0: "A"}),
    "ColumnJoiner": lambda: itemmodels.ColumnJoinerProxyModel(),
    "ColumnOrder": lambda: itemmodels.ColumnOrderProxyModel([1, 0]),
    "FlattenTree": lambda: itemmodels.FlattenTreeProxyModel(),
    "FuzzyFilter": lambda: itemmodels.FuzzyFilterProxyModel(),
    "Melt": lambda: itemmodels.MeltProxyModel([0]),
    "MultiColumnFilter": lambda: itemmodels.MultiColumnFilterProxyModel(),
    "PredicateFilter": lambda: itemmodels.PredicateFilterProxyModel(),
    "RangeFilter": lambda: itemmodels.RangeFilterProxyModel(1, 4),
    "SliceAppearance": lambda: itemmodels.SliceAppearanceProxyModel(foreground="red"),
    "SliceChangeFlags": lambda: itemmodels.SliceChangeFlagsProxyModel(),
    "SliceChangeIconSize": lambda: itemmodels.SliceChangeIconSizeProxyModel((10, 10)),
    "SliceCheckable": lambda: itemmodels.SliceCheckableProxyModel(),
    "SliceCheckableTree": lambda: itemmodels.SliceCheckableTreeProxyModel(),
    "SliceColorCategories": lambda: itemmodels.SliceColorCategoriesProxyModel(),
    "SliceDisplayText": lambda: itemmodels.SliceDisplayTextProxyModel(),
    "SliceFilter": lambda: itemmodels.SliceFilterProxyModel(
        indexer=(slice(1, None, 2), 0)
    ),
    "SliceHighlightCurrent": lambda: itemmodels.SliceHighlightCurrentProxyModel(),
    "SliceIdentity": lambda: itemmodels.SliceIdentityProxyModel(),
    "SliceMapRole": lambda: itemmodels.SliceMapRoleProxyModel({
        constants.DISPLAY_ROLE: constants.TOOLTIP_ROLE
    }),
    "SliceToMarkdown": lambda: itemmodels.SliceToMarkdownProxyModel(),
    "SliceValueTransformation": lambda: itemmodels.SliceValueTransformationProxyModel(),
    "SubsetFilter": lambda: itemmodels.SubsetFilterProxyModel(slice(0, 2), None),
    "TableToList": lambda: itemmodels.TableToListProxyModel(),
    "ValueFilter": lambda: itemmodels.ValueFilterProxyModel("name1"),
    "Rank": lambda: get_class("proxies.rankproxymodel", "RankProxyModel")(1),
    "Unmelt": lambda: get_class("proxies.unmeltproxymodel", "UnmeltProxyModel")(
        [0], 1, 2
    ),
    "Bins": lambda: get_class("proxies.binsproxymodel", "BinsProxyModel")(
        1, [0, 2, 4, 6]
    ),
    "Stack": lambda: get_class("proxies.stackproxymodel", "StackProxyModel")(),
}


@pytest.mark.parametrize("source", ["table", "tree"])
@pytest.mark.parametrize("name", list(PROXIES))
def test_proxy_contract(name, source, qtmodeltester):
    src = table_source() if source == "table" else tree_source()
    proxy = PROXIES[name]()
    proxy.setSourceModel(src)
    qtmodeltester.check(proxy, force_py=True)
    qtmodeltester.check(proxy, force_py=False)
    # mutate the source to exercise signal forwarding.
    src.appendRow([gui.StandardItem("new"), gui.StandardItem("7")])
    src.removeRow(0)
    src.setData(src.index(0, 0), "changed")
    proxy.sort(0, constants.DESCENDING)
    qtmodeltester.check(proxy, force_py=True)
