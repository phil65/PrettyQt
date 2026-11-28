import io
from typing import Literal, Self

from prettyqt import core, gui
from prettyqt.qt import API
from prettyqt.utils import bidict, helpers, serializemixin


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
    "cmyk8888",
]

FORMAT: bidict[FormatStr, gui.QImage.Format] = bidict(
    invalid=gui.QImage.Format.Format_Invalid,
    mono=gui.QImage.Format.Format_Mono,
    monolsb=gui.QImage.Format.Format_MonoLSB,
    indexed8=gui.QImage.Format.Format_Indexed8,
    rgb32=gui.QImage.Format.Format_RGB32,
    argb32=gui.QImage.Format.Format_ARGB32,
    argb32_premultiplied=gui.QImage.Format.Format_ARGB32_Premultiplied,
    rgb16=gui.QImage.Format.Format_RGB16,
    argb8565_premultiplied=gui.QImage.Format.Format_ARGB8565_Premultiplied,
    rgb666=gui.QImage.Format.Format_RGB666,
    argb6666_premultiplied=gui.QImage.Format.Format_ARGB6666_Premultiplied,
    rgb555=gui.QImage.Format.Format_RGB555,
    argb8555_premultiplied=gui.QImage.Format.Format_ARGB8555_Premultiplied,
    rgb888=gui.QImage.Format.Format_RGB888,
    rgb444=gui.QImage.Format.Format_RGB444,
    argb4444_premultiplied=gui.QImage.Format.Format_ARGB4444_Premultiplied,
    rgbx8888=gui.QImage.Format.Format_RGBX8888,
    rgba8888=gui.QImage.Format.Format_RGBA8888,
    rgba8888_premultiplied=gui.QImage.Format.Format_RGBA8888_Premultiplied,
    bgr30=gui.QImage.Format.Format_BGR30,
    a2bgr30_premultiplied=gui.QImage.Format.Format_A2BGR30_Premultiplied,
    rgb30=gui.QImage.Format.Format_RGB30,
    a2rgb30_premultiplied=gui.QImage.Format.Format_A2RGB30_Premultiplied,
    alpha8=gui.QImage.Format.Format_Alpha8,
    grayscale8=gui.QImage.Format.Format_Grayscale8,
    grayscale16=gui.QImage.Format.Format_Grayscale16,
    rgbx64=gui.QImage.Format.Format_RGBX64,
    rgba64=gui.QImage.Format.Format_RGBA64,
    rgba64_premultiplied=gui.QImage.Format.Format_RGBA64_Premultiplied,
    bgr888=gui.QImage.Format.Format_BGR888,
    rgbx16fpx4=gui.QImage.Format.Format_RGBX16FPx4,
    rgba16fpx4=gui.QImage.Format.Format_RGBA16FPx4,
    rgba16fpx4_premultiplied=gui.QImage.Format.Format_RGBA16FPx4_Premultiplied,
    rgbx32fpx4=gui.QImage.Format.Format_RGBX32FPx4,
    rgba32fpx4=gui.QImage.Format.Format_RGBA32FPx4,
    rgba32fpx4_premultiplied=gui.QImage.Format.Format_RGBA32FPx4_Premultiplied,
    cmyk8888=gui.QImage.Format.Format_CMYK8888,
)


class Image(serializemixin.SerializeMixin, gui.PaintDeviceMixin, gui.QImage):
    """Hardware-independent image representation with direct access to the pixel data."""

    def __setitem__(self, index: tuple[int, int], value):
        self.setPixel(index[1], index[0], value)

    def __getitem__(self, index: tuple[int, int]) -> int | list[int]:
        match index:
            case int() as row, int() as col:
                return self.pixel(col, row)
            case (row, col):
                rowcount = self.height()
                colcount = self.width()
                return [
                    self.pixel(j, i)
                    for i, j in helpers.iter_positions(row, col, rowcount, colcount)
                ]
            case _:
                raise TypeError(index)

    @classmethod
    def from_ndarray(cls, arr) -> Self:
        import numpy as np

        height, width, bytes_per_component = arr.shape
        if arr.dtype in {np.float32, np.float64}:
            arr = (255 * arr).round()
        arr = np.ascontiguousarray(arr, dtype=np.uint8)
        img = cls(
            arr.data,
            width,
            height,
            bytes_per_component * width,
            gui.QImage.Format.Format_RGB888,
        )
        img.__data = arr  # ty: ignore[missing-attribute]  # keeps the buffer alive
        return img

    def to_ndarray(
        self, fmt: FormatStr | gui.QImage.Format = "rgb888", channels: int = 3
    ):
        import numpy as np

        qimage = self.convert_to_format(fmt)
        width = qimage.width()
        height = qimage.height()
        ptr = qimage.constBits()
        if ptr is None:
            return np.empty((0, 0, channels), dtype=np.uint8)
        if API == "pyqt6":
            raw = ptr.asstring(qimage.sizeInBytes())  # ty: ignore[missing-attribute]
            arr = np.frombuffer(raw, dtype=np.uint8)
        else:
            arr = np.frombuffer(ptr, dtype=np.uint8)
        bytes_per_line = qimage.bytesPerLine()
        arr = arr.reshape((height, bytes_per_line))[:, : width * channels]
        return arr.reshape((height, width, channels)).copy()

    @classmethod
    def from_pil(cls, image) -> Self:
        # from https://github.com/python-pillow/Pillow/blob/main/src/PIL/ImageQt.py
        from PIL import ImageQt

        data = ImageQt._toqclass_helper(image)
        img = cls(data["data"], data["size"][0], data["size"][1], data["format"])
        if data["colortable"]:
            img.setColorTable(data["colortable"])
        img.__data = data["data"]  # ty: ignore[missing-attribute]  # keeps the buffer alive
        return img

    def to_pil(self):
        from PIL import Image as PILImage

        buffer = core.Buffer()
        buffer.open(core.Buffer.OpenModeFlag.ReadWrite)
        # PySide6's stub wants bytes, but only str works at runtime.
        self.save(buffer, "PNG")  # ty: ignore[no-matching-overload]
        return PILImage.open(io.BytesIO(buffer.data().data()))

    def invert_pixels(self, invert_alpha: bool = False):
        self.invertPixels(
            gui.QImage.InvertMode.InvertRgba
            if invert_alpha
            else gui.QImage.InvertMode.InvertRgb
        )

    def convert_to_format(self, fmt: FormatStr | gui.QImage.Format) -> Self:
        return type(self)(self.convertToFormat(FORMAT.get_enum_value(fmt)))

    def as_bytes(self) -> bytes:
        bits = self.bits()
        if bits is None:
            return b""
        if API == "pyqt6":  # sip.voidptr, the stubs only know PySide6's memoryview
            return bits.asstring(self.sizeInBytes())  # ty: ignore[missing-attribute]
        return bytes(bits)


if __name__ == "__main__":
    app = gui.app()
    image = gui.Pixmap(100, 100).toImage()
    image = Image(image)
    print(len(bytes(image)))
