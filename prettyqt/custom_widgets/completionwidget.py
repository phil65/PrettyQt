"""A dropdown completer widget for the text edits."""

from __future__ import annotations

import os

from prettyqt import gui, widgets
from prettyqt.qt import QtCore, QtGui, QtWidgets


class CompletionWidget(widgets.ListWidget):
    def __init__(self, textedit: QtWidgets.QTextEdit | QtWidgets.QPlainTextEdit):
        super().__init__(parent=textedit)

        self._text_edit = textedit
        self.set_edit_triggers("none")
        self.set_selection_behaviour("rows")
        self.set_selection_mode("single")

        # We need Popup style to ensure correct mouse interaction
        # (dialog would dissappear on mouse click with ToolTip style)
        self.setWindowFlags(QtCore.Qt.WindowType.Popup)  # type: ignore

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_StaticContents)
        original_policy = self._text_edit.focusPolicy()

        self.set_focus_policy("none")
        self._text_edit.setFocusPolicy(original_policy)

        # Ensure that the text edit keeps focus when widget is displayed.
        self.setFocusProxy(self._text_edit)

        self.set_frame_shadow("plain")
        self.set_frame_shape("styled_panel")

        self.itemActivated.connect(self._complete_current)

    def eventFilter(self, obj, event):
        """Handle mouse input and to auto-hide when losing focus."""
        if obj is self:
            if event.type() == QtCore.QEvent.Type.MouseButtonPress:
                pos = self.mapToGlobal(event.pos())
                target = QtWidgets.QApplication.widgetAt(pos)
                if target and self.isAncestorOf(target) or target is self:
                    return False
                else:
                    self.cancel_completion()

        return super().eventFilter(obj, event)

    def keyPressEvent(self, event):
        key = event.key()
        if key in (
            QtCore.Qt.Key.Key_Return,
            QtCore.Qt.Key.Key_Enter,
            QtCore.Qt.Key.Key_Tab,
        ):
            self._complete_current()
        elif key == QtCore.Qt.Key.Key_Escape:
            self.hide()
        elif key in (
            QtCore.Qt.Key.Key_Up,
            QtCore.Qt.Key.Key_Down,
            QtCore.Qt.Key.Key_PageUp,
            QtCore.Qt.Key.Key_PageDown,
            QtCore.Qt.Key.Key_Home,
            QtCore.Qt.Key.Key_End,
        ):
            return super().keyPressEvent(event)
        else:
            QtWidgets.QApplication.sendEvent(self._text_edit, event)

    # 'QWidget' interface

    def hideEvent(self, event):
        """Disconnect signal handlers and event filter."""
        super().hideEvent(event)
        try:
            self._text_edit.cursorPositionChanged.disconnect(self._update_current)
        except TypeError:
            pass
        self.removeEventFilter(self)

    def showEvent(self, event):
        """Connect signal handlers and event filter."""
        super().showEvent(event)
        self._text_edit.cursorPositionChanged.connect(self._update_current)
        self.installEventFilter(self)

    # 'CompletionWidget' interface

    def show_items(self, cursor, items: list[str], prefix_length: int = 0):
        """Show the widget with 'items' at the position specified by 'cursor'."""
        point = self._get_top_left_position(cursor)
        self.clear()
        path_items = []
        for item in items:
            # Check if the item could refer to a file or dir. The replacing
            # of '"' is needed for items on Windows
            path = os.path.abspath(item.replace('"', ""))
            if os.path.isfile(path) or os.path.isdir(path):
                path_items.append(item.replace('"', ""))
            else:
                list_item = widgets.ListWidgetItem()
                list_item.setData(QtCore.Qt.ItemDataRole.UserRole, item)  # type: ignore
                # Need to split to only show last element of a dot completion
                list_item.setText(item.split(".")[-1])
                self.addItem(list_item)

        common_prefix = os.path.dirname(os.path.commonprefix(path_items))
        for path_item in path_items:
            list_item = widgets.ListWidgetItem()
            list_item.setData(QtCore.Qt.ItemDataRole.UserRole, path_item)  # type: ignore
            text = path_item.split(common_prefix)[-1] if common_prefix else path_item
            list_item.setText(text)
            self.addItem(list_item)

        height = self.sizeHint().height()
        screen_rect = self.get_screen().availableGeometry()
        if screen_rect.size().height() + screen_rect.y() - point.y() - height < 0:
            point = self._text_edit.mapToGlobal(self._text_edit.cursorRect().topRight())
            point.setY(int(point.y() - height))
        scrollbar_width = self.verticalScrollBar().sizeHint().width()
        w = self.sizeHintForColumn(0) + scrollbar_width + 2 * self.frameWidth()
        self.setGeometry(point.x(), point.y(), w, height)

        # Move cursor to start of the prefix to replace it
        # when a item is selected
        cursor.movePosition(QtGui.QTextCursor.MoveOperation.Left, n=prefix_length)
        self._start_position = cursor.position()
        self.setCurrentRow(0)
        self.raise_()
        self.show()

    # Protected interface

    def _get_top_left_position(self, cursor: QtGui.QTextCursor) -> QtCore.QPoint:
        """Get top left position for this widget."""
        point = self._text_edit.cursorRect(cursor).center()
        point_size = self._text_edit.font().pointSize()
        factor = 1.05 if os.name == "nt" else 0.98
        delta = int((point_size * 1.20) ** factor)
        y = delta - (point_size // 2)
        point.setY(int(point.y() + y))
        point = self._text_edit.mapToGlobal(point)
        return point

    def _complete_current(self):
        """Perform the completion with the currently selected item."""
        text = self.currentItem().data(QtCore.Qt.ItemDataRole.UserRole)  # type: ignore
        self._current_text_cursor().insertText(text)
        self.hide()

    def _current_text_cursor(self) -> gui.TextCursor:
        """Return a cursor with text between the start  and currentposition selected."""
        cursor = self._text_edit.get_text_cursor()
        if cursor.position() >= self._start_position:
            cursor.setPosition(self._start_position, gui.TextCursor.MoveMode.KeepAnchor)
        return cursor

    def _update_current(self):
        """Update the current item based on the current text and the widget position."""
        # Update widget position
        cursor = self._text_edit.get_text_cursor()
        point = self._get_top_left_position(cursor)
        self.move(point)

        # Update current item
        prefix = self._current_text_cursor().selection().toPlainText()
        if prefix:
            flags = (
                QtCore.Qt.MatchFlag.MatchStartsWith  # type: ignore
                | QtCore.Qt.MatchFlag.MatchCaseSensitive
            )
            items = self.findItems(prefix, flags)
            if items:
                self.setCurrentItem(items[0])
            else:
                self.hide()
        else:
            self.hide()

    def cancel_completion(self):
        self.hide()


if __name__ == "__main__":
    app = widgets.app()
    textedit = widgets.TextEdit()
    completion_widget = CompletionWidget(textedit)
    textedit.show()
    completion_widget.show_items(textedit.get_text_cursor(), ["a", "b"])
    app.main_loop()
