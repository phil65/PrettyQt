from __future__ import annotations

from typing import Any

from prettyqt import core, custom_models
from prettyqt.utils import treeitem
import xml.etree.ElementTree as ET
import io


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
        obj: Any,
        show_root: bool = True,
        **kwargs,
    ):
        context = ET.iterparse(io.StringIO(obj), events=("start",))
        _, root = next(context)

        super().__init__(
            obj=root,
            columns=COLUMNS,
            show_root=show_root,
            **kwargs,
        )

    def hasChildren(self, parent: core.ModelIndex | None = None):
        parent = parent or core.ModelIndex()
        if parent.column() > 0:
            return False
        item = self.data_by_index(parent)
        return True if self.show_root and item == self._root_item else bool(item.obj)

    def _fetch_object_children(self, item: treeitem.TreeItem) -> list[treeitem.TreeItem]:
        """Fetch the children of a Python object.

        Returns: list of treeitem.TreeItems
        """
        # items = []
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
    table = widgets.TreeView()
    model = XmlModel(xml, parent=table)
    table.setRootIsDecorated(True)
    # table.setSortingEnabled(True)
    table.set_model(model)
    table.show()
    app.main_loop()
