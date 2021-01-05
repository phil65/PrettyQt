from __future__ import annotations

import os
import pathlib
from typing import Literal, Union

from prettyqt import core, gui
from prettyqt.qt import QtCore, QtQuick
from prettyqt.utils import bidict


RESIZE_MODES = bidict(
    view_to_root_object=QtQuick.QQuickView.SizeViewToRootObject,
    root_object_to_view=QtQuick.QQuickView.SizeRootObjectToView,
)

ResizeModeStr = Literal["view_to_root_object", "root_object_to_view"]

STATUS = bidict(
    null=QtQuick.QQuickView.Null,
    ready=QtQuick.QQuickView.Ready,
    loading=QtQuick.QQuickView.Loading,
    error=QtQuick.QQuickView.Error,
)

StatusStr = Literal["null", "ready", "loading", "error"]

QtQuick.QQuickView.__bases__ = (gui.Window,)


class QuickView(QtQuick.QQuickView):
    def set_source(self, source: Union[str, os.PathLike, QtCore.QUrl]):
        if isinstance(source, os.PathLike):  # type: ignore
            source = os.fspath(source)
        if isinstance(source, str):
            source = core.Url.fromLocalFile(source)
        self.setSource(source)

    def get_source(self) -> pathlib.Path:
        return pathlib.Path(self.source().toLocalFile())

    def get_status(self) -> StatusStr:
        return STATUS.inverse[self.status()]
