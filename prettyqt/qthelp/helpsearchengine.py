from __future__ import annotations

from prettyqt import core, qthelp
from prettyqt.qt import QtHelp


class HelpSearchEngine(core.ObjectMixin, QtHelp.QHelpSearchEngine):
    def search_results(self, start: int, end: int) -> list[qthelp.HelpSearchResult]:
        return [qthelp.HelpSearchResult(i) for i in self.searchResults(start, end)]


if __name__ == "__main__":
    core = qthelp.HelpEngine("test")
    engine = HelpSearchEngine(core)
