from __future__ import annotations

import logging

import mknodes
from mknodes.pages import processors

from prettyqt import core, gui, itemmodels, prettyqtmarkdown, widgets
from prettyqt.utils import classhelpers


SLICE_PROXY_INFO = """This is a [slice proxy](SliceIdentityProxyModel.md)
and can be selectively applied to a model. Read more about
 [slices](https://docs.python.org/3/library/functions.html#slice)."""

RECURSIVE_MODEL_INFO = "Model can be recursive, so be careful with iterating whole tree."

logger = logging.getLogger(__name__)
app = widgets.app()


class QtParentContainerProcessor(processors.ContainerProcessor):
    ID = "qt_signature"

    def append_block(self, page: mknodes.MkPage):
        qt_parent = classhelpers.get_qt_parent_class(self.item)
        assert qt_parent
        provider = page.ctx.links if page.ctx else prettyqtmarkdown.QtLinkProvider()
        page += f"Qt Base Class: {provider.link_for_klass(qt_parent)}"
        page += f"Signature: `{qt_parent.__doc__}`"

    def get_default_header(self, page: mknodes.MkPage):
        return ""

    def check_if_apply(self, page: mknodes.MkPage):
        return bool(classhelpers.get_qt_parent_class(self.item))


class QtScreenshotContainerProcessor(processors.ContainerProcessor):
    ID = "qt_signature"

    def append_block(self, page: mknodes.MkPage):
        if widget := self.item.setup_example():
            page += mknodes.MkCode.for_object(self.item.setup_example)
            page += prettyqtmarkdown.MkWidgetScreenShot(widget)

    def get_default_header(self, page: mknodes.MkPage):
        return "🖼 Screenshot"

    def check_if_apply(self, page: mknodes.MkPage):
        return (
            "setup_example" in self.item.__dict__
            and "Abstract" not in self.item.__name__
            and not self.item.__name__.endswith("Mixin")
        )


class QtContainerProcessor(processors.ContainerProcessor):
    ID = "qt"

    def append_block(self, page: mknodes.MkPage):
        if issubclass(self.item, itemmodels.SliceIdentityProxyModel):
            page += mknodes.MkAdmonition(SLICE_PROXY_INFO)
        if issubclass(self.item, core.AbstractItemModelMixin) and self.item.IS_RECURSIVE:
            page += mknodes.MkAdmonition(RECURSIVE_MODEL_INFO, typ="warning")
        if (
            issubclass(self.item, core.AbstractItemModelMixin)
            and self.item.DELEGATE_DEFAULT is not None
        ):
            msg = f"Recommended delegate: {self.item.DELEGATE_DEFAULT!r}"
            page += mknodes.MkAdmonition(msg)
        if issubclass(self.item, core.AbstractItemModelMixin) and hasattr(
            self.item, "SUPPORTS"
        ):
            page += mknodes.MkAdmonition(f"Supported data type: `{self.item.SUPPORTS}`")
        if issubclass(self.item, core.QObject):
            header = "⌗ Property table"
            table = prettyqtmarkdown.MkPropertyTable(self.item, header=header)
            page += table
        if hasattr(self.item, "ID") and issubclass(self.item, gui.Validator):
            page += f"\n\nValidator ID: **{self.item.ID}**\n\n"
        if hasattr(self.item, "ID") and issubclass(
            self.item, widgets.AbstractItemDelegateMixin
        ):
            page += f"\n\nDelegate ID: **{self.item.ID}**\n\n"

    def get_default_header(self, page: mknodes.MkPage):
        return ""


class MkPrettyQtClassPage(mknodes.MkClassPage):
    """A ClassPage specifically for Qt-based classes."""

    def get_pageprocessors(self):
        processors = super().get_pageprocessors()
        return [
            QtParentContainerProcessor(self.klass),
            *processors,
            QtContainerProcessor(self.klass),
            QtScreenshotContainerProcessor(self.klass),
        ]


if __name__ == "__main__":
    page = MkPrettyQtClassPage(klass=core.StringListModel)
    print(page.to_markdown())
