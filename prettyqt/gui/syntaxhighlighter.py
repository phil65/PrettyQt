from __future__ import annotations

from prettyqt import core, gui


class SyntaxHighlighterMixin(core.ObjectMixin):
    def __init__(self, parent: core.QObject | None = None):
        super().__init__(parent)  # type: ignore

    def get_current_block(self) -> gui.TextBlock:
        return gui.TextBlock(self.currentBlock())

    def get_format(self, position: int) -> gui.TextCharFormat:
        return gui.TextCharFormat(self.format(position))


class SyntaxHighlighter(SyntaxHighlighterMixin, gui.QSyntaxHighlighter):
    pass
