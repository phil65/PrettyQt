from __future__ import annotations

from prettyqt import core, qthelp, widgets
from prettyqt.qt import QtHelp
from prettyqt.utils import datatypes


class HelpSearchResultWidget(widgets.WidgetMixin):  # , QtHelp.QHelpSearchResultWidget):
    def __init__(self, item: QtHelp.QHelpFilterData):
        self.item = item

    def __getattr__(self, val):
        return getattr(self.item, val)

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
    app.main_loop()
