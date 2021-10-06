from __future__ import annotations

from typing import Literal

from prettyqt.qt import QtGui
from prettyqt.utils import bidict


SURFACE_CLASS = bidict(
    window=QtGui.QSurface.SurfaceClass.Window,
    offscreen=QtGui.QSurface.SurfaceClass.Offscreen,
)

SurfaceClassStr = Literal["window", "offscreen"]

SURFACE_TYPES = bidict(
    raster=QtGui.QSurface.SurfaceType.RasterSurface,
    open_gl=QtGui.QSurface.SurfaceType.OpenGLSurface,
    raster_gl=QtGui.QSurface.SurfaceType.RasterGLSurface,
    open_vg=QtGui.QSurface.SurfaceType.OpenVGSurface,
    vulkan=QtGui.QSurface.SurfaceType.VulkanSurface,
    metal=QtGui.QSurface.SurfaceType.MetalSurface,
)

SurfaceTypeStr = Literal["raster", "open_gl", "raster_gl", "open_vg", "vulkan", "metal"]


class Surface(QtGui.QSurface):
    def __repr__(self):
        return f"{type(self).__name__}()"

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
