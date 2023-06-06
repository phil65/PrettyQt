from __future__ import annotations

from typing import Literal

from prettyqt import widgets
from prettyqt.qt import QtPrintSupport
from prettyqt.utils import InvalidParamError, bidict


VIEW_MODE = bidict(
    single_page=QtPrintSupport.QPrintPreviewWidget.ViewMode.SinglePageView,
    facing_pages=QtPrintSupport.QPrintPreviewWidget.ViewMode.FacingPagesView,
    all_pages=QtPrintSupport.QPrintPreviewWidget.ViewMode.AllPagesView,
)

ViewModeStr = Literal["single_page", "facing_pages", "all_pages"]

ZOOM_MODE = bidict(
    custom_zoom=QtPrintSupport.QPrintPreviewWidget.ZoomMode.CustomZoom,
    fit_to_width=QtPrintSupport.QPrintPreviewWidget.ZoomMode.FitToWidth,
    fit_in_view=QtPrintSupport.QPrintPreviewWidget.ZoomMode.FitInView,
)

ZoomModeStr = Literal[
    "custom_zoom",
    "fit_to_width",
    "fit_in_view",
]


class PrintPreviewWidget(widgets.WidgetMixin, QtPrintSupport.QPrintPreviewWidget):
    def get_view_mode(self) -> ViewModeStr:
        return VIEW_MODE.inverse[self.viewMode()]

    def set_view_mode(self, mode: ViewModeStr):
        """Set view mode.

        Args:
            mode: view mode

        Raises:
            InvalidParamError: view mode does not exist
        """
        if mode not in VIEW_MODE:
            raise InvalidParamError(mode, VIEW_MODE)
        self.setViewMode(VIEW_MODE[mode])

    def get_zoom_mode(self) -> ZoomModeStr:
        return ZOOM_MODE.inverse[self.zoomMode()]

    def set_zoom_mode(self, mode: ZoomModeStr):
        """Set zoom mode.

        Args:
            mode: zoom mode

        Raises:
            InvalidParamError: zoom mode does not exist
        """
        if mode not in ZOOM_MODE:
            raise InvalidParamError(mode, ZOOM_MODE)
        self.setZoomMode(ZOOM_MODE[mode])
