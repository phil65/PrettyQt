from typing import Literal

from qtpy import QtGui

from prettyqt.utils import InvalidParamError, bidict


METRICS = bidict(
    width=QtGui.QPaintDevice.PdmWidth,
    height=QtGui.QPaintDevice.PdmHeight,
    width_mm=QtGui.QPaintDevice.PdmWidthMM,
    height_mm=QtGui.QPaintDevice.PdmHeightMM,
    num_colors=QtGui.QPaintDevice.PdmNumColors,
    depth=QtGui.QPaintDevice.PdmDepth,
    dpi_x=QtGui.QPaintDevice.PdmDpiX,
    dpi_y=QtGui.QPaintDevice.PdmDpiY,
    physical_dpi_x=QtGui.QPaintDevice.PdmPhysicalDpiX,
    physical_dpi_y=QtGui.QPaintDevice.PdmPhysicalDpiY,
    pixel_ratio=QtGui.QPaintDevice.PdmDevicePixelRatio,
    pixel_ratio_scaled=QtGui.QPaintDevice.PdmDevicePixelRatioScaled,
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
