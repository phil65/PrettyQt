from __future__ import annotations

from prettyqt import constants, core, gui, widgets


class CodeEditor(widgets.PlainTextEdit):
    """Super basic code editor."""

    def __init__(self, language: str = "python", **kwargs):
        super().__init__(**kwargs)
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


if __name__ == "__main__":
    app = widgets.app()
    dlg = CodeEditor()
    dlg.show()
    app.exec()
