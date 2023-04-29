from __future__ import annotations

import os
import pathlib
from typing import Literal

from prettyqt import core, widgets
from prettyqt.qt import QtQuickWidgets
from prettyqt.utils import bidict, datatypes


RESIZE_MODES = bidict(
    view_to_root_object=QtQuickWidgets.QQuickWidget.ResizeMode.SizeViewToRootObject,
    root_object_to_view=QtQuickWidgets.QQuickWidget.ResizeMode.SizeRootObjectToView,
)

ResizeModeStr = Literal["view_to_root_object", "root_object_to_view"]

STATUS = bidict(
    null=QtQuickWidgets.QQuickWidget.Status.Null,
    ready=QtQuickWidgets.QQuickWidget.Status.Ready,
    loading=QtQuickWidgets.QQuickWidget.Status.Loading,
    error=QtQuickWidgets.QQuickWidget.Status.Error,
)

StatusStr = Literal["null", "ready", "loading", "error"]


class QuickWidget(widgets.WidgetMixin, QtQuickWidgets.QQuickWidget):
    def set_source(self, source: datatypes.UrlType | datatypes.PathType):
        if isinstance(source, os.PathLike):
            source = os.fspath(source)
        if isinstance(source, str):
            source = core.Url.fromLocalFile(source)
        self.setSource(source)

    def get_source(self) -> pathlib.Path:
        return pathlib.Path(self.source().toLocalFile())

    def get_status(self) -> StatusStr:
        return STATUS.inverse[self.status()]


if __name__ == "__main__":
    app = widgets.app()
    widget = QuickWidget()
