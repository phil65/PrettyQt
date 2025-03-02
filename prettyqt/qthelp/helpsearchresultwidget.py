from __future__ import annotations

from typing import TYPE_CHECKING

from prettyqt import core, qthelp, widgets


if TYPE_CHECKING:
    from prettyqt.utils import datatypes


class HelpSearchResultWidget(widgets.WidgetMixin):  # , qthelp.QHelpSearchResultWidget):
    """Text browser to display search results."""

    def __init__(self, item: qthelp.QHelpSearchResultWidget):
        self.item = item

    def __getattr__(self, val):
        return getattr(self.item, val)

    @classmethod
    def setup_example(cls):
        core_engine = qthelp.HelpEngineCore("test")
        engine = qthelp.HelpSearchEngine(core_engine)
        widget = engine.get_result_widget()
        widget.engine = engine
        widget.core_engine = core_engine
        return widget

    def get_link_at(self, point: datatypes.PointType) -> core.Url:
        if isinstance(point, tuple):
            point = core.Point(*point)
        return core.Url(self.linkAt(point))


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    core_engine = qthelp.HelpEngineCore("test")
    engine = qthelp.HelpSearchEngine(core_engine)
    widget = engine.get_result_widget()
    widget.show()
    app.exec()
