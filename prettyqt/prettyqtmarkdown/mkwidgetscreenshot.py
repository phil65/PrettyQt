from __future__ import annotations

import logging

import mknodes

from prettyqt import constants, core, widgets
from prettyqt.utils import datatypes


logger = logging.getLogger(__name__)


class MkWidgetScreenShot(mknodes.MkBinaryImage):
    """Node to easily create and embed a widget screenshot into docs."""

    def __init__(
        self,
        widget: widgets.QWidget,
        caption: str = "",
        path: str | None = None,
        title: str = "Image title",
        header: str = "",
        resize_to: datatypes.SizeType | None = None,
    ):
        """Constructor.

        Arguments:
            widget: Widget to make a screenshot from
            caption: Image caption
            path: Image path
            title: Image title
            header: Section header
            resize_to: widget screenshot size
        """
        if path is None:
            path = f"{widget.__class__.__name__}_screenshot.png"
        logger.info(f"Screenshot for {widget}")
        widget.setAttribute(constants.WidgetAttribute.WA_DontShowOnScreen)
        widget.show()
        widget.adjustSize()
        widgets.app().processEvents()
        pixmap = widget.grab()
        widget.hide()
        widget.deleteLater()
        widgets.app().processEvents()
        ba = core.ByteArray()
        buffer = core.QBuffer(ba)
        buffer.open(core.QIODeviceBase.OpenModeFlag.WriteOnly)
        pixmap.save(buffer, "PNG")
        super().__init__(
            data=ba.data(),
            path=path,
            header=header,
            caption=caption,
            title=title,
        )


if __name__ == "__main__":
    app = widgets.app()

    w = widgets.PushButton("Test")
    page = mknodes.MkPage()
    page += MkWidgetScreenShot(w, "test.png")
    print(page.to_markdown())
