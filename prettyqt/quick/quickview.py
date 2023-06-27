from __future__ import annotations

import pathlib
from typing import Literal

from prettyqt import quick
from prettyqt.qt import QtQuick
from prettyqt.utils import bidict, datatypes


ResizeModeStr = Literal["view_to_root_object", "root_object_to_view"]

RESIZE_MODES: bidict[ResizeModeStr, QtQuick.QQuickView.ResizeMode] = bidict(
    view_to_root_object=QtQuick.QQuickView.ResizeMode.SizeViewToRootObject,
    root_object_to_view=QtQuick.QQuickView.ResizeMode.SizeRootObjectToView,
)

StatusStr = Literal["null", "ready", "loading", "error"]

STATUS: bidict[StatusStr, QtQuick.QQuickView.Status] = bidict(
    null=QtQuick.QQuickView.Status.Null,
    ready=QtQuick.QQuickView.Status.Ready,
    loading=QtQuick.QQuickView.Status.Loading,
    error=QtQuick.QQuickView.Status.Error,
)


class QuickView(quick.quickwindow.QuickWindowMixin, QtQuick.QQuickView):
    def set_source(self, source: datatypes.UrlType | datatypes.PathType):
        self.setSource(datatypes.to_local_url(source))

    def get_source(self) -> pathlib.Path:
        return pathlib.Path(self.source().toLocalFile())

    def get_status(self) -> StatusStr:
        return STATUS.inverse[self.status()]
