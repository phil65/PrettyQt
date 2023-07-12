from __future__ import annotations

import inspect
import logging

from prettyqt import constants, core, gui, itemmodels, widgets
from prettyqt.utils import classhelpers, datatypes, helpers, markdownizer


BASE_URL = "https://doc.qt.io/qtforpython-6/PySide6/"
SLICE_PROXY_INFO = """This is a [slice proxy](SliceIdentityProxyModel.md)
and can be selectively applied to a model."""
RECURSIVE_MODEL_INFO = "Model can be recursive, so be careful with iterating whole tree."

logger = logging.getLogger(__name__)


class PrettyQtClassDocument(markdownizer.ClassDocument):
    def _build(self):
        super()._build()
        if issubclass(self.klass, core.AbstractItemModelMixin) and issubclass(
            self.klass, core.QObject
        ):
            sig = inspect.signature(self.klass.__init__)
            params = list(sig.parameters.values())
            if len(params) > 1:
                typ = params[1].annotation
                self.append(
                    markdownizer.Admonition("info", f"Supported data type: `{typ}`")
                )
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
                self.append(f"Qt Base Class: {markdownizer.link_for_class(qt_parent)}")
        if hasattr(self.klass, "ID") and issubclass(self.klass, gui.Validator):
            self.append(f"\n\nValidator ID: **{self.klass.ID}**\n\n")
        if hasattr(self.klass, "ID") and issubclass(
            self.klass, widgets.AbstractItemDelegateMixin
        ):
            self.append(f"\n\nDelegate ID: **{self.klass.ID}**\n\n")
        # if (
        #     hasattr(klass, "setup_example")
        #     and "Abstract" not in klass.__name__
        #     and not klass.__name__.endswith("Mixin")
        # ):
        #     if widget := klass.setup_example():
        #         doc += markdownizer.WidgetScreenShot(
        #             widget=widget,
        #             path=full_doc_path.parent / f"{kls_name}.png",
        #             header="🖼 Screenshot",
        #         )


class PrettyQtModuleDocument(markdownizer.ClassDocument):
    pass


class WidgetScreenShot(markdownizer.BinaryImage):
    def __init__(
        self,
        widget: widgets.QWidget,
        path: str,
        caption: str = "",
        title: str = "Image title",
        header: str = "",
        resize_to: datatypes.SizeType | None = None,
    ):
        logger.info(f"Screenshot for {widget}")
        widget.setAttribute(constants.WidgetAttribute.WA_DontShowOnScreen)
        # widget.add(widget)
        widgets.app().processEvents()
        widget.show()
        widgets.app().processEvents()
        widget.adjustSize()
        widgets.app().processEvents()
        pixmap = widget.grab()
        widgets.app().processEvents()
        widget.hide()
        widgets.app().processEvents()
        ba = core.ByteArray()
        buffer = core.QBuffer(ba)
        buffer.open(core.QIODeviceBase.OpenModeFlag.WriteOnly)
        pixmap.save(buffer, "PNG")
        super().__init__(
            data=ba.data(), path=path, header=header, caption=caption, title=title
        )


def model_to_markdown(
    model: core.AbstractItemModelMixin, use_checkstate_role: bool = True, **kwargs
) -> str:
    data, h_header, v_header = model.get_table_data(**kwargs)
    if use_checkstate_role:
        kwargs["role"] = constants.CHECKSTATE_ROLE
        check_data, _, __ = model.get_table_data(**kwargs)
        for i, row in enumerate(data):
            for j, _column in enumerate(row):
                if check_data[i][j]:
                    data[i][j] = "x"

    lines = [f"|{'|'.join(h_header)}|", f"|{'--|--'.join('' for _ in h_header)}|"]
    for row in data:
        sections = [str(i) if i else "" for i in row]
        lines.append(f"|{'|'.join(sections)}|")
    return "\n".join(lines)


def to_mermaid_tree(index: core.ModelIndex, role=constants.DISPLAY_ROLE):
    indexes, inheritances = helpers.get_connections(
        [index],
        child_getter=lambda x: x.model().iter_tree(x, depth=1, fetch_more=True),
        id_getter=lambda x: x.data(role),
    )
    text = index_tree_to_mermaid(indexes, inheritances)
    lines = ["\n\n## Index diagram\n\n``` mermaid\n", text, "\n```\n"]
    return "".join(lines)


def index_tree_to_mermaid(klasses, inheritances):
    return "graph TD;\n" + "\n".join(
        list(klasses) + [f"{a} --> {b}" for a, b in inheritances]
    )


if __name__ == "__main__":
    doc = markdownizer.Document([], True, True)
    doc += markdownizer.Admonition("info", "etst")
    doc += markdownizer.Table(data=dict(a=[1, 2], b=["c", "D"]), header="From mapping")
    doc += markdownizer.Table.get_prop_tables_for_klass(core.StringListModel)[0]
    doc += markdownizer.DocStrings(helpers, header="DocStrings")
    doc += markdownizer.Table.get_dependency_table("prettyqt")
    doc += markdownizer.MermaidDiagram.for_classes(
        [markdownizer.Table], header="Mermaid diagram"
    )

    print(doc.to_markdown())
