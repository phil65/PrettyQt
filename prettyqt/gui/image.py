from __future__ import annotations

from prettyqt import core, gui
from prettyqt.qt import API, QtGui


class Image(gui.PaintDeviceMixin, QtGui.QImage):
    def __getstate__(self):
        return bytes(self)

    def __setstate__(self, ba):
        core.DataStream.write_bytearray(ba, self)

    def __setitem__(self, index: tuple[int, int], value):
        self.setPixel(index[0], index[1], value)

    def __reduce__(self):
        return type(self), (), self.__getstate__()

    def __getitem__(self, index: tuple[int, int]):
        return self.pixel(index[0], index[1])

    def __bytes__(self):
        ba = core.DataStream.create_bytearray(self)
        return bytes(ba)

    @classmethod
    def from_ndarray(cls, arr) -> Image:
        import numpy as np

        height, width, channel = arr.shape
        if arr.dtype in {np.float32, np.float64}:
            arr = (255 * arr).round()
        arr = arr.astype(np.uint8)
        return cls(arr.data, width, height, channel * width, cls.Format.Format_RGB888)

    @classmethod
    def from_pil(cls, image):
        # from https://github.com/python-pillow/Pillow/blob/main/src/PIL/ImageQt.py
        from PIL import ImageQt

        data = ImageQt._toqclass_helper(image)
        img = cls(data["data"], data["size"][0], data["size"][1], data["format"])
        if data["colortable"]:
            img.setColorTable(data["colortable"])
        img.__data = data["data"]
        return img

    def to_pil(self) -> Image:
        import io

        from PIL import Image as PILImage

        buffer = core.Buffer()
        buffer.open(core.Buffer.OpenModeFlag.ReadWrite)
        self.save(buffer, "PNG")
        return PILImage.open(io.BytesIO(buffer.data()))

    def invert_pixels(self, invert_alpha: bool = False):
        self.invertPixels(
            self.InvertMode.InvertRgba if invert_alpha else self.InvertMode.InvertRgb
        )

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
