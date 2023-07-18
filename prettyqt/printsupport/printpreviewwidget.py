from __future__ import annotations

from typing import Literal

from prettyqt import widgets
from prettyqt.qt import QtPrintSupport
from prettyqt.utils import bidict


ViewModeStr = Literal["single_page", "facing_pages", "all_pages"]

VIEW_MODE: bidict[ViewModeStr, QtPrintSupport.QPrintPreviewWidget.ViewMode] = bidict(
    single_page=QtPrintSupport.QPrintPreviewWidget.ViewMode.SinglePageView,
    facing_pages=QtPrintSupport.QPrintPreviewWidget.ViewMode.FacingPagesView,
    all_pages=QtPrintSupport.QPrintPreviewWidget.ViewMode.AllPagesView,
)

ZoomModeStr = Literal[
    "custom_zoom",
    "fit_to_width",
    "fit_in_view",
]

ZOOM_MODE: bidict[ZoomModeStr, QtPrintSupport.QPrintPreviewWidget.ZoomMode] = bidict(
    custom_zoom=QtPrintSupport.QPrintPreviewWidget.ZoomMode.CustomZoom,
    fit_to_width=QtPrintSupport.QPrintPreviewWidget.ZoomMode.FitToWidth,
    fit_in_view=QtPrintSupport.QPrintPreviewWidget.ZoomMode.FitInView,
)


class PrintPreviewWidget(widgets.WidgetMixin, QtPrintSupport.QPrintPreviewWidget):
    """Widget for previewing page layouts for printer output."""

    def get_view_mode(self) -> ViewModeStr:
        return VIEW_MODE.inverse[self.viewMode()]

    def set_view_mode(
        self, mode: ViewModeStr | QtPrintSupport.QPrintPreviewWidget.ViewMode
    ):
        """Set view mode.

        Args:
            mode: view mode
        """
        self.setViewMode(VIEW_MODE.get_enum_value(mode))

    def get_zoom_mode(self) -> ZoomModeStr:
        return ZOOM_MODE.inverse[self.zoomMode()]

    def set_zoom_mode(
        self, mode: ZoomModeStr | QtPrintSupport.QPrintPreviewWidget.ZoomMode
    ):
        """Set zoom mode.

        Args:
            mode: zoom mode
        """
        self.setZoomMode(ZOOM_MODE.get_enum_value(mode))
