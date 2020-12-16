from typing import Union

from qtpy import QtCore, QtQml

from prettyqt import core
from prettyqt.utils import bidict


COMPILATION_MODES = bidict(
    prefer_synchronous=QtQml.QQmlComponent.PreferSynchronous,
    asynchronous=QtQml.QQmlComponent.Asynchronous,
)

STATUS = bidict(
    null=QtQml.QQmlComponent.Null,
    ready=QtQml.QQmlComponent.Ready,
    loading=QtQml.QQmlComponent.Loading,
    error=QtQml.QQmlComponent.Error,
)

QtQml.QQmlComponent.__bases__ = (core.Object,)


class QmlComponent(QtQml.QQmlComponent):
    def get_status(self) -> str:
        return STATUS.inverse[self.status()]

    def get_url(self) -> core.Url:
        return core.Url(self.url())

    def load_url(self, url: Union[QtCore.QUrl, str], mode: str):
        if isinstance(url, str):
            url = core.Url.from_user_input(url)
        self.loadUrl(url, COMPILATION_MODES[mode])
