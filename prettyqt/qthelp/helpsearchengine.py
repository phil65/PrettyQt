from __future__ import annotations

from typing import List

from prettyqt import core, qthelp
from prettyqt.qt import QtHelp


QtHelp.QHelpSearchEngine.__bases__ = (core.Object,)


class HelpSearchEngine(QtHelp.QHelpSearchEngine):
    def search_results(self, start: int, end: int) -> List[qthelp.HelpSearchResult]:
        return [qthelp.HelpSearchResult(i) for i in self.searchResults(start, end)]


if __name__ == "__main__":
    core = qthelp.HelpEngine("test")
    engine = HelpSearchEngine(core)
