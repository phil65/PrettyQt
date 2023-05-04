from __future__ import annotations

import enum

from prettyqt import constants, core, gui, widgets
from prettyqt.qt import QtCore


class AccordionItem(widgets.GroupBox):
    def __init__(self, title, widget):
        super().__init__(None)

        # create the layout
        layout = widgets.BoxLayout("vertical")
        layout.set_margin(6)
        layout.setSpacing(0)
        layout.addWidget(widget)

        self._rollout_style = 2
        self._drag_drop_mode = 0

        self.setAcceptDrops(True)
        self.setLayout(layout)
        self.set_context_menu_policy("custom")
        self.customContextMenuRequested.connect(self.show_menu)

        # create custom properties
        self._widget = widget
        self._collapsed = False
        self._collapsible = True
        self._clicked = False

        # set common properties
        self.setTitle(title)

    def dragEnterEvent(self, event):
        if not self._drag_drop_mode:
            return

        source = event.source()
        if (
            source != self
            and source.parent() == self.parent()
            and isinstance(source, AccordionItem)
        ):
            event.acceptProposedAction()

    def get_drag_drop_rect(self) -> core.Rect:
        return core.Rect(25, 7, 10, 6)

    def get_drag_drop_mode(self) -> AccordionWidget.RolloutStyle:
        return self._drag_drop_mode

    def dragMoveEvent(self, event):
        if not self._drag_drop_mode:
            return

        source = event.source()
        if (
            source != self
            and source.parent() == self.parent()
            and isinstance(source, AccordionItem)
        ):
            event.acceptProposedAction()

    def dropEvent(self, event):
        widget = event.source()
        layout = self.parent().layout()
        layout.insertWidget(layout.indexOf(self), widget)
        self._widget.emitItemsReordered()

    def expand_collapsed_rect(self) -> core.Rect:
        return core.Rect(0, 0, self.width(), 20)

    # def enterEvent(self, event):
    #     self.accordionWidget().leaveEvent(event)
    #     event.accept()

    # def leaveEvent(self, event):
    #     self.accordionWidget().enterEvent(event)
    #     event.accept()

    def mouseReleaseEvent(self, event):
        if self._clicked and self.expand_collapsed_rect().contains(
            event.position().toPoint()
        ):
            self.toggle_collapsed()
            event.accept()
        else:
            event.ignore()

        self._clicked = False

    def mouseMoveEvent(self, event):
        event.ignore()

    def mousePressEvent(self, event):
        # handle an internal move

        # start a drag event
        if (
            event.button() == QtCore.Qt.MouseButton.LeftButton
            and self.get_drag_drop_rect().contains(event.position().toPoint())
        ):
            # create the pixmap
            pixmap = self.grab()

            # create the mimedata
            mime_data = core.MimeData()
            mime_data.setText("ItemTitle::%s" % (self.title()))

            # create the drag
            drag = gui.Drag(self)
            drag.setMimeData(mime_data)
            drag.setPixmap(pixmap)
            drag.setHotSpot(event.position().toPoint())

            if not drag.exec():
                self._widget.emitItemDragFailed(self)

            event.accept()

        # determine if the expand/collapse should occur
        elif (
            event.button() == QtCore.Qt.MouseButton.LeftButton
            and self.expand_collapsed_rect().contains(event.position().toPoint())
        ):
            self._clicked = True
            event.accept()

        else:
            event.ignore()

    def isCollapsed(self) -> bool:
        return self._collapsed

    def isCollapsible(self) -> bool:
        return self._collapsible

    def _draw_triangle(self, painter, x, y):
        brush = gui.Brush(
            gui.Color(255, 255, 255, 160), QtCore.Qt.BrushStyle.SolidPattern
        )
        tl, tr, tp = (
            (
                core.Point(x + 11, y + 6),
                core.Point(x + 16, y + 11),
                core.Point(x + 11, y + 16),
            )
            if self.isCollapsed()
            else (
                core.Point(x + 9, y + 8),
                core.Point(x + 19, y + 8),
                core.Point(x + 14, y + 13),
            )
        )
        points = [tl, tr, tp]
        triangle = gui.Polygon(points)
        currentBrush = painter.brush()
        painter.setBrush(brush)
        painter.drawPolygon(triangle)
        painter.setBrush(currentBrush)

    def paintEvent(self, event):
        with gui.Painter(self) as painter:
            painter.setRenderHint(painter.RenderHint.Antialiasing)
            font = painter.font()
            font.setBold(True)
            painter.setFont(font)

            x = self.rect().x()
            y = self.rect().y()
            w = self.rect().width() - 1
            h = self.rect().height() - 1
            light_color = self.palette().color(gui.Palette.ColorRole.Light)
            shadow_color = self.palette().color(gui.Palette.ColorRole.Shadow)
            # draw a rounded style
            if self._rollout_style == AccordionWidget.RolloutStyle.Rounded:
                # draw the text
                painter.drawText(
                    x + 33,
                    y + 3,
                    w,
                    16,
                    constants.ALIGN_TOP_LEFT,
                    self.title(),
                )

                # draw the triangle
                self._draw_triangle(painter, x, y)
                # draw the borders
                pen = gui.Pen(light_color)
                pen.setWidthF(0.6)
                painter.setPen(pen)

                r = 8
                painter.drawRoundedRect(x + 1, y + 1, w - 1, h - 1, r, r)

                pen.setColor(shadow_color)
                painter.setPen(pen)

                painter.drawRoundedRect(x, y, w - 1, h - 1, r, r)

            # draw a square style
            if self._rollout_style == AccordionWidget.RolloutStyle.Square:
                # draw the text
                painter.drawText(
                    x + 33, y + 3, w, 16, constants.ALIGN_TOP_LEFT, self.title()
                )

                self._draw_triangle(painter, x, y)

                # draw the borders
                pen = gui.Pen(light_color)
                pen.setWidthF(0.6)
                painter.setPen(pen)

                painter.drawRect(x + 1, y + 1, w - 1, h - 1)

                pen.setColor(shadow_color)
                painter.setPen(pen)

                painter.drawRect(x, y, w - 1, h - 1)

            # draw a Maya style
            if self._rollout_style == AccordionWidget.RolloutStyle.Maya:
                # draw the text
                painter.drawText(
                    x + 33,
                    y + 3,
                    w,
                    16,
                    constants.ALIGN_TOP_LEFT,
                    self.title(),
                )

                painter.setRenderHint(gui.Painter.RenderHint.Antialiasing, False)

                self._draw_triangle(painter, x, y)

                # draw the borders - top
                header_height = 20

                header_rect = core.Rect(x + 1, y + 1, w - 1, header_height)
                header_rect_shadow = core.Rect(x - 1, y - 1, w + 1, header_height + 2)

                # Highlight
                pen = gui.Pen(light_color)
                pen.setWidthF(0.4)
                painter.setPen(pen)

                painter.drawRect(header_rect)
                painter.fillRect(header_rect, gui.Color(255, 255, 255, 18))

                # Shadow
                pen.setColor(self.palette().color(gui.Palette.ColorRole.Dark))
                painter.setPen(pen)
                painter.drawRect(header_rect_shadow)

                if not self.isCollapsed():
                    # draw the lover border
                    pen = gui.Pen(self.palette().color(gui.Palette.ColorRole.Dark))
                    pen.setWidthF(0.8)
                    painter.setPen(pen)

                    offset = header_height + 3
                    body_rect = core.Rect(x, y + offset, w, h - offset)
                    body_rect_shadow = core.Rect(x + 1, y + offset, w + 1, h - offset + 1)
                    painter.drawRect(body_rect)

                    pen.setColor(light_color)
                    pen.setWidthF(0.4)
                    painter.setPen(pen)

                    painter.drawRect(body_rect_shadow)

            # draw a boxed style
            elif self._rollout_style == AccordionWidget.RolloutStyle.Boxed:
                if self.isCollapsed():
                    arect = core.Rect(x + 1, y + 9, w - 1, 4)
                    brect = core.Rect(x, y + 8, w - 1, 4)
                    text = "+"
                else:
                    arect = core.Rect(x + 1, y + 9, w - 1, h - 9)
                    brect = core.Rect(x, y + 8, w - 1, h - 9)
                    text = "-"

                # draw the borders
                pen = gui.Pen(light_color)
                pen.setWidthF(0.6)
                painter.setPen(pen)

                painter.drawRect(arect)

                pen.setColor(shadow_color)
                painter.setPen(pen)

                painter.drawRect(brect)

                painter.setRenderHint(painter.RenderHint.Antialiasing, False)
                painter.setBrush(
                    self.palette().color(gui.Palette.ColorRole.Window).darker(120)
                )
                painter.drawRect(x + 10, y + 1, w - 20, 16)
                painter.drawText(
                    x + 16,
                    y + 1,
                    w - 32,
                    16,
                    constants.ALIGN_CENTER_LEFT,
                    text,
                )
                painter.drawText(
                    x + 10,
                    y + 1,
                    w - 20,
                    16,
                    QtCore.Qt.AlignmentFlag.AlignCenter,
                    self.title(),
                )

            if self.get_drag_drop_mode():
                rect = self.get_drag_drop_rect()

                # draw the lines
                left = rect.left()
                right = rect.right()
                cy = rect.center().y()

                for y in (cy - 3, cy, cy + 3):
                    painter.drawLine(left, y, right, y)

    def setCollapsed(self, state: bool = True):
        if not self.isCollapsible():
            return
        with self._widget.updates_off():
            self._collapsed = state

            if state:
                self.setMinimumHeight(22)
                self.setMaximumHeight(22)
                self.widget().setVisible(False)
            else:
                self.setMinimumHeight(0)
                self.setMaximumHeight(1000000)
                self.widget().setVisible(True)

            # self._widget.emitItemCollapsed(self)

    def setCollapsible(self, state: bool = True):
        self._collapsible = state

    def set_drag_drop_mode(self, mode):
        self._drag_drop_mode = mode

    def set_rollout_style(self, style):
        self._rollout_style = style

    def show_menu(self):
        if core.Rect(0, 0, self.width(), 20).contains(
            self.mapFromGlobal(gui.Cursor.pos())
        ):
            pass
            # self._widget.emitItemMenuRequested(self)

    def get_rollout_style(self):
        return self._rollout_style

    def toggle_collapsed(self):
        self.setCollapsed(not self.isCollapsed())

    def widget(self):
        return self._widget


