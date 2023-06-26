from __future__ import annotations

from prettyqt import constants, gui, widgets
from prettyqt.qt import QtWidgets


class GraphicsPolygonItem(
    widgets.AbstractGraphicsShapeItemMixin, QtWidgets.QGraphicsPolygonItem
):
    def get_polygon(self) -> gui.PolygonF:
        return gui.PolygonF(self.polygon())

    def set_fill_rule(self, rule: constants.FillRuleStr | constants.FillRule):
        self.setFillRule(constants.FILL_RULE.get_enum_value(rule))

    def get_fill_rule(self) -> constants.FillRuleStr:
        return constants.FILL_RULE.inverse[self.fillRule()]
