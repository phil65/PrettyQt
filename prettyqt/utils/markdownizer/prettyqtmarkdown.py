from __future__ import annotations

from importlib import metadata
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
        if qt_parent := classhelpers.get_qt_parent_class(self.klass):
            self.append(f"Qt Base Class: {markdownizer.link_for_class(qt_parent)}")
            self.append(f"Signature: `{qt_parent.__doc__}`")
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
        if issubclass(self.klass, core.AbstractItemModelMixin) and hasattr(
            self.klass, "SUPPORTS"
        ):
            msg = f"Supported data type: `{self.klass.SUPPORTS}`"
            self.append(markdownizer.Admonition("info", msg))
        if issubclass(self.klass, core.QObject):
            self.append(markdownizer.PropertyTable(self.klass, header="Property table"))
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


class PropertyTable(markdownizer.Table):
    def __init__(
        self,
        qobject: core.QObject | type[core.QObject],
        user_prop_name: str | None = None,
        header: str = "",
    ):
        lines = []
        headers = ["Qt Property", "Type", "Options"]
        if isinstance(qobject, core.QObject):
            properties = core.MetaObject(qobject.metaObject()).get_properties()
        elif issubclass(qobject, core.QObject):
            properties = core.MetaObject(qobject.staticMetaObject).get_properties()
        for prop in properties:
            property_name = f"`{prop.get_name()}`"
            if prop.get_name() == user_prop_name:
                property_name += " *(User property)*"
            # if (flag := prop.get_enumerator()):

            meta_type = prop.get_meta_type()
            property_type = f"**{(meta_type.get_name() or '').rstrip('*')}**"
            sections: list[str] = [
                property_name,
                property_type,
                "x" if prop.get_name() == user_prop_name else "",
            ]
            lines.append(sections)
        super().__init__(columns=headers, data=list(zip(*lines)), header=header)


class ItemModelTable(markdownizer.Table):
    def __init__(
        self,
        model: core.AbstractItemModelMixin,
        use_checkstate_role: bool = True,
        **kwargs,
    ):
        proxy = itemmodels.SliceToMarkdownProxyModel(None, source_model=model)
        data, h_header, _ = proxy.get_table_data(
            use_checkstate_role=use_checkstate_role, **kwargs
        )
        data = list(zip(*data))
        super().__init__(data, columns=h_header)


class DependencyTable(ItemModelTable):
    def __init__(self, distribution: str | metadata.Distribution = "prettyqt"):
        model = itemmodels.ImportlibTreeModel(distribution)
        proxy = itemmodels.ColumnOrderProxyModel(
            order=["Name", "Constraints", "Extra", "Summary", "Homepage"],
            source_model=model,
        )
        super().__init__(proxy)


class MarkdownModel(itemmodels.TreeModel):
    def columnCount(self, index):
        return 3

    def data(self, index, role):
        data = self.data_by_index(index).obj
        match role, index.column():
            case constants.DISPLAY_ROLE, 0:
                return repr(data)
            case constants.DISPLAY_ROLE, 1:
                return data.to_markdown().count("\n")
            # case constants.DISPLAY_ROLE, 2:
            #     return data.to_markdown()

    def _fetch_object_children(self, treeitem) -> list[MarkdownModel.TreeItem]:
        return [self.TreeItem(i) for i in treeitem.obj.children]

    def _has_children(self, treeitem) -> bool:
        return len(treeitem.obj.children) > 0


if __name__ == "__main__":
    doc = markdownizer.Document([], True, True)
    doc += markdownizer.Admonition("info", "etst")
    doc += markdownizer.Table(data=dict(a=[1, 2], b=["c", "D"]), header="From mapping")
    doc += markdownizer.PropertyTable(core.StringListModel)
    doc += markdownizer.DocStrings(helpers, header="DocStrings")
    doc += markdownizer.DependencyTable("prettyqt")
    doc += markdownizer.MermaidDiagram.for_classes(
        [markdownizer.Table], header="Mermaid diagram"
    )

    print(doc.to_markdown())
