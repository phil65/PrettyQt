from __future__ import annotations

from collections.abc import Mapping
import dataclasses
from typing import TYPE_CHECKING, Literal

from prettyqt import constants, core, gui, widgets


if TYPE_CHECKING:
    from collections.abc import Iterable


MarkerKindStr = Literal["error", "warning", "info"]

MARKER_COLORS: Mapping[MarkerKindStr, tuple[int, int, int]] = {
    "error": (220, 50, 47),
    "warning": (230, 160, 0),
    "info": (38, 139, 210),
}


@dataclasses.dataclass(frozen=True)
class LineMarker:
    """A message attached to a line of a CodeEditor (line numbers start at 1)."""

    line: int
    message: str
    kind: MarkerKindStr = "error"


class CodeEditor(widgets.PlainTextEdit):
    """Code editor with line numbers, syntax highlighting and line markers.

    Line markers (errors / warnings / infos) tint the line and its number;
    hovering the line number or the line shows the marker messages as tooltip.
    `set_text()` keeps cursor and scroll position (and the undo history).
    """

    def __init__(self, language: str = "python", **kwargs):
        super().__init__(**kwargs)
        self._markers: dict[int, list[LineMarker]] = {}
        self.line_area = LineNumberArea(self)
        self.blockCountChanged.connect(self.update_line_area_width)
        self.updateRequest.connect(self.update_line_area)
        self.set_font(gui.Font.mono(as_qt=True))
        self.update_line_area_width(0)
        self.set_current_line_color(gui.Color(128, 128, 128, 20))
        self.set_syntaxhighlighter(language)

    #     self.delimiter = "    "
    #     self.completion_state = 0
    #     self.completing = False
    #     self.cursorPositionChanged.connect(self.reset_completion)

    # def keyPressEvent(self, event):
    #     match event.key():
    #         case constants.Key.Key_Backtab if self.textCursor().hasSelection():
    #             start_cursor = self.get_textCursor()
    #             with start_cursor.edit_block():
    #                 start_pos = start_cursor.selectionStart()
    #                 start_cursor.setPosition(start_pos)
    #                 start_cursor.move_position("start_of_line")
    #                 start_cursor.clearSelection()
    #                 end_cursor = self.get_text_cursor()
    #                 end_pos = end_cursor.selectionEnd()
    #                 end_cursor.setPosition(end_pos)
    #                 end_cursor.move_position("start_of_line")
    #                 delimit_len = len(self.delimiter)
    #                 while start_cursor.anchor() != end_cursor.position():
    #                     start_cursor.move_position(
    #                         "next_character", mode="keep", n=delimit_len
    #                     )
    #                     if start_cursor.selectedText() == self.delimiter:
    #                         start_cursor.removeSelectedText()
    #                     start_cursor.move_position("next_block")
    #                 start_cursor.move_position(
    #                     "next_character", mode="keep", n=delimit_len
    #                 )
    #                 if start_cursor.selectedText() == self.delimiter:
    #                     start_cursor.removeSelectedText()
    #         case constants.Key.Key_Tab if self.textCursor().hasSelection():
    #             start_cursor = self.get_text_cursor()
    #             with start_cursor.edit_block():
    #                 start_pos = start_cursor.selectionStart()
    #                 start_cursor.setPosition(start_pos)
    #                 start_cursor.move_position("start_of_line")
    #                 end_cursor = self.get_text_cursor()
    #                 end_pos = end_cursor.selectionEnd()
    #                 end_cursor.setPosition(end_pos)
    #                 end_cursor.move_position("start_of_line")
    #                 while start_cursor.position() != end_cursor.position():
    #                     start_cursor.insertText(self.delimiter)
    #                     start_cursor.move_position("next_block")
    #                 start_cursor.insertText(self.delimiter)
    #         case constants.Key.Key_Escape if self.completion_state > 0:
    #             self.completion_state = 0
    #             cursor = self.get_text_cursor()
    #             with cursor.edit_block():
    #                 self.selecter.replace_block_at_cursor(self._orig_text)
    #             self._orig_text == None
    #         case constants.Key.Key_Tab:
    #             if self.is_start():
    #                 self.textCursor().insertText(self.delimiter)
    #             else:
    #                 cursor = self.get_text_cursor()
    #                 with cursor.edit_block():
    #                     self.completing = True
    #                     if self.completion_state == 0:
    #                         self._orig_text = self.textCursor().block().text()
    #                     if self.completion_state > 0:
    #                         self.selecter.replace_block_at_cursor(self._orig_text)
    #                     new_text = self.completer.complete(
    #                         self._orig_text, self.completion_state
    #                     )
    #                     if new_text:
    #                         if new_text.find("(") > 0:
    #                             new_text = new_text[0 : new_text.find("(") + 1]
    #                         self.completion_state += 1
    #                         self.selecter.replace_block_at_cursor(new_text)
    #                     else:
    #                         self.completion_state = 0
    #                         self.selecter.replace_block_at_cursor(self._orig_text)
    #                         self._orig_text == None
    #                 self.completing = False
    #         case _:
    #             return super().keyPressEvent(event)

    # def reset_completion(self):
    #     if not self.completing:
    #         self.completion_state = 0

    # def is_start(self) -> bool:
    #     temp_cursor = self.textCursor()
    #     if temp_cursor.positionInBlock() == 0:
    #         return True
    #     start_text = temp_cursor.block().text()[0 : temp_cursor.positionInBlock()]
    #     delim = set(self.delimiter)
    #     return set(start_text) - delim == set()

    def set_syntaxhighlighter(
        self, syntax: str | gui.QSyntaxHighlighter, style: str | None = None
    ):
        """Set the highlighter; the previous one is detached from the document."""
        old = getattr(self, "_hl", None)
        if old is not None and old is not syntax:
            old.setDocument(None)
            old.deleteLater()
        super().set_syntaxhighlighter(syntax, style)

    def set_text(self, text: str, *, keep_position: bool = True):
        """Set the text.

        Args:
            text: new text
            keep_position: keep cursor position, selection and scroll position, and
                           make the change undoable (instead of resetting the document)
        """
        if not keep_position:
            self.setPlainText(text)
            return
        if text == self.toPlainText():
            return
        cursor = self.textCursor()
        anchor, position = cursor.anchor(), cursor.position()
        h_value = self.horizontalScrollBar().value()
        v_value = self.verticalScrollBar().value()
        edit_cursor = gui.QTextCursor(self.document())
        edit_cursor.beginEditBlock()
        edit_cursor.select(gui.QTextCursor.SelectionType.Document)
        edit_cursor.insertText(text)
        edit_cursor.endEditBlock()
        last = max(len(text), 0)
        cursor = self.textCursor()
        cursor.setPosition(min(anchor, last))
        cursor.setPosition(min(position, last), gui.QTextCursor.MoveMode.KeepAnchor)
        self.setTextCursor(cursor)
        self.verticalScrollBar().setValue(v_value)
        self.horizontalScrollBar().setValue(h_value)

    def set_value(self, value: str):
        self.set_text(value)

    # --- line markers -----------------------------------------------------

    def add_line_marker(self, line: int, message: str, kind: MarkerKindStr = "error"):
        """Attach a message to a line (1-based line number)."""
        if kind not in MARKER_COLORS:
            msg = f"Invalid marker kind {kind!r}"
            raise ValueError(msg)
        self._markers.setdefault(line, []).append(LineMarker(line, message, kind))
        self._update_markers()

    def set_line_markers(
        self,
        markers: Mapping[int, str] | Iterable[LineMarker | tuple[int, str]],
        kind: MarkerKindStr = "error",
    ):
        """Replace all markers.

        Args:
            markers: {line: message}, LineMarkers or (line, message) tuples
            kind: kind for markers given as mapping / tuples
        """
        self._markers.clear()
        items = markers.items() if isinstance(markers, Mapping) else markers
        for item in items:
            if isinstance(item, LineMarker):
                marker = item
            else:
                marker = LineMarker(item[0], item[1], kind)
            self._markers.setdefault(marker.line, []).append(marker)
        self._update_markers()

    def clear_line_markers(self, line: int | None = None):
        """Remove the markers of a line, or all markers."""
        if line is None:
            self._markers.clear()
        else:
            self._markers.pop(line, None)
        self._update_markers()

    def get_line_markers(self) -> list[LineMarker]:
        return [m for line in sorted(self._markers) for m in self._markers[line]]

    def get_line_marker_text(self, line: int) -> str:
        """Return the messages of a line, one per row ("" if none)."""
        return "\n".join(m.message for m in self._markers.get(line, []))

    def _marker_color(self, line: int, alpha: int) -> gui.Color | None:
        if not (markers := self._markers.get(line)):
            return None
        kind = min((m.kind for m in markers), key=list(MARKER_COLORS).index)
        return gui.Color(*MARKER_COLORS[kind], alpha)

    def _update_markers(self):
        selections = []
        doc = self.document()
        for line in sorted(self._markers):
            block = doc.findBlockByNumber(line - 1)
            if not block.isValid():
                continue
            selection = widgets.QTextEdit.ExtraSelection()
            selection.format.setBackground(self._marker_color(line, 50))
            prop = gui.QTextFormat.Property.FullWidthSelection
            selection.format.setProperty(prop, True)
            selection.cursor = gui.QTextCursor(block)
            selections.append(selection)
        self.setExtraSelections(selections)
        self.line_area.update()

    def _line_at(self, y: int) -> int | None:
        block = self.firstVisibleBlock()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        while block.isValid():
            bottom = top + self.blockBoundingRect(block).height()
            if top <= y < bottom:
                return block.blockNumber() + 1
            top = bottom
            block = block.next()
        return None

    def show_marker_tooltip(self, pos: core.QPoint, global_pos: core.QPoint) -> bool:
        line = self._line_at(pos.y())
        if line is None or not (text := self.get_line_marker_text(line)):
            widgets.ToolTip.hideText()
            return False
        widgets.ToolTip.showText(global_pos, text)
        return True

    def viewportEvent(self, event):
        if event.type() == core.QEvent.Type.ToolTip:
            self.show_marker_tooltip(event.pos(), event.globalPos())
            return True
        return super().viewportEvent(event)

    def resizeEvent(self, event):
        super().resizeEvent(event)

        cr = self.contentsRect()
        rect = core.Rect(cr.left(), cr.top(), self.line_area_width(), cr.height())
        self.line_area.setGeometry(rect)

    def line_area_width(self) -> int:
        digits = len(str(self.blockCount()))
        return 3 + self.fontMetrics().boundingRect("9").width() * digits

    def update_line_area_width(self, _):
        self.setViewportMargins(self.line_area_width(), 0, 0, 0)

    def update_line_area(self, rect: core.QRect, dy: int):
        if dy:
            self.line_area.scroll(0, dy)
        else:
            self.line_area.update(0, rect.y(), self.line_area.width(), rect.height())

        if rect.contains(self.viewport().rect()):
            self.update_line_area_width(0)

    def line_area_paintevent(self, event):
        with gui.Painter(self.line_area) as painter:
            painter.fill_rect(event.rect(), "lightgray")

            block = self.firstVisibleBlock()
            block_number = block.blockNumber()
            top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
            bottom = top + self.blockBoundingRect(block).height()
            width = self.line_area.width()
            height = self.fontMetrics().height()
            painter.set_color("black")
            while block.isValid() and (top <= event.rect().bottom()):
                if block.isVisible() and (bottom >= event.rect().top()):
                    number = str(block_number + 1)
                    if color := self._marker_color(block_number + 1, 160):
                        painter.fill_rect(
                            core.QRectF(0, top, width, bottom - top).toRect(), color
                        )
                    painter.drawText(
                        0, int(top), width, height, constants.ALIGN_RIGHT, number
                    )
                block = block.next()
                top = bottom
                bottom = top + self.blockBoundingRect(block).height()
                block_number += 1


class LineNumberArea(widgets.Widget):
    def __init__(self, editor: CodeEditor):
        super().__init__(editor)
        self.editor = editor

    def sizeHint(self) -> core.Size:
        return core.Size(self.editor.line_area_width(), 0)

    def paintEvent(self, event):
        self.editor.line_area_paintevent(event)

    def event(self, event):
        if event.type() == core.QEvent.Type.ToolTip:
            self.editor.show_marker_tooltip(event.pos(), event.globalPos())
            return True
        return super().event(event)


if __name__ == "__main__":
    app = widgets.app()
    dlg = CodeEditor()
    dlg.set_text("def f(x):\n    return x +\n")
    dlg.add_line_marker(2, "SyntaxError: invalid syntax")
    dlg.show()
    app.exec()
