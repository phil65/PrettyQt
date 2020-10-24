# -*- coding: utf-8 -*-
"""Credits to PyQode Authors."""

from typing import Optional

from qtpy import QtWidgets

from prettyqt import core, gui, widgets


class PromptLineEdit(widgets.LineEdit):
    """Extends QLineEdit to show a prompt text and a clear icon."""

    #: Signal emitted when the embedded button is clicked
    clear_clicked = core.Signal()

    def __init__(
        self, parent: Optional[QtWidgets.QWidget] = None, prompt_text: str = "Search"
    ):
        super().__init__(parent=parent)
        self._margin = self.sizeHint().height() - 2
        self._spacing = 0
        self._prompt_text = prompt_text
        self.button = widgets.ToolButton(self)
        self.button.set_style_icon("lineedit_clear")
        with self.button.edit_stylesheet() as ss:
            ss.QToolButton.setValues(border=None, padding="0px")
        self.button.set_cursor("arrow")
        self.button.set_focus_policy("none")
        self.set_button_visible(False)
        self.textChanged.connect(self._on_text_changed)
        self.button.clicked.connect(self.clear)
        self.button.clicked.connect(self.clear_clicked.emit)

    @property
    def prompt_text(self) -> str:
        """Gets/Sets the prompt text."""
        return self._prompt_text

    @prompt_text.setter
    def prompt_text(self, prompt: str):
        self._prompt_text = prompt
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)

        if not (self._prompt_text and not self.text() and self.isEnabled()):
            return None
        option = widgets.StyleOptionFrame()
        self.initStyleOption(option)

        left, top, right, bottom = self.getTextMargins()

        va = self.style().visualAlignment(self.layoutDirection(), self.alignment())
        rect = (
            self.style()
            .subElementRect(widgets.Style.SE_LineEditContents, option, self)
            .adjusted(2, 0, 0, 0)
            .adjusted(left, top, -right, -bottom)
        )
        fm = self.get_font_metrics()
        text = fm.elided_text(self._prompt_text, mode="right", width=rect.width())
        with gui.Painter(self) as painter:
            color = self.get_palette().get_color("text", "disabled")
            painter.setPen(color)
            painter.drawText(rect, va, text)

    def resizeEvent(self, event):
        # Adjusts Clear button position
        super().resizeEvent(event)
        self.button.resize(self._margin, self.height() - 2)
        self.button.move(self.width() - self._margin - 3, 1)

    def set_button_visible(self, visible: bool):
        """Sets the clear button as ``visible``.

        Args:
            visible (bool): Visibility of button
        """
        self.button.setVisible(visible)
        left, top, right, bottom = self.getTextMargins()
        if visible:
            right = self._margin + self._spacing
        else:
            right = 0
        self.setTextMargins(left, top, right, bottom)

    def _on_text_changed(self, text: str):
        """Text changed, update Clear button visibility."""
        self.set_button_visible(len(text) > 0)


if __name__ == "__main__":
    app = widgets.app()
    widget = PromptLineEdit()
    widget.show()
    app.main_loop()
