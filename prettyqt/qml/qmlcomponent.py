from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtQml
from prettyqt.utils import bidict, datatypes


COMPILATION_MODES = bidict(
    prefer_synchronous=QtQml.QQmlComponent.CompilationMode.PreferSynchronous,
    asynchronous=QtQml.QQmlComponent.CompilationMode.Asynchronous,
)

STATUS = bidict(
    null=QtQml.QQmlComponent.Status.Null,
    ready=QtQml.QQmlComponent.Status.Ready,
    loading=QtQml.QQmlComponent.Status.Loading,
    error=QtQml.QQmlComponent.Status.Error,
)


class QmlComponent(core.ObjectMixin, QtQml.QQmlComponent):
    """Encapsulates a QML component definition."""

    def get_status(self) -> str:
        return STATUS.inverse[self.status()]

    def get_url(self) -> core.Url:
        return core.Url(self.url())

    def load_url(self, url: datatypes.UrlType, mode: str):
        if isinstance(url, str):
            url = core.Url.from_user_input(url)
        self.loadUrl(url, COMPILATION_MODES[mode])
