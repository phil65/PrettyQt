from qtpy import QtGui
from prettyqt.utils import bidict, InvalidParamError


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


class PaintDevice(QtGui.QPaintDevice):
    def get_metric(self, metric: str) -> int:
        """Return metric information.

        Possible values: "center", "on_value"
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
