from __future__ import annotations

import logging

import mknodes

from prettyqt import constants, core, prettyqtmarkdown, widgets
from prettyqt.utils import datatypes, helpers


logger = logging.getLogger(__name__)


class WidgetScreenShot(mknodes.MkBinaryImage):
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


if __name__ == "__main__":
    doc = mknodes.MkPage([], True, True)
    doc += mknodes.MkAdmonition("info", "etst")
    doc += mknodes.MkTable(data=dict(a=[1, 2], b=["c", "D"]), header="From mapping")
    doc += prettyqtmarkdown.PropertyTable(core.StringListModel)
    doc += mknodes.MkDocStrings(helpers, header="DocStrings")
    doc += prettyqtmarkdown.DependencyTable("prettyqt")
    doc += mknodes.MkClassDiagram(mknodes.MkTable, header="Mermaid diagram")

    print(doc.to_markdown())
