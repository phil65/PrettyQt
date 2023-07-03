from __future__ import annotations

import io
import logging

from lxml import etree

from prettyqt import core, custom_models


logger = logging.getLogger(__name__)


class LxmlModel(custom_models.BaseXmlModel):
    """Semi-lazy xml model based on lxml. Fetches all direct child nodes when needed.

    Model cant be modified, that only really makes sense for a full DOM implementation.
    """

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
    table.show()
    with app.debug_mode():
        app.exec()
