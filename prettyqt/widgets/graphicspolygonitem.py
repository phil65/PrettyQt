from __future__ import annotations

from prettyqt import constants, gui, widgets
from prettyqt.qt import QtWidgets
from prettyqt.utils import InvalidParamError


QtWidgets.QGraphicsPolygonItem.__bases__ = (widgets.AbstractGraphicsShapeItem,)


class GraphicsPolygonItem(QtWidgets.QGraphicsPolygonItem):
    def serialize_fields(self):
        return dict(polygon=self.get_polygon(), fill_rule=self.get_fill_rule())

    def get_polygon(self) -> gui.PolygonF:
        return gui.PolygonF(self.polygon())

    def set_fill_rule(self, rule: constants.FillRuleStr):
        if rule not in constants.FILL_RULE:
            raise InvalidParamError(rule, constants.FILL_RULE)
        self.setFillRule(constants.FILL_RULE[rule])

    def get_fill_rule(self) -> constants.FillRuleStr:
        return constants.FILL_RULE.inverse[self.fillRule()]
