from typing import Literal

from qtpy import QtGui

from prettyqt.utils import bidict


SURFACE_CLASS = bidict(window=QtGui.QSurface.Window, offscreen=QtGui.QSurface.Offscreen)

SurfaceClassStr = Literal["window", "offscreen"]

SURFACE_TYPES = bidict(
    raster=QtGui.QSurface.RasterSurface,
    open_gl=QtGui.QSurface.OpenGLSurface,
    raster_gl=QtGui.QSurface.RasterGLSurface,
    open_vg=QtGui.QSurface.OpenVGSurface,
    vulkan=QtGui.QSurface.VulkanSurface,
    metal=QtGui.QSurface.MetalSurface,
)

SurfaceTypeStr = Literal["raster", "open_gl", "raster_gl", "open_vg", "vulkan", "metal"]


class Surface(QtGui.QSurface):
    def __repr__(self):
        return f"{self.__class__.__name__}()"

    def get_surface_class(self) -> SurfaceClassStr:
        """Get the current surface class.

        Returns:
            surface class
        """
        return SURFACE_CLASS.inverse[self.surfaceClass()]

    def get_surface_type(self) -> SurfaceTypeStr:
        """Get the current surface type.

        Returns:
            surface type
        """
        return SURFACE_TYPES.inverse[self.surfaceType()]


if __name__ == "__main__":
    surface = Surface()
