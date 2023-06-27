from __future__ import annotations

from prettyqt import gui


class TextImageFormat(gui.TextCharFormatMixin, gui.QTextImageFormat):
    def __bool__(self):
        return self.isValid()


if __name__ == "__main__":
    fmt = TextImageFormat()
