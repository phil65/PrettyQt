from __future__ import annotations

import io
import logging

from lxml import etree

from prettyqt import core, itemmodels


logger = logging.getLogger(__name__)


class LxmlModel(itemmodels.BaseXmlModel):
    """DOM xml model based on lxml. Parses full xml.

    Covers more features than the lazy models. (modifying the tree, xpath, ..)
    """

    SUPPORTS = bytes | str | etree.ElementTree

    def __init__(
        self,
        obj: str | bytes | etree.ElementTree,
        **kwargs,
    ):
        match obj:
            case bytes():
                xml_str = etree.XML(obj.decode())
                tree = etree.ElementTree(xml_str)
            case str():
                tree = etree.ElementTree(etree.XML(obj))
            case etree.ElementTree():
                tree = obj
            case _:
                raise TypeError(obj)
        self.tree = tree
        super().__init__(obj=self.tree.getroot(), **kwargs)

    @classmethod
    def supports(cls, instance) -> bool:
        match instance:
            case etree.ElementTree():
                return True
            case _:
                return False

    def get_parent_node(self, node_or_index: core.ModelIndex | etree.Element):
        if not isinstance(node_or_index, core.ModelIndex):
            return node_or_index.getparent()
        index = node_or_index
        parent = index.parent()
        return parent.data(self.Roles.NodeRole)

    @staticmethod
    def get_key_for_element(element: etree.Element) -> list[int]:
        child_elem = element
        key = []
        while (parent_elem := child_elem.getparent()) is not None:
            key.append(parent_elem.index(child_elem))
            child_elem = parent_elem
        return key

    def get_indexes_from_xpath(self, xpath: str):
        elements = self.tree.xpath(xpath)
        keys = [self.get_key_for_element(element) for element in elements]
        [self.index_from_key(key) for key in keys]


class LazyLxmlModel(itemmodels.BaseXmlModel):
    """Semi-lazy xml model based on lxml. Fetches all direct child nodes when needed.

    Model cant be modified, that only really makes sense for a full DOM implementation.
    """

    SUPPORTS = io.BytesIO | bytes | str | etree.iterparse | etree.Element

    def __init__(
        self,
        obj: str | bytes | io.BytesIO | etree.ElementTree,
        tag: str | None = None,
        **kwargs,
    ):
        match obj:
            case io.BytesIO():
                context = etree.iterparse(obj, events=("start",), tag=tag)
                _, root = next(context)
            case bytes():
                context = etree.iterparse(io.BytesIO(obj), events=("start",), tag=tag)
                _, root = next(context)
            case str():
                context = etree.iterparse(
                    io.BytesIO(obj.encode()), events=("start",), tag=tag
                )
                _, root = next(context)
            case etree.iterparse():
                _, root = next(obj)
            case etree.Element():
                root = obj
            case _:
                raise TypeError(obj)
        super().__init__(obj=root, **kwargs)

    @classmethod
    def supports(cls, instance) -> bool:
        match instance:
            case etree.Element() | etree.iterparse():
                return True
            case _:
                return False

    def get_parent_node(self, node_or_index: core.ModelIndex | etree.Element):
        if not isinstance(node_or_index, core.ModelIndex):
            return node_or_index.getparent()
        index = node_or_index
        parent = index.parent()
        return parent.data(self.Roles.NodeRole)

    def get_key_for_element(self, element):
        child_elem = self
        key = []
        while parent_elem := child_elem.getparent():
            key.append(parent_elem.index(child_elem))
            child_elem = parent_elem
        return key


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    xml = """<root>
<element key='value'>text</element>
<element><sub>text</sub></element>
<empty-element xmlns="http://testns/" />
</root>
"""
    table = widgets.TreeView()
    model = LxmlModel(xml, parent=table)
    table.setRootIsDecorated(True)
    # table.setSortingEnabled(True)
    table.set_model(model)

    def test(new, old):
        node = new.data(new.model().Roles.NodeRole)
        new.model().get_parent_node(node)

    table.selectionModel().currentChanged.connect(test)
    print(model.get_indexes_from_xpath("element"))
    table.show()
    with app.debug_mode():
        app.exec()
