from __future__ import annotations

import io
import xml.etree.ElementTree as ET

from prettyqt import custom_models
from prettyqt.utils import datatypes, treeitem


COL_TAG = custom_models.ColumnItem(
    name="Tag",
    doc="Tag.",
    label=lambda x: x.obj.tag,
)


COL_TEXT = custom_models.ColumnItem(
    name="Text",
    doc="Text.",
    label=lambda x: x.obj.text,
)


COL_TAIL = custom_models.ColumnItem(
    name="Tail",
    doc="Tail.",
    label=lambda x: x.obj.tail,
)


COL_ATTRIB = custom_models.ColumnItem(
    name="Attributes",
    doc="Attributes.",
    label=lambda x: repr(x.obj.attrib),
)


COLUMNS = [COL_TAG, COL_TEXT, COL_ATTRIB, COL_TAIL]


class XmlModel(custom_models.ColumnItemModel):
    """Semi-lazy xml model. Fetches all direct child items when accessing index."""

    def __init__(
        self,
        obj: str | datatypes.IsTreeIterator | ET.ElementTree,
        show_root: bool = True,
        **kwargs,
    ):
        match obj:
            case str():
                context = ET.iterparse(io.StringIO(obj), events=("start",))
                _, root = next(context)
            case datatypes.IsTreeIterator():
                _, root = next(obj)
            case ET.ElementTree():
                xml_str = ET.tostring(xml._root, encoding="unicode")
                context = ET.iterparse(io.StringIO(xml_str), events=("start",))
                _, root = next(context)
        super().__init__(
            obj=root,
            columns=COLUMNS,
            show_root=show_root,
            **kwargs,
        )

    @classmethod
    def supports(cls, instance) -> bool:
        return isinstance(instance, datatypes.IsTreeIterator | ET.ElementTree)

    def _has_children(self, item: treeitem.TreeItem) -> bool:
        return bool(item.obj)

    def _fetch_object_children(self, item: treeitem.TreeItem) -> list[treeitem.TreeItem]:
        return [treeitem.TreeItem(obj=i) for i in item.obj]


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
    table.show()
    app.main_loop()
