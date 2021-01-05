from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtHelp


class HelpLink(QtHelp.QHelpLink):
    def get_url(self) -> core.Url:
        return core.Url(self.url)
