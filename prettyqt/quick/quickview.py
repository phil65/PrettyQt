import pathlib
from typing import Union

from qtpy import QtCore, QtQuick

from prettyqt import core, gui
from prettyqt.utils import bidict


RESIZE_MODES = bidict(
    view_to_root_object=QtQuick.QQuickView.SizeViewToRootObject,
    root_object_to_view=QtQuick.QQuickView.SizeRootObjectToView,
)

STATUS = bidict(
    null=QtQuick.QQuickView.Null,
    ready=QtQuick.QQuickView.Ready,
    loading=QtQuick.QQuickView.Loading,
    error=QtQuick.QQuickView.Error,
)


QtQuick.QQuickView.__bases__ = (gui.Window,)


class QuickView(QtQuick.QQuickView):
    def set_source(self, source: Union[str, pathlib.Path, QtCore.QUrl]):
        if isinstance(source, pathlib.Path):
            source = str(source)
        if isinstance(source, str):
            source = core.Url.fromLocalFile(source)
        self.setSource(source)

    def get_source(self) -> pathlib.Path:
        return pathlib.Path(self.source().toLocalFile())

    def get_status(self) -> str:
        return STATUS.inverse[self.status()]
