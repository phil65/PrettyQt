from __future__ import annotations

import pathlib
from typing import Literal

from prettyqt import quick
from prettyqt.utils import bidict, datatypes


ResizeModeStr = Literal["view_to_root_object", "root_object_to_view"]

RESIZE_MODES: bidict[ResizeModeStr, quick.QQuickView.ResizeMode] = bidict(
    view_to_root_object=quick.QQuickView.ResizeMode.SizeViewToRootObject,
    root_object_to_view=quick.QQuickView.ResizeMode.SizeRootObjectToView,
)

StatusStr = Literal["null", "ready", "loading", "error"]

STATUS: bidict[StatusStr, quick.QQuickView.Status] = bidict(
    null=quick.QQuickView.Status.Null,
    ready=quick.QQuickView.Status.Ready,
    loading=quick.QQuickView.Status.Loading,
    error=quick.QQuickView.Status.Error,
)


class QuickView(quick.quickwindow.QuickWindowMixin, quick.QQuickView):
    def set_source(self, source: datatypes.UrlType | datatypes.PathType):
        self.setSource(datatypes.to_local_url(source))

    def get_source(self) -> pathlib.Path:
        return pathlib.Path(self.source().toLocalFile())

    def get_status(self) -> StatusStr:
        return STATUS.inverse[self.status()]
