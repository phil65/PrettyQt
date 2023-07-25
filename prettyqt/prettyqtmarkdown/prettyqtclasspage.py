from __future__ import annotations

import logging

import mknodes

from mknodes.utils import helpers

from prettyqt import core, gui, itemmodels, prettyqtmarkdown, widgets
from prettyqt.utils import classhelpers


SLICE_PROXY_INFO = """This is a [slice proxy](SliceIdentityProxyModel.md)
and can be selectively applied to a model. Read more about
 [slices](https://docs.python.org/3/library/functions.html#slice)."""

RECURSIVE_MODEL_INFO = "Model can be recursive, so be careful with iterating whole tree."

logger = logging.getLogger(__name__)
app = widgets.app()


class PrettyQtClassPage(mknodes.MkClassPage):
    """A ClassPage specifically for Qt-based classes."""

    def _build(self):
        if qt_parent := classhelpers.get_qt_parent_class(self.klass):
            self.append(f"Qt Base Class: {helpers.link_for_class(qt_parent)}")
            self.append(f"Signature: `{qt_parent.__doc__}`")
        super()._build()
        if issubclass(self.klass, itemmodels.SliceIdentityProxyModel):
            self.add_admonition(SLICE_PROXY_INFO)
        if (
            issubclass(self.klass, core.AbstractItemModelMixin)
            and self.klass.IS_RECURSIVE
        ):
            self.add_admonition(RECURSIVE_MODEL_INFO, "warning")
        if (
            issubclass(self.klass, core.AbstractItemModelMixin)
            and self.klass.DELEGATE_DEFAULT is not None
        ):
            msg = f"Recommended delegate: {self.klass.DELEGATE_DEFAULT!r}"
            self.add_admonition(msg)
        if issubclass(self.klass, core.AbstractItemModelMixin) and hasattr(
            self.klass, "SUPPORTS"
        ):
            self.add_admonition(f"Supported data type: `{self.klass.SUPPORTS}`")
        if issubclass(self.klass, core.QObject):
            table = prettyqtmarkdown.PropertyTable(self.klass, header="⌗ Property table")
            self.append(table)
        if hasattr(self.klass, "ID") and issubclass(self.klass, gui.Validator):
            self.append(f"\n\nValidator ID: **{self.klass.ID}**\n\n")
        if hasattr(self.klass, "ID") and issubclass(
            self.klass, widgets.AbstractItemDelegateMixin
        ):
            self.append(f"\n\nDelegate ID: **{self.klass.ID}**\n\n")
        if (
            hasattr(self.klass, "setup_example")
            and "Abstract" not in self.klass.__name__
            and not self.klass.__name__.endswith("Mixin")
        ):
            if widget := self.klass.setup_example():
                self += prettyqtmarkdown.WidgetScreenShot(widget, header="🖼 Screenshot")


if __name__ == "__main__":
    page = PrettyQtClassPage(klass=core.StringListModel)
    print(page.to_markdown())
