from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtHelp


class HelpSearchResult(QtHelp.QHelpSearchResult):
    """The data associated with the search result."""

    def get_url(self) -> core.Url:
        return core.Url(self.url())
