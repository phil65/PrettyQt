from __future__ import annotations

from prettyqt import core, qthelp


class HelpSearchEngine(core.ObjectMixin, qthelp.QHelpSearchEngine):
    """Access to widgets reusable to integrate fulltext search."""

    def search_results(self, start: int, end: int) -> list[qthelp.HelpSearchResult]:
        return [qthelp.HelpSearchResult(i) for i in self.searchResults(start, end)]

    def get_result_widget(self) -> qthelp.HelpSearchResultWidget:
        return qthelp.HelpSearchResultWidget(self.resultWidget())


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    core_engine = qthelp.HelpEngineCore("test")
    engine = HelpSearchEngine(core_engine)
    widget = engine.get_result_widget()
    widget.show()
    app.exec()
