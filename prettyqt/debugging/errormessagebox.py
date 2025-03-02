from __future__ import annotations

import logging
import re
import sys
import traceback
from typing import TYPE_CHECKING

from prettyqt import debugging, gui, widgets
from prettyqt.utils import helpers


if TYPE_CHECKING:
    from collections.abc import Callable, Generator


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
        traceback_button.setText("Show trackback")
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


def get_tb_formatter(font: str = "Monospace") -> Callable[[Exception, bool, str], str]:
    """Return a formatter callable that uses IPython VerboseTB if available.

    Imports IPython lazily if available to take advantage of ultratb.VerboseTB.
    If unavailable, cgitb is used instead, but this function overrides a lot of
    the hardcoded citgb styles and adds error chaining (for exceptions that
    result from other exceptions).

    Returns:
        callable: A function that accepts a 3-tuple and a boolean ``(exc_info, as_html)``
                and returns a formatted traceback string. The ``exc_info`` tuple is of
                the ``(type, value, traceback)`` format returned by sys.exc_info().
                The ``as_html`` determines whether the traceback is formatted in html
                or plain text.
    """
    try:
        import IPython.core.ultratb

        def format_exc_info(exc: Exception, as_html: bool, color="Neutral") -> str:
            # avoids printing the array data
            # some discussion related to obtaining the current string function
            # can be found here, https://github.com/numpy/numpy/issues/11266
            import numpy as np

            np.set_string_function(lambda arr: f"{type(arr)} {arr.shape} {arr.dtype}")

            vbtb = IPython.core.ultratb.VerboseTB(color_scheme=color)
            tb = vbtb.text(exc.__class__, exc, exc.__traceback__)
            if as_html:
                ansi_string = (
                    tb.replace(" ", "&nbsp;").replace("<", "&lt;").replace(">", "&gt;")
                )
                html = helpers.ansi2html(ansi_string)
                html = html.replace("\n", "<br>")
                style = f"font-family: monaco,{font},monospace;"
                tb = f"<span style='{style}'>{html}</span>"

            # resets to default behavior
            np.set_string_function(None)
            return tb

    except ModuleNotFoundError:
        import cgitb
        import traceback

        # cgitb does not support error chaining...
        # see https://peps.python.org/pep-3134/#enhanced-reporting
        # this is a workaround
        def cgitb_chain(exc: Exception) -> Generator[str, None, None]:
            """Recurse through exception stack and chain cgitb_html calls."""
            if exc.__cause__:
                yield from cgitb_chain(exc.__cause__)
                yield (
                    '<br><br><font color="#51B432">The above exception was '
                    "the direct cause of the following exception:</font><br>"
                )
            elif exc.__context__:
                yield from cgitb_chain(exc.__context__)
                yield (
                    '<br><br><font color="#51B432">During handling of the '
                    "above exception, another exception occurred:</font><br>"
                )
            yield cgitb_html(exc)

        def cgitb_html(exc: Exception) -> str:
            """Format exception with cgitb.html."""
            info = (type(exc), exc, exc.__traceback__)
            return cgitb.html(info)

        def format_exc_info(exc: Exception, as_html: bool, color=None) -> str:
            info = (
                exc.__class__,
                exc,
                exc.__traceback__,
            )
            # avoids printing the array data
            try:
                import numpy as np

                np.set_string_function(lambda arr: f"{type(arr)} {arr.shape} {arr.dtype}")
                np_imported = True
            except ImportError:
                np_imported = False
            if as_html:
                html = "\n".join(cgitb_chain(exc))
                # cgitb has a lot of hardcoded colors that don't work for us
                # remove bgcolor, and let theme handle it
                html = re.sub('bgcolor="#.*"', "", html)
                # remove superfluous whitespace
                html = html.replace("<br>\n", "\n")
                # but retain it around the <small> bits
                html = re.sub(r"(<tr><td><small.*</tr>)", "<br>\\1<br>", html)
                # weird 2-part syntax is a workaround for hard-to-grep text.
                html = html.replace(
                    "<p>A problem occurred in a Python script. Here is the sequence of",
                    "",
                )
                html = html.replace(
                    "function calls leading up to the error, "
                    "in the order they occurred.</p>",
                    "<br>",
                )
                # remove hardcoded fonts
                html = html.replace("\n", "<br>")
                style = f"font-family: monaco,{font},monospace;"
                tb_text = f"<span style='{style}'>{html}</span>"
            else:
                # if we don't need HTML, just use traceback
                strings = traceback.format_exception(*info)
                tb_text = "".join(strings)
            # resets to default behavior
            if np_imported:
                np.set_string_function(None)
            return tb_text

    return format_exc_info


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    w = widgets.Widget()
    wnd = ErrorMessageBox("a", "b", w)
    wnd.show()
    with app.debug_mode():
        app.exec()
