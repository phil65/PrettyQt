from __future__ import annotations

from typing import Literal

from typing_extensions import Self

from prettyqt import core, gui
from prettyqt.utils import bidict, datatypes, get_repr, serializemixin


MODE = bidict(
    normal=gui.QIcon.Mode.Normal,
    disabled=gui.QIcon.Mode.Disabled,
    active=gui.QIcon.Mode.Active,
    selected=gui.QIcon.Mode.Selected,
)

ModeStr = Literal["normal", "disabled", "active", "selected"]

STATE = bidict(off=gui.QIcon.State.Off, on=gui.QIcon.State.On)

StateStr = Literal["off", "on"]


class Icon(serializemixin.SerializeMixin, gui.QIcon):
    """Scalable icons in different modes and states."""

    def __repr__(self):
        return get_repr(self)

    def __bool__(self):
        return not self.isNull()

    def __getstate__(self):
        pixmap = self.pixmap(256, 256)
        return bytes(gui.Pixmap(pixmap))

    def __setstate__(self, ba):
        px = gui.Pixmap()
        px.__setstate__(ba)
        self.add_pixmap(px)

    @classmethod
    def for_color(cls, color_str: str) -> Self:
        color = gui.Color(color_str)
        bitmap = gui.Pixmap(16, 16)
        bitmap.fill(color)
        return cls(bitmap)

    @classmethod
    def from_char(cls, char: str, background="black", color="white") -> Self:
        """Create a QIcon with a given character."""
        icon = cls()
        for size in (16, 32, 64):
            px = gui.Pixmap.create_char(
                char, background=background, color=color, size=size
            )
            icon.addPixmap(px)
        return icon

    @classmethod
    def from_image(cls, image: gui.QImage) -> Self:
        return cls(gui.Pixmap.fromImage(image))

    def get_available_sizes(
        self,
        mode: ModeStr | gui.QIcon.Mode = "normal",
        state: StateStr | gui.QIcon.State = "off",
    ) -> list[core.Size]:
        m = MODE.get_enum_value(mode)
        s = STATE.get_enum_value(state)
        return [core.Size(i) for i in self.availableSizes(m, s)]

    def add_pixmap(
        self,
        data: core.QByteArray | gui.QPixmap | bytes,
        mode: ModeStr | gui.QIcon.Mode = "normal",
        state: StateStr | gui.QIcon.State = "off",
    ):
        if isinstance(data, bytes):
            data = core.QByteArray(data)
        if isinstance(data, core.QByteArray):
            pixmap = gui.QPixmap()
            pixmap.loadFromData(data)
        else:
            pixmap = data
        self.addPixmap(pixmap, MODE.get_enum_value(mode), STATE.get_enum_value(state))

    def get_pixmap(
        self,
        size: datatypes.SizeType | int,
        mode: ModeStr | gui.QIcon.Mode = "normal",
        state: StateStr | gui.QIcon.State = "off",
    ) -> gui.QPixmap:
        sz = datatypes.to_size(size)
        return self.pixmap(sz, MODE.get_enum_value(mode), STATE.get_enum_value(state))

    def get_actual_size(
        self,
        size: datatypes.SizeType,
        mode: ModeStr | gui.QIcon.Mode = "normal",
        state: StateStr | gui.QIcon.State = "off",
    ) -> core.Size:
        sz = datatypes.to_size(size)
        m = MODE.get_enum_value(mode)
        s = STATE.get_enum_value(state)
        actual_size = self.actualSize(sz, m, s)
        return core.Size(actual_size)


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    icon = Icon.from_char("A")
    window = widgets.MainWindow()
    window.set_icon(icon)
    window.show()
    app.exec()
