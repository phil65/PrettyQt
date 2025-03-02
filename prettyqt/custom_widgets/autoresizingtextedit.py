from __future__ import annotations

from prettyqt import core, widgets


PM = widgets.QStyle.PixelMetric
SH = widgets.QStyle.StyleHint


class AutoResizeTextEditMixin:
    def __init__(self, parent=None):
        super().__init__(parent)
        self.set_line_wrap_mode("none")
        doc_layout = self.document().documentLayout()
        doc_layout.documentSizeChanged.connect(self.update_vertical_size)
        self.update_vertical_size()

    def update_vertical_size(self):
        # can vertical or horizontal scrollbars appear?
        vcan = self.get_vertical_scrollbar_policy() == "as_needed"
        hcan = self.get_horizontal_scrollbar_policy() == "as_needed"

        # width a scrollbar takes off the viewport size
        frame_width = 0
        style = self.style()
        if style.styleHint(SH.SH_ScrollView_FrameOnlyAroundContents, None, self):
            frame_width = style.pixelMetric(PM.PM_DefaultFrameWidth) * 2
        extent = style.pixelMetric(PM.PM_ScrollBarExtent, None, self) + frame_width
        doc = self.document()
        margin = frame_width + doc.documentMargin()
        size = self.get_document_size() + core.QSize(int(margin), int(margin))
        width = size.width()
        height = size.height()
        max_width = self.width()
        max_height = self.maximumHeight()
        # will scrollbars appear?
        hwill, vwill = False, False
        if hcan and width > max_width:
            hwill = True
        if vcan and height > max_height:
            vwill = True
        if vcan and hwill and height + extent > max_height:
            vwill = True
        if hcan and vwill and width + extent > max_width:
            hwill = True
        if hwill:
            height += extent
        self.resize(self.width(), min(max_height, height))

    def get_document_size(self):
        """Implemented differently for QTextEdit and QPlainTextEdit."""
        raise NotImplementedError

    def setLineWrapMode(self, mode):
        """Reimplemented to avoid WidgetWidth wrap mode, which causes resize loops."""
        if mode == self.LineWrapMode.WidgetWidth:
            msg = "cannot use WidgetWidth wrap mode"
            raise ValueError(msg)
        super().setLineWrapMode(mode)


class AutoResizeTextEdit(AutoResizeTextEditMixin, widgets.TextEdit):
    """TextEdit which adjusts its height to the contained text."""

    def get_document_size(self) -> core.QSize:
        return self.document().documentLayout().documentSize().toSize()


class AutoResizePlainTextEdit(AutoResizeTextEditMixin, widgets.PlainTextEdit):
    """PlainTextEdit which adjusts its height to the contained text."""

    def get_document_size(self) -> core.QSize:
        doc = self.document()
        layout = doc.documentLayout()
        size = layout.documentSize().toSize()
        block = doc.firstBlock()
        line_height = layout.blockBoundingRect(block).height() / block.lineCount()
        height = int(size.height() * line_height + 2 * doc.documentMargin())
        return core.QSize(size.width(), height)


if __name__ == "__main__":
    app = widgets.app()
    widget = widgets.Widget()
    layout = widget.set_layout("grid")
    textedit = AutoResizePlainTextEdit()
    layout[0, 1] = textedit
    widget.show()
    app.exec()
