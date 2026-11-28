import logging
import sys
import traceback
from typing import TYPE_CHECKING

from prettyqt import debugging, gui, widgets
from prettyqt.utils import helpers


if TYPE_CHECKING:
    from collections.abc import Callable


logger = logging.getLogger(__name__)


class ErrorMessageBox(widgets.MessageBox):
    """An message box widget for displaying Python exception."""

    def __init__(self, title: str, text_or_exception: str | Exception, parent=None):
        if isinstance(text_or_exception, str):
            text = text_or_exception
            exc = None
        else:
            text = str(text_or_exception)
            exc = text_or_exception
        super().__init__(
            # icon=MBox.Icon.Critical,
            window_title=title,
            text=str(text)[:1000],
            buttons=["ok", "help", "close"],
            parent=parent,
        )

        self._exc = exc

        traceback_button = self.get_button("help")
        traceback_button.setText("Show traceback")
        close_button = self.get_button("close")
        close_button.setText("Quit application")

    def exec(self):
        match super().exec():
            case widgets.MessageBox.StandardButton.Help:
                tb = self._get_traceback()
                dlg = debugging.TracebackDialog(self)
                dlg.setText(tb)
                dlg.exec()
                return None
            case widgets.MessageBox.StandardButton.Close:
                sys.exit(1)
            case widgets.MessageBox.StandardButton.Ok:
                return True

    # @classmethod
    # def setup_example(cls):
    #     return cls("Title", "Test message")

    @classmethod
    def from_exc(cls, e: Exception, parent=None):
        """Construct message box from a exception."""
        return cls(type(e).__name__, e, parent)

    @classmethod
    def raise_(cls, e: Exception, parent=None):
        """Raise exception in the message box."""
        # unwrap EmitLoopError
        return cls.from_exc(e, parent=parent).exec()

    def _get_traceback(self):
        if self._exc is None:
            return traceback.format_exc()
        formatter = get_tb_formatter(gui.Font.mono().family())
        return formatter(self._exc, as_html=True)

    @classmethod
    def _excepthook(cls, exc_type: type[Exception], exc_value: Exception, exc_traceback):
        """Exception hook used during application execution."""
        strings = traceback.format_exception(exc_type, exc_value, exc_traceback)
        tb = "".join(strings)
        logger.error(tb)
        return ErrorMessageBox.raise_(exc_value, parent=None)


# Following functions are mostly copied from napari (BSD 3-Clause).
# See https://github.com/napari/napari/blob/main/napari/utils/notifications.py


def get_tb_formatter(font: str = "Monospace") -> Callable[..., str]:
    """Return a formatter callable that uses IPython VerboseTB if available.

    Imports IPython lazily if available to take advantage of ultratb.VerboseTB,
    otherwise falls back to the traceback module (which also renders chained
    exceptions).

    Returns:
        callable: A function that accepts ``(exception, as_html, color)`` and returns
                a formatted traceback string. ``as_html`` determines whether the
                traceback is formatted in html or plain text.
    """
    style = f"font-family: monaco,{font},monospace;"
    try:
        import IPython.core.ultratb

        def format_exc_info(exc: Exception, as_html: bool, color="Neutral") -> str:
            try:  # IPython >= 9
                vbtb = IPython.core.ultratb.VerboseTB(theme_name=color.lower())
            except TypeError:
                vbtb = IPython.core.ultratb.VerboseTB(color_scheme=color)
            tb = vbtb.text(exc.__class__, exc, exc.__traceback__)
            if as_html:
                ansi_string = (
                    tb.replace(" ", "&nbsp;").replace("<", "&lt;").replace(">", "&gt;")
                )
                html = helpers.ansi2html(ansi_string)
                html = html.replace("\n", "<br>")
                tb = f"<span style='{style}'>{html}</span>"
            return tb

    except ModuleNotFoundError:
        import html
        import traceback

        def format_exc_info(exc: Exception, as_html: bool, color=None) -> str:
            tb_text = "".join(traceback.format_exception(exc))
            if not as_html:
                return tb_text
            body = html.escape(tb_text).replace(" ", "&nbsp;").replace("\n", "<br>")
            return f"<span style='{style}'>{body}</span>"

    return format_exc_info


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    w = widgets.Widget()
    wnd = ErrorMessageBox("a", "b", w)
    wnd.show()
    with app.debug_mode():
        app.exec()
