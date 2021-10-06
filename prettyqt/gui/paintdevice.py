from __future__ import annotations

from typing import Literal

from prettyqt.qt import QtGui
from prettyqt.utils import InvalidParamError, bidict


METRICS = bidict(
    width=QtGui.QPaintDevice.PaintDeviceMetric.PdmWidth,
    height=QtGui.QPaintDevice.PaintDeviceMetric.PdmHeight,
    width_mm=QtGui.QPaintDevice.PaintDeviceMetric.PdmWidthMM,
    height_mm=QtGui.QPaintDevice.PaintDeviceMetric.PdmHeightMM,
    num_colors=QtGui.QPaintDevice.PaintDeviceMetric.PdmNumColors,
    depth=QtGui.QPaintDevice.PaintDeviceMetric.PdmDepth,
    dpi_x=QtGui.QPaintDevice.PaintDeviceMetric.PdmDpiX,
    dpi_y=QtGui.QPaintDevice.PaintDeviceMetric.PdmDpiY,
    physical_dpi_x=QtGui.QPaintDevice.PaintDeviceMetric.PdmPhysicalDpiX,
    physical_dpi_y=QtGui.QPaintDevice.PaintDeviceMetric.PdmPhysicalDpiY,
    pixel_ratio=QtGui.QPaintDevice.PaintDeviceMetric.PdmDevicePixelRatio,
    pixel_ratio_scaled=QtGui.QPaintDevice.PaintDeviceMetric.PdmDevicePixelRatioScaled,
)

MetricStr = Literal[
    "width",
    "height",
    "width_mm",
    "height_mm",
    "num_colors",
    "depth",
    "dpi_x",
    "dpi_y",
    "physical_dpi_x",
    "physical_dpi_y",
    "pixel_ratio",
    "pixel_ratio_scaled",
]


class PaintDevice(QtGui.QPaintDevice):
    def get_metric(self, metric: MetricStr) -> int:
        """Return metric information.

        Args:
            metric: metric information to get

        Returns:
            metric information
        """
        if metric not in METRICS:
            raise InvalidParamError(metric, METRICS)
        return self.metric(METRICS[metric])


if __name__ == "__main__":
    device = PaintDevice()
