from typing import Literal

from prettyqt import core
from prettyqt.qt import QtQml
from prettyqt.utils import bidict, datatypes


CompilationModeStr = Literal["prefer_synchronous", "asynchronous"]

COMPILATION_MODES: bidict[CompilationModeStr, QtQml.QQmlComponent.CompilationMode] = (
    bidict(
        prefer_synchronous=QtQml.QQmlComponent.CompilationMode.PreferSynchronous,
        asynchronous=QtQml.QQmlComponent.CompilationMode.Asynchronous,
    )
)

StatusStr = Literal["null", "ready", "loading", "error"]

STATUS: bidict[StatusStr, QtQml.QQmlComponent.Status] = bidict(
    null=QtQml.QQmlComponent.Status.Null,
    ready=QtQml.QQmlComponent.Status.Ready,
    loading=QtQml.QQmlComponent.Status.Loading,
    error=QtQml.QQmlComponent.Status.Error,
)


class QmlComponent(core.ObjectMixin, QtQml.QQmlComponent):
    """Encapsulates a QML component definition."""

    def get_status(self) -> StatusStr:
        return STATUS.inverse[self.status()]

    def get_url(self) -> core.Url:
        return core.Url(self.url())

    def load_url(
        self,
        url: datatypes.UrlType,
        mode: CompilationModeStr
        | QtQml.QQmlComponent.CompilationMode = "prefer_synchronous",
    ):
        qurl = (
            core.Url.from_user_input(url)
            if isinstance(url, str)
            else datatypes.to_url(url)
        )
        self.loadUrl(qurl, COMPILATION_MODES.get_enum_value(mode))
