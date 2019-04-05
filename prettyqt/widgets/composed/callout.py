# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtGui, QtCore
from prettyqt import gui, widgets


class Callout(widgets.GraphicsItem):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.anchor = QtCore.QPointF()
        self.text = None
        self.text_rect = None

    def boundingRect(self) -> QtCore.QRectF:
        anchor = self.mapFromParent(self.chart.mapToPosition(self.anchor))
        rect = QtCore.QRectF()
        rect.setLeft(min(self.rect.left(), anchor.x()))
        rect.setRight(max(self.rect.right(), anchor.x()))
        rect.setTop(min(self.rect.top(), anchor.y()))
        rect.setBottom(max(self.rect.bottom(), anchor.y()))
        return rect

    def paint(self, painter, option, widget):
        path = QtGui.QPainterPath()
        path.addRoundedRect(self.rect, 5, 5)

        anchor = self.mapFromParent(self.chart.mapToPosition(self.anchor))
        if not self.rect.contains(anchor):
            point1 = QtCore.QPointF()
            point2 = QtCore.QPointF()

            # establish the position of the anchor point in relation to self.rect
            above = anchor.y() <= self.rect.top()
            above_center = self.rect.top() < anchor.y() <= self.rect.center().y()
            below_center = self.rect.center().y() < anchor.y() <= self.rect.bottom()
            below = anchor.y() > self.rect.bottom()

            on_left = anchor.x() <= self.rect.left()
            left_of_center = self.rect.left() < anchor.x() <= self.rect.center().x()
            right_of_center = self.rect.center().x() < anchor.x() <= self.rect.right()
            on_right = anchor.x() > self.rect.right()

            # get the nearest self.rect corner.
            x = (on_right + right_of_center) * self.rect.width()
            y = (below + below_center) * self.rect.height()
            corner_case = (above and on_left) or (above and on_right) or (
                below and on_left) or (below and on_right)
            vertical = abs(anchor.x() - x) > abs(anchor.y() - y)

            x1 = x + left_of_center * 10 - right_of_center * 20 + \
                corner_case * (not vertical) * (on_left * 10 - on_right * 20)
            y1 = y + above_center * 10 - below_center * 20 + \
                corner_case * vertical * (above * 10 - below * 20)
            point1.setX(x1)
            point1.setY(y1)

            x2 = x + left_of_center * 20 - right_of_center * 10 + \
                corner_case * (not vertical) * (on_left * 20 - on_right * 10)
            y2 = y + above_center * 20 - below_center * 10 + \
                corner_case * vertical * (above * 20 - below * 10)
            point2.setX(x2)
            point2.setY(y2)

            path.moveTo(point1)
            path.lineTo(anchor)
            path.lineTo(point2)
            path = path.simplified()
            painter.setBrush(gui.Color(255, 255, 255))
        painter.drawPath(path)
        painter.drawText(self.text_rect, self.text)

    def mousePressEvent(self, event):
        event.setAccepted(True)

    def mouseMoveEvent(self, event):
        if event.buttons() & QtCore.Qt.LeftButton:
            pos = event.pos() - event.buttonDownPos(QtCore.Qt.LeftButton)
            self.setPos(self.mapToParent(pos))
            event.setAccepted(True)
        else:
            event.setAccepted(False)

    def setText(self, text: str):
        self.text = text
        metrics = QtGui.QFontMetrics(self.font)
        self.text_rect = metrics.boundingRect(QtCore.QRect(0, 0, 150, 150),
                                              QtCore.Qt.AlignLeft,
                                              self.text)
        self.text_rect.translate(5, 5)
        self.prepareGeometryChange()
        self.rect = self.text_rect.adjusted(-5, -5, 5, 5)

    def setAnchor(self, point):
        self.anchor = point

    def updateGeometry(self):
        self.prepareGeometryChange()
        self.setPos(self.chart.mapToPosition(self.anchor) + QtCore.QPoint(10, -50))
