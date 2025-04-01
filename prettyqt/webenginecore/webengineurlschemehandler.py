from __future__ import annotations

from typing import TYPE_CHECKING, Any

from prettyqt import core
from prettyqt.qt import QtWebEngineCore


if TYPE_CHECKING:
    from collections.abc import Callable


class WebEngineUrlSchemeHandler(
    core.ObjectMixin, QtWebEngineCore.QWebEngineUrlSchemeHandler
):
    pass


class CallbackWebEngineUrlSchemeHandler(WebEngineUrlSchemeHandler):
    def __init__(
        self,
        callback: Callable[[QtWebEngineCore.QWebEngineUrlRequestJob], Any],
        *args: Any,
        **kwargs: Any,
    ):
        super().__init__(*args, **kwargs)
        self.callback = callback

    def requestStarted(self, request: QtWebEngineCore.QWebEngineUrlRequestJob):
        self.callback(request)


if __name__ == "__main__":
    item = WebEngineUrlSchemeHandler()
