from __future__ import annotations

import enum
import io
import logging
from typing import ClassVar
import xml.etree.ElementTree as ET

from prettyqt import constants, core, itemmodels
from prettyqt.utils import datatypes


logger = logging.getLogger(__name__)


class XmlColumnItem(itemmodels.ColumnItem):
    def get_data(self, item: XmlModel.TreeItem, role: constants.ItemDataRole):
        match role:
            case XmlModel.Roles.NodeRole:
                return item.obj


class TagColumn(XmlColumnItem):
    name = "Tag"
    doc = "Tag"

    def get_data(self, item: XmlModel.TreeItem, role: constants.ItemDataRole):
        match role:
            case constants.DISPLAY_ROLE:
                return item.obj.tag
        return super().get_data(item, role)


class TextColumn(XmlColumnItem):
    name = "Text"
    doc = "Text"

    def get_data(self, item: XmlModel.TreeItem, role: constants.ItemDataRole):
        match role:
            case constants.DISPLAY_ROLE:
                return item.obj.text
        return super().get_data(item, role)


class TailColumn(XmlColumnItem):
    name = "Tail"
    doc = "Tail"

    def get_data(self, item: XmlModel.TreeItem, role: constants.ItemDataRole):
        match role:
            case constants.DISPLAY_ROLE:
                return item.obj.tail
        return super().get_data(item, role)


class AttributeColumn(XmlColumnItem):
    name = "Attribute"
    doc = "Attribute"

    def get_data(self, item: XmlModel.TreeItem, role: constants.ItemDataRole):
        match role:
            case constants.DISPLAY_ROLE:
                return item.obj.attrib
        return super().get_data(item, role)


class BaseXmlModel(itemmodels.ColumnItemModel):
    ICON = "mdi.xml"
    COLUMNS: ClassVar = [TagColumn, TextColumn, TailColumn, AttributeColumn]

    def __init__(self, obj, **kwargs):
        super().__init__(obj=obj, columns=self.COLUMNS, show_root=True, **kwargs)

    class Roles(enum.IntEnum):
        NodeRole = constants.USER_ROLE + 24245

    def _has_children(self, item: XmlModel.TreeItem) -> bool:
        return len(item.obj) > 0

    def _fetch_object_children(self, item: XmlModel.TreeItem) -> list[XmlModel.TreeItem]:
        return [self.TreeItem(obj=i) for i in item.obj]


class XmlModel(BaseXmlModel):
    """Semi-lazy xml model. Fetches all direct child nodes when needed.

    Model cant be modified, that only really makes sense for a full DOM implementation.
    """

    SUPPORTS = io.StringIO | str | datatypes.IsTreeIterator | ET.ElementTree

    def __init__(
        self,
        obj: str | datatypes.IsTreeIterator | ET.ElementTree,
        show_root: bool = True,
        **kwargs,
    ):
        match obj:
            case io.StringIO():
                context = ET.iterparse(obj, events=("start",))
                _, root = next(context)
            case str():
                context = ET.iterparse(io.StringIO(obj), events=("start",))
                _, root = next(context)
            case datatypes.IsTreeIterator():
                _, root = next(obj)
            case ET.ElementTree():
                xml_str = ET.tostring(obj._root, encoding="unicode")
                context = ET.iterparse(io.StringIO(xml_str), events=("start",))
                _, root = next(context)
            case _:
                raise TypeError(obj)
        super().__init__(obj=root, **kwargs)

    @classmethod
    def supports(cls, instance) -> bool:
        match instance:
            case datatypes.IsTreeIterator() | ET.ElementTree():
                return True
            case _:
                return False

    def get_parent_node(self, node_or_index: core.ModelIndex | ET.Element):
        # only lxml has Element.getparent()
        # for builtin Elements we need to go through indexes since we do not have a
        # full ElementTree.
        # might be worth having two XML models, a lazy one and a full-featured one.
        # Then we could use xpath to get parent here.
        if isinstance(node_or_index, core.ModelIndex):
            index = node_or_index
        elif indexes := self.search_tree(
            node_or_index, role=self.Roles.NodeRole, max_results=1
        ):
            index = indexes[0]
        else:
            return None
        parent = index.parent()
        return parent.data(self.Roles.NodeRole)


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    xml = """<root>
<element key='value'>text</element>
<element><sub>text</sub></element>
<empty-element xmlns="http://testns/" />
</root>
"""
    xml = ET.parse(io.StringIO(xml))
    table = widgets.TreeView()
    model = XmlModel(xml, parent=table)
    table.setRootIsDecorated(True)
    # table.setSortingEnabled(True)
    table.set_model(model)

    def test(new, old):
        node = new.data(new.model().Roles.NodeRole)
        new.model().get_parent_node(node)

    table.selectionModel().currentChanged.connect(test)
    table.show()
    with app.debug_mode():
        app.exec()
