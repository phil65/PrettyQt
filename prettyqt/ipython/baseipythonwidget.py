from __future__ import annotations

import logging
import os

from qtconsole.rich_jupyter_widget import RichJupyterWidget

from prettyqt import core, gui, widgets


# disables 'Please pass -Xfrozen_modules=off' warning
os.environ["PYDEVD_DISABLE_FILE_VALIDATION"] = "1"

logger = logging.getLogger(__name__)


class BaseIPythonWidget(RichJupyterWidget, widgets.WidgetMixin):
    """Convenience class for a live IPython console widget running out-of-process."""

    code_executed = core.Signal(str)

    def __init__(self, *args, **kwargs):
        super().__init__(
            gui_completion="droplist",  # 'plain', 'droplist', 'ncurses'
            kind="rich",  # 'plain', 'rich', only applies when no custom control set.
            paging="vsplit",  # h  'inside', 'hsplit', 'vsplit', 'custom', 'none'
            # custom_control=widgets.TextEdit,
            # custom_page_control=widgets.TextEdit,
        )
        self.banner = "IPython Console"
        self.font_size = 6
        # self.gui_completion = "droplist"
        widgets.Application.call_on_exit(self.shutdown)
        # self.exit_requested.connect(self.shutdown)

        widgets.Application.styleHints().colorSchemeChanged.connect(
            self.adjust_style_to_palette
        )
        self.adjust_style_to_palette()

    def adjust_style_to_palette(self):
        """Adjust coloring of the terminal to current palette."""
        pal = widgets.Application.get_palette()
        style = "linux" if pal.is_dark() else "lightbg"
        self.set_default_style(style)

    def shutdown(self):
        """Stop IPython and cleanup."""
        return NotImplemented

    def buffer(self) -> str:
        """Get current code block."""
        return self.input_buffer

    def set_buffer(self, code: str) -> None:
        """Set code string to Jupyter QtConsole buffer."""
        self.input_buffer = ""
        if not isinstance(code, str):
            raise ValueError(f"Cannot set {type(code)}.")
        cursor = self._control.textCursor()
        lines = code.split("\n")
        for line in lines[:-1]:
            cursor.insertText(line + "\n")
            self._insert_continuation_prompt(cursor)  # insert "...:"
        cursor.insertText(lines[-1])
        return None

    def insert_text(self, text: str) -> None:
        cursor = self._control.textCursor()
        cursor.insertText(text)
        return None

    def set_temp_text(self, text: str) -> None:
        cursor = self._control.textCursor()
        cursor.removeSelectedText()
        pos = cursor.position()
        cursor.insertText(text)
        cursor.setPosition(pos)
        cursor.setPosition(pos + len(text), gui.TextCursor.MoveMode.KeepAnchor)
        self._control.setTextCursor(cursor)
        return None

    def get_selected_text(self) -> str:
        """Return the selected text."""
        cursor = self._control.textCursor()
        return cursor.selection().toPlainText()

    def clear(self):
        """Clear the terminal."""
        self._control.clear()

    def print_text(self, text: str, before_prompt: bool = False):
        """Print some plain text to the console."""
        self._append_plain_text(text)

    def execute(
        self,
        source: str | None = None,
        hidden: bool = False,
        interactive: bool = False,
    ):
        """Execute a command in the frame of the console widget."""
        if source is None:
            source = self.input_buffer
        super().execute(source=source, hidden=hidden, interactive=interactive)
        self.code_executed.emit(source)
        return None


if __name__ == "__main__":
    from prettyqt.custom_widgets import commandpalette

    app = widgets.app()
    cp = commandpalette.CommandPalette()
    app.set_style("fusion")
    console_widget = BaseIPythonWidget(app)
    console_widget.print_text("hallo")
    console_widget.show()
    console_widget.add_shortcut("Ctrl+P", cp.show)
    cp.populate_from_widget(console_widget)
    app.main_loop()
