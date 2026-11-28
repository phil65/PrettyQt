from typing import TYPE_CHECKING, Literal

from prettyqt import core, widgets
from prettyqt.utils import bidict, datatypes


mod = widgets.QRhiWidget

ApiStr = Literal["null", "opengl", "metal", "vulkan", "direct3d11", "direct3d12"]

API: bidict[ApiStr, mod.Api] = bidict(
    null=mod.Api.Null,
    opengl=mod.Api.OpenGL,
    metal=mod.Api.Metal,
    vulkan=mod.Api.Vulkan,
    direct3d11=mod.Api.Direct3D11,
    direct3d12=mod.Api.Direct3D12,
)

TextureFormatStr = Literal["rgba8", "rgba16f", "rgba32f", "rgb10a2"]

TEXTURE_FORMAT: bidict[TextureFormatStr, mod.TextureFormat] = bidict(
    rgba8=mod.TextureFormat.RGBA8,
    rgba16f=mod.TextureFormat.RGBA16F,
    rgba32f=mod.TextureFormat.RGBA32F,
    rgb10a2=mod.TextureFormat.RGB10A2,
)


if TYPE_CHECKING:
    from prettyqt.qt import QtWidgets

    _RhiWidgetBase = QtWidgets.QRhiWidget
else:
    _RhiWidgetBase = object


class RhiWidgetMixin(widgets.WidgetMixin, _RhiWidgetBase):
    def _get_map(self):
        maps = super()._get_map()
        maps |= {"colorBufferFormat": TEXTURE_FORMAT}
        return maps

    def set_api(self, api: ApiStr | mod.Api):
        """Set the graphics API to use.

        Args:
            api: graphics API
        """
        self.setApi(API.get_enum_value(api))

    def get_api(self) -> ApiStr:
        """Return current graphics API.

        Returns:
            graphics API
        """
        return API.inverse[self.api()]

    def set_color_buffer_format(self, fmt: TextureFormatStr | mod.TextureFormat):
        """Set the texture format for the color buffer.

        Args:
            fmt: texture format
        """
        self.setColorBufferFormat(TEXTURE_FORMAT.get_enum_value(fmt))

    def get_color_buffer_format(self) -> TextureFormatStr:
        """Return current color buffer texture format.

        Returns:
            texture format
        """
        return TEXTURE_FORMAT.inverse[self.colorBufferFormat()]

    def set_fixed_color_buffer_size(self, size: datatypes.SizeType):
        """Set fixed color buffer size."""
        self.setFixedColorBufferSize(datatypes.to_size(size))

    def get_fixed_color_buffer_size(self) -> core.Size:
        """Return fixed color buffer size."""
        return core.Size(self.fixedColorBufferSize())


class RhiWidget(RhiWidgetMixin, widgets.QRhiWidget):
    """Widget for rendering 3D graphics via the Qt Rendering Hardware Interface."""
