from __future__ import annotations

import base64
import os
import pathlib
from typing import Self

from prettyqt import constants, core, gui
from prettyqt.utils import colors, datatypes, serializemixin


class PixmapMixin(serializemixin.SerializeMixin, gui.PaintDeviceMixin):
    """Off-screen image representation that can be used as a paint device."""

    def __bool__(self):
        return not self.isNull()

    def __eq__(self, other):
        return self.toImage() == other.toImage() if isinstance(other, Pixmap) else False

    def __hash__(self):
        return self.cacheKey()

    @classmethod
    def from_file(cls, path: datatypes.PathType) -> Self:
        path = pathlib.Path(path)
        with path.open(mode="rb") as f:
            data = f.read()
        # Create widget
        pixmap = cls()
        pixmap.loadFromData(core.QByteArray(data))
        return pixmap

    @classmethod
    def from_image(
        cls,
        img: gui.QImage,
        color_preference: constants.ColorPreferenceStr = "auto",
        dithering: constants.DitherPreferenceStr = "diffuse",
        alpha_dithering: constants.AlphaDitherPreferenceStr = "threshold",
        mode_preference: constants.ModePreferenceStr = "auto",
    ) -> Self:
        flag = constants.ImageConversionFlag(0)
        flag |= constants.COLOR_PREFERENCE.inverse[color_preference]
        flag |= constants.DITHER_PREFERENCE.inverse[dithering]
        flag |= constants.ALPHA_DITHER_PREFERENCE.inverse[alpha_dithering]
        flag |= constants.MODE_PREFERENCE.inverse[mode_preference]
        return cls(cls.fromImage(img, flag))

    def save_to_file(
        self,
        path: str | os.PathLike[str],
        fmt: str = "png",
        quality: int | None = None,
    ) -> bool:
        return self.save(os.fspath(path), fmt, -1 if quality is None else quality)

    def get_size(self) -> core.Size:
        return core.Size(self.size())

    def get_rect(self) -> core.Rect:
        return core.Rect(self.rect())

    def to_image(self) -> gui.Image:
        return gui.Image(self.toImage())

    def rotated(self, rotation: int) -> Pixmap:
        w, h = self.width(), self.height()
        pixmap = self.transformed(gui.Transform().rotate(rotation))
        return pixmap.copy((pixmap.width() - w) // 2, (pixmap.height() - h) // 2, w, h)

    def get_image_data_url(self) -> str:
        """Render the contents of the pixmap as a data URL (RFC-2397).

        Returns:
            datauri : str
        """
        device = core.Buffer()
        assert device.open_file("read_write")
        self.save(device, b"png")
        device.close()
        data = bytes(device.data())
        payload = base64.b64encode(data).decode("ascii")
        return f"data:image/png;base64,{payload}"

    @classmethod
    def create_dot(cls, color: datatypes.ColorType = "black", size: int = 16) -> Self:
        col = colors.get_color(color)
        px = cls(size, size)
        px.fill(constants.GlobalColor.transparent)  # type: ignore
        px_size = px.rect().adjusted(1, 1, -1, -1)
        with gui.Painter(px) as painter:
            painter.use_antialiasing()
            painter.setBrush(col)
            pen_color = gui.Color(15, 15, 15)
            painter.set_pen(color=pen_color, width=1)
            painter.drawEllipse(px_size)
        return px

    @classmethod
    def create_checkerboard_pattern(
        cls, n: int, color_1: datatypes.ColorType, color_2: datatypes.ColorType
    ) -> Self:
        """Construct tileable checkerboard pattern for paint events."""
        # Brush will be an nxn checkerboard pattern
        pat = cls(2 * n, 2 * n)
        bg0 = colors.get_color(color_1)
        bg1 = colors.get_color(color_2)
        with gui.Painter(pat) as p:
            p.setPen(constants.PenStyle.NoPen)
            # Paint a checkerboard pattern for the color to be overlaid on
            p.fillRect(pat.rect(), bg0)
            p.fillRect(0, 0, n, n, bg1)
            p.fillRect(n, n, 2 * n, 2 * n, bg1)
        return pat

    @classmethod
    def create_char(
        cls,
        char: str,
        size: int,
        background: datatypes.ColorType = "black",
        color: datatypes.ColorType = "white",
    ) -> Self:
        pixmap = cls(size, size)
        pixmap.fill(constants.GlobalColor.transparent)
        with gui.Painter(pixmap) as painter:
            painter.setRenderHints(
                painter.RenderHint.Antialiasing
                | painter.RenderHint.TextAntialiasing
                | painter.RenderHint.SmoothPixmapTransform
            )
            painter.set_pen(color=background)
            painter.set_brush(background)
            margin = 1 + size // 16
            text_margin = size // 20
            w = size - 2 * margin
            rect = core.RectF(margin, margin, w, w)
            painter.draw_rounded_rect(rect, 30, 30, relative=True)
            painter.set_pen(color=color)
            with painter.edit_font() as font:  # type: gui.QFont
                font.setPixelSize(size - 2 * margin - 2 * text_margin)
            painter.draw_text(rect, char, alignment="center")
        return pixmap


class Pixmap(PixmapMixin, gui.QPixmap):
    pass


if __name__ == "__main__":
    from prettyqt import gui

    app = gui.app()
    p = Pixmap.create_char("A", 20)
    print(bytes(p))
