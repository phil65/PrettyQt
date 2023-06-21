from __future__ import annotations

import emoji

from prettyqt import constants, core, gui

ZERO_COORD = core.Point(0, 0)


class EmojiIconEngine(gui.IconEngine):
    """A custom QIconEngine that can render emojis."""

    def __init__(self, name: str, language: str = "alias") -> None:
        self._name = name
        self._language = language
        super().__init__()

    def paint(
        self,
        painter: gui.QPainter,
        rect: core.QRect,
        mode: gui.QIcon.Mode,
        state: gui.QIcon.State,
    ):
        icon_char = emoji.emojize(f":{self._name}:", language=self._language)
        painter.drawText(rect, int(constants.ALIGN_CENTER), icon_char)

    def clone(self):
        """Required to subclass abstract QIconEngine."""
        return EmojiIconEngine(self._name, self._language)

    def pixmap(self, size, mode, state) -> gui.QPixmap:
        pm = gui.QPixmap(size)
        pm.fill(constants.GlobalColor.transparent)
        rect = core.Rect(ZERO_COORD, size)
        with gui.Painter(pm) as painter:
            self.paint(painter, rect, mode, state)
        return pm


class Emojis:
    def __init__(self):
        self._names = {v["en"][1:-1]: k for k, v in emoji.EMOJI_DATA.items()}

    def __getattr__(self, attribute):
        return self._names[attribute]

    def __dir__(self):
        return self._names


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    provider = Emojis()
    print(dir(provider))
    engine = EmojiIconEngine("thumbsup")
    icon = gui.QIcon(engine)
    widget = widgets.Widget()
    widget.set_icon(icon)
    widget.show()
    app.exec()
