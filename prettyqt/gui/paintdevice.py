from typing import TYPE_CHECKING, Literal

from prettyqt.qt import QtGui
from prettyqt.utils import bidict


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


if TYPE_CHECKING:
    _PaintDeviceBase = QtGui.QPaintDevice
else:
    _PaintDeviceBase = object


class PaintDeviceMixin(_PaintDeviceBase):
    def get_metric(self, metric: MetricStr | QtGui.QPaintDevice.PaintDeviceMetric) -> int:
        """Return metric information.

        Args:
            metric: metric information to get

        Returns:
            metric information
        """
        return self.metric(METRICS.get_enum_value(metric))


class PaintDevice(PaintDeviceMixin, QtGui.QPaintDevice):
    """The base class of objects that can be painted on with QPainter."""


if __name__ == "__main__":
    device = PaintDevice()
