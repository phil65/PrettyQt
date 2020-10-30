# -*- coding: utf-8 -*-

from qtpy import QtGui

from prettyqt.utils import bidict

SURFACE_CLASS = bidict(window=QtGui.QSurface.Window, offscreen=QtGui.QSurface.Offscreen)

SURFACE_TYPES = bidict(
    raster=QtGui.QSurface.RasterSurface,
    open_gl=QtGui.QSurface.OpenGLSurface,
    raster_gl=QtGui.QSurface.RasterGLSurface,
    open_vg=QtGui.QSurface.OpenVGSurface,
    vulkan=QtGui.QSurface.VulkanSurface,
    metal=QtGui.QSurface.MetalSurface,
)


class Surface(QtGui.QSurface):
    def __repr__(self):
        return f"{self.__class__.__name__}()"

    def get_surface_class(self) -> str:
        """Get the current surface class.

        Possible values: "window", "offscreen"

        Returns:
            surface class
        """
        return SURFACE_CLASS.inv[self.surfaceClass()]

    def get_surface_type(self) -> str:
        """Get the current surface type.

        Possible values: "raster", "open_gl", "raster_gl", "open_vg", "vulkan", "metal"

        Returns:
            surface type
        """
        return SURFACE_TYPES.inv[self.surfaceType()]


if __name__ == "__main__":
    surface = Surface()
