from __future__ import annotations

import io
from typing import Literal

from typing_extensions import Self

from prettyqt import core, gui
from prettyqt.qt import API, QtGui
from prettyqt.utils import InvalidParamError, bidict, serializemixin


FORMAT = bidict(
    invalid=QtGui.QImage.Format.Format_Invalid,
    mono=QtGui.QImage.Format.Format_Mono,
    monolsb=QtGui.QImage.Format.Format_MonoLSB,
    indexed8=QtGui.QImage.Format.Format_Indexed8,
    rgb32=QtGui.QImage.Format.Format_RGB32,
    argb32=QtGui.QImage.Format.Format_ARGB32,
    argb32_premultiplied=QtGui.QImage.Format.Format_ARGB32_Premultiplied,
    rgb16=QtGui.QImage.Format.Format_RGB16,
    argb8565_premultiplied=QtGui.QImage.Format.Format_ARGB8565_Premultiplied,
    rgb666=QtGui.QImage.Format.Format_RGB666,
    argb6666_premultiplied=QtGui.QImage.Format.Format_ARGB6666_Premultiplied,
    rgb555=QtGui.QImage.Format.Format_RGB555,
    argb8555_premultiplied=QtGui.QImage.Format.Format_ARGB8555_Premultiplied,
    rgb888=QtGui.QImage.Format.Format_RGB888,
    rgb444=QtGui.QImage.Format.Format_RGB444,
    argb4444_premultiplied=QtGui.QImage.Format.Format_ARGB4444_Premultiplied,
    rgbx8888=QtGui.QImage.Format.Format_RGBX8888,
    rgba8888=QtGui.QImage.Format.Format_RGBA8888,
    rgba8888_premultiplied=QtGui.QImage.Format.Format_RGBA8888_Premultiplied,
    bgr30=QtGui.QImage.Format.Format_BGR30,
    a2bgr30_premultiplied=QtGui.QImage.Format.Format_A2BGR30_Premultiplied,
    rgb30=QtGui.QImage.Format.Format_RGB30,
    a2rgb30_premultiplied=QtGui.QImage.Format.Format_A2RGB30_Premultiplied,
    alpha8=QtGui.QImage.Format.Format_Alpha8,
    grayscale8=QtGui.QImage.Format.Format_Grayscale8,
    grayscale16=QtGui.QImage.Format.Format_Grayscale16,
    rgbx64=QtGui.QImage.Format.Format_RGBX64,
    rgba64=QtGui.QImage.Format.Format_RGBA64,
    rgba64_premultiplied=QtGui.QImage.Format.Format_RGBA64_Premultiplied,
    bgr888=QtGui.QImage.Format.Format_BGR888,
    rgbx16fpx4=QtGui.QImage.Format.Format_RGBX16FPx4,
    rgba16fpx4=QtGui.QImage.Format.Format_RGBA16FPx4,
    rgba16fpx4_premultiplied=QtGui.QImage.Format.Format_RGBA16FPx4_Premultiplied,
    rgbx32fpx4=QtGui.QImage.Format.Format_RGBX32FPx4,
    rgba32fpx4=QtGui.QImage.Format.Format_RGBA32FPx4,
    rgba32fpx4_premultiplied=QtGui.QImage.Format.Format_RGBA32FPx4_Premultiplied,
)

FormatStr = Literal[
    "invalid",
    "mono",
    "monolsb",
    "indexed8",
    "rgb32",
    "argb32",
    "argb32_premultiplied",
    "rgb16",
    "argb8565_premultiplied",
    "rgb666",
    "argb6666_premultiplied",
    "rgb555",
    "argb8555_premultiplied",
    "rgb888",
    "rgb444",
    "argb4444_premultiplied",
    "rgbx8888",
    "rgba8888",
    "rgba8888_premultiplied",
    "bgr30",
    "a2bgr30_premultiplied",
    "rgb30",
    "a2rgb30_premultiplied",
    "alpha8",
    "grayscale8",
    "grayscale16",
    "rgbx64",
    "rgba64",
    "rgba64_premultiplied",
    "bgr888",
    "rgbx16fpx4",
    "rgba16fpx4",
    "rgba16fpx4_premultiplied",
    "rgbx32fpx4",
    "rgba32fpx4",
    "rgba32fpx4_premultiplied",
]


class Image(serializemixin.SerializeMixin, gui.PaintDeviceMixin, QtGui.QImage):
    def __setitem__(self, index: tuple[int, int], value):
        self.setPixel(index[0], index[1], value)

    def __getitem__(self, index: tuple[int, int]) -> int:
        return self.pixel(index[0], index[1])

    @classmethod
    def from_ndarray(cls, arr) -> Self:
        import numpy as np

        height, width, bytes_per_component = arr.shape
        if arr.dtype in {np.float32, np.float64}:
            arr = (255 * arr).round()
        arr = arr.astype(np.uint8)
        return cls(
            arr.data,
            width,
            height,
            bytes_per_component * width,
            QtGui.QImage.Format.Format_RGB888,
        )

    def to_ndarray(self, fmt: FormatStr = "rgb888", channels: int = 3):
        import numpy as np

        qimage = self.convert_to_format(fmt)
        width = qimage.width()
        height = qimage.height()

        ptr = qimage.constBits()
        array = np.array(ptr).reshape(height, width, channels)  # Copies the data
        return array

    @classmethod
    def from_pil(cls, image) -> Self:
        # from https://github.com/python-pillow/Pillow/blob/main/src/PIL/ImageQt.py
        from PIL import ImageQt

        data = ImageQt._toqclass_helper(image)
        img = cls(data["data"], data["size"][0], data["size"][1], data["format"])
        if data["colortable"]:
            img.setColorTable(data["colortable"])
        img.__data = data["data"]
        return img

    def to_pil(self) -> Image:
        from PIL import Image as PILImage

        buffer = core.Buffer()
        buffer.open(core.Buffer.OpenModeFlag.ReadWrite)
        self.save(buffer, "PNG")
        return PILImage.open(io.BytesIO(buffer.data()))

    def invert_pixels(self, invert_alpha: bool = False):
        self.invertPixels(
            QtGui.QImage.InvertMode.InvertRgba
            if invert_alpha
            else QtGui.QImage.InvertMode.InvertRgb
        )

    def convert_to_format(self, fmt: FormatStr):
        if fmt not in FORMAT:
            raise InvalidParamError(fmt, FORMAT)
        self.convertToFormat(FORMAT[fmt])

    def as_bytes(self) -> bytes | None:
        bits = self.bits()
        if bits is None:
            return None
        match API:
            case "pyqt6":
                return bits.asstring(self.sizeInBytes())
            case "pyside6":
                return bits.tobytes()


if __name__ == "__main__":
    app = gui.app()
    image = gui.Pixmap(100, 100).toImage()
    image = Image(image)
    print(len(bytes(image)))