class AccordionWidget(widgets.ScrollArea):
    itemCollapsed = core.Signal(AccordionItem)
    itemMenuRequested = core.Signal(AccordionItem)
    itemDragFailed = core.Signal(AccordionItem)
    itemsReordered = core.Signal()

    @core.Enum
    class RolloutStyle(enum.IntEnum):
        """Rollout style for the widget."""

        Boxed = 1
        Rounded = 2
        Square = 3
        Maya = 4

    @core.Enum
    class DragDropMode(enum.IntEnum):
        """Drag drop mode for the widget."""

        NoDragDrop = 0
        InternalMove = 1

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFrameShape(widgets.ScrollArea.Shape.NoFrame)
        self.setAutoFillBackground(False)
        self.setWidgetResizable(True)
        self.setMouseTracking(True)
        # self.verticalScrollBar().setMaximumWidth(10)

        widget = widgets.Widget(self)

        # define custom properties
        self._rollout_style = self.RolloutStyle.Rounded
        self._drag_drop_mode = self.DragDropMode.NoDragDrop
        self._scrolling = False
        self._scroll_init_y = 0
        self._scroll_init_val = 0
        self._ItemClass = AccordionItem
        self._items = {}

        layout = widgets.BoxLayout("vertical")
        layout.set_margin(2)
        layout.setSpacing(2)
        layout.addStretch(1)

        widget.setLayout(layout)

        self.setWidget(widget)

    def setSpacing(self, spaceInt):
        self.widget().layout().setSpacing(spaceInt)

    def addItem(
        self,
        title: object,
        widget: object,
        collapsed: object = False,
        index: object = None,
    ) -> object:
        with self.updates_off():
            item = self._ItemClass(title, widget)
            item.set_rollout_style(self.get_rollout_style())
            item.set_drag_drop_mode(self.get_drag_drop_mode())
            layout = self.widget().layout()
            if index is None:  # append if not specified index
                index = layout.count() - 1
            layout.insertWidget(index, item)
            layout.setStretchFactor(item, 0)

            if collapsed:
                item.setCollapsed(collapsed)
            return item

    def clear(self):
        with self.updates_off():
            layout = self.widget().layout()
            while layout.count() > 1:
                item = layout.itemAt(0)

                # remove the item from the layout
                w = item.widget()
                layout.removeItem(item)

                # close the widget and delete it
                w.close()
                w.deleteLater()

    # def eventFilter(self, object, event) -> bool:
    #     if event.type() == QtCore.QEvent.Type.MouseButtonPress:
    #         self.mousePressEvent(event)
    #         return True

    #     elif event.type() == QtCore.QEvent.Type.MouseMove:
    #         self.mouseMoveEvent(event)
    #         return True

    #     elif event.type() == QtCore.QEvent.Type.MouseButtonRelease:
    #         self.mouseReleaseEvent(event)
    #         return True

    #     return False

    def canScroll(self):
        return self.verticalScrollBar().maximum() > 0

    def count(self):
        return self.widget().layout().count() - 1

    def get_drag_drop_mode(self) -> DragDropMode:
        return self._drag_drop_mode

    def indexOf(self, widget):
        layout = self.widget().layout()
        return next(
            (
                index
                for index in range(layout.count())
                if layout.itemAt(index).widget().widget() == widget
            ),
            -1,
        )

    def is_boxed_mode(self):
        return self._rollout_style == self.RolloutStyle.Boxed

    def get_rollout_style(self):
        return self._rollout_style

    def item_class(self):
        return self._ItemClass

    def itemAt(self, index):
        layout = self.widget().layout()
        if 0 <= index < layout.count() - 1:
            return layout.itemAt(index).widget()
        return None

    def emitItemCollapsed(self, item):
        if not self.signalsBlocked():
            self.itemCollapsed.emit(item)

    def emitItemDragFailed(self, item):
        if not self.signalsBlocked():
            self.itemDragFailed.emit(item)

    def emitItemMenuRequested(self, item):
        if not self.signalsBlocked():
            self.itemMenuRequested.emit(item)

    def emitItemsReordered(self):
        if not self.signalsBlocked():
            self.itemsReordered.emit()

    def enterEvent(self, event):
        if self.canScroll():
            widgets.Application.setOverrideCursor(QtCore.Qt.CursorShape.OpenHandCursor)

    def leaveEvent(self, event):
        if self.canScroll():
            widgets.Application.restoreOverrideCursor()

    def mouseMoveEvent(self, event):
        if self._scrolling:
            sbar = self.verticalScrollBar()
            smax = sbar.maximum()

            # calculate the distance moved for the moust point
            dy = event.globalY() - self._scroll_init_y

            # calculate the percentage that is of the scroll bar
            dval = smax * (dy / float(sbar.height()))

            # calculate the new value
            sbar.setValue(self._scroll_init_val - dval)

        event.accept()

    def mousePressEvent(self, event):
        # handle a scroll event
        if event.button() == QtCore.Qt.MouseButton.LeftButton and self.canScroll():
            self._scrolling = True
            self._scroll_init_y = event.globalY()
            self._scroll_init_val = self.verticalScrollBar().value()

            widgets.Application.setOverrideCursor(QtCore.Qt.CursorShape.ClosedHandCursor)

        event.accept()

    def mouseReleaseEvent(self, event):
        if self._scrolling:
            widgets.Application.restoreOverrideCursor()

        self._scrolling = False
        self._scroll_init_y = 0
        self._scroll_init_val = 0
        event.accept()

    def move_item_down(self, index):
        layout = self.widget().layout()
        if (layout.count() - 1) > (index + 1):
            widget = layout.takeAt(index).widget()
            layout.insertWidget(index + 1, widget)

    def move_item_up(self, index):
        if index > 0:
            layout = self.widget().layout()
            widget = layout.takeAt(index).widget()
            layout.insertWidget(index - 1, widget)

    def set_drag_drop_mode(self, mode: DragDropMode):
        self._drag_drop_mode = mode

        for item in self.findChildren(AccordionItem):
            item.set_drag_drop_mode(self._drag_drop_mode)

    def set_item_class(self, item_class):
        self._ItemClass = item_class

    def set_rollout_style(self, rollout_style: RolloutStyle):
        self._rollout_style = rollout_style

        for item in self.findChildren(AccordionItem):
            item.set_rollout_style(self._rollout_style)

    def takeAt(self, index):
        with self.updates_off():
            layout = self.widget().layout()
            widget = None
            if 0 <= index < layout.count() - 1:
                item = layout.itemAt(index)
                widget = item.widget()

                layout.removeItem(item)
                widget.close()
            return widget

    def widgetAt(self, index):
        return item.widget() if (item := self.itemAt(index)) else None

    rollout_style = core.Property(int, get_rollout_style, set_rollout_style)
    dragdrop_mode = core.Property(int, get_drag_drop_mode, set_drag_drop_mode)


if __name__ == "__main__":
    app = widgets.app()
    widget = AccordionWidget()
    item = AccordionItem("hallo", widgets.LineEdit("test"))
    widget.addItem("tsektjk", AccordionItem("hallo", widgets.LineEdit("test")))
    widget.addItem("tsektjk", AccordionItem("hallo", widgets.LineEdit("test")))
    widget.addItem("tsektjk", item)
    widget.addItem("tsektjk", item)
    widget.show()
    app.main_loop()
