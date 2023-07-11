from __future__ import annotations

import contextlib

from prettyqt.qt import QtWidgets


class WhatsThis(QtWidgets.QWhatsThis):
    """Simple description of any widget, i.e. answering the question "What's This?"."""

    @classmethod
    @contextlib.contextmanager
    def enter_mode(cls):
        cls.enterWhatsThisMode()
        yield cls
        cls.leaveWhatsThisMode()


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()

    def test():
        with WhatsThis.enter_mode() as w:
            print(w.inWhatsThisMode())

    btn = widgets.PushButton(callback=test)
    btn.show()
    app.exec()
