from __future__ import annotations

import logging

from prettyqt import core, gui, itemmodels, widgets
from prettyqt.utils import classhelpers, helpers, markdownhelpers, markdownizer


BASE_URL = "https://doc.qt.io/qtforpython-6/PySide6/"
SLICE_PROXY_INFO = """This is a [slice proxy](SliceIdentityProxyModel.md)
and can be selectively applied to a model."""
RECURSIVE_MODEL_INFO = "Model can be recursive, so be careful with iterating whole tree."

logger = logging.getLogger(__name__)


class PrettyQtClassDocument(markdownizer.ClassDocument):
    def _build(self):
        super()._build()
        if issubclass(self.klass, itemmodels.SliceIdentityProxyModel):
            self.append(markdownizer.Admonition("info", SLICE_PROXY_INFO))
        if (
            issubclass(self.klass, core.AbstractItemModelMixin)
            and self.klass.IS_RECURSIVE
        ):
            self.append(markdownizer.Admonition("warning", RECURSIVE_MODEL_INFO))
        if (
            issubclass(self.klass, core.AbstractItemModelMixin)
            and self.klass.DELEGATE_DEFAULT is not None
        ):
            msg = f"Recommended delegate: {self.klass.DELEGATE_DEFAULT!r}"
            self.append(markdownizer.Admonition("info", msg))
        if issubclass(self.klass, core.QObject):
            # model = itemmodels.QObjectPropertiesModel()
            for table in markdownizer.Table.get_prop_tables_for_klass(self.klass):
                self.append(table)  # noqa: PERF402
            if qt_parent := classhelpers.get_qt_parent_class(self.klass):
                self.append(f"Qt Base Class: {markdownizer.get_qt_help_link(qt_parent)}")
        if hasattr(self.klass, "ID") and issubclass(self.klass, gui.Validator):
            self.append(f"\n\nValidator ID: **{self.klass.ID}**\n\n")
        if hasattr(self.klass, "ID") and issubclass(
            self.klass, widgets.AbstractItemDelegateMixin
        ):
            self.append(f"\n\nDelegate ID: **{self.klass.ID}**\n\n")


if __name__ == "__main__":
    doc = markdownizer.Document([], True, True)
    doc += markdownizer.Admonition("info", "etst")
    doc += markdownizer.Table(data=dict(a=[1, 2], b=["c", "D"]), header="From mapping")
    doc += markdownizer.Table.get_prop_tables_for_klass(core.StringListModel)[0]
    doc += markdownizer.DocStringSection(helpers, header="DocStrings")
    doc += markdownizer.Table.get_dependency_table("prettyqt")
    doc += markdownizer.MermaidDiagram.for_classes(
        [markdownizer.Table], header="Mermaid diagram"
    )

    print(doc.to_markdown())
    logger.info(markdownhelpers.get_mermaid_for_klass(markdownizer.Table))
    # print(text)
