from __future__ import annotations

import enum

from typing import Literal

from prettyqt import constants, core, gui, widgets
from prettyqt.utils import bidict, colors, datatypes, listdelegators


SceneLayerStr = Literal["item", "background", "foreground", "all"]

SCENE_LAYER: bidict[SceneLayerStr, widgets.QGraphicsScene.SceneLayer] = bidict(
    item=widgets.QGraphicsScene.SceneLayer.ItemLayer,
    background=widgets.QGraphicsScene.SceneLayer.BackgroundLayer,
    foreground=widgets.QGraphicsScene.SceneLayer.ForegroundLayer,
    all=widgets.QGraphicsScene.SceneLayer.AllLayers,
)

ItemIndexMethodStr = Literal["bsp_tree", "none"]

ITEM_INDEX_METHOD: bidict[ItemIndexMethodStr, widgets.QGraphicsScene.ItemIndexMethod] = (
    bidict(
        bsp_tree=widgets.QGraphicsScene.ItemIndexMethod.BspTreeIndex,
        none=widgets.QGraphicsScene.ItemIndexMethod.NoIndex,
    )
)


class GraphicsScene(core.ObjectMixin, widgets.QGraphicsScene):
    """Surface for managing a large number of 2D graphical items."""

    class GridType(enum.IntEnum):
        """Grid type for background."""

        NoGrid = 0
        DotGrid = 1
        LineGrid = 2

    def __init__(self, parent=None):
        super().__init__(parent)
        self._grid_mode = self.GridType.LineGrid
        self._grid_size = 50
        self._pen_width = 0.65
        self._grid_color = self.get_palette().get_color("text")
        self._bg_color = self.get_palette().get_color("window")
        # self.setBackgroundBrush(self._bg_color)

    def __repr__(self):
        cls_name = str(self.__class__.__name__)
        return f'<{cls_name}("{self.viewer()}") object at {hex(id(self))}>'

    def __getitem__(self, index: int) -> widgets.QGraphicsItem:
        return self.items()[index]

    def _get_map(self):
        maps = super()._get_map()
        maps |= {"itemIndexMethod": ITEM_INDEX_METHOD}
        return maps

    def get_palette(self) -> gui.Palette:
        return gui.Palette(self.palette())

    def get_font(self) -> gui.Font:
        return gui.Font(self.font())

    def get_background_brush(self) -> gui.Brush:
        return gui.Brush(self.backgroundBrush())

    def get_foreground_brush(self) -> gui.Brush:
        return gui.Brush(self.foregroundBrush())

    def add(self, item) -> widgets.QGraphicsItem:
        match item:
            case widgets.QGraphicsItem():
                self.addItem(item)
                return item
            case gui.QPixmap():
                return self.add_pixmap(item)
            case gui.QPainterPath():
                return self.add_path(item)
            case gui.QPolygonF():
                return self.add_polygon(item)
            case core.QRectF():
                return self.add_rect(item)
            case core.QLine():
                return self.add_line(item)
            case str():
                return self.add_text(item)
            case widgets.QWidget():
                return self.add_widget(item)
            case _:
                raise TypeError(item)

    def add_pixmap(self, pixmap: gui.QPixmap) -> widgets.GraphicsPixmapItem:
        g_item = widgets.GraphicsPixmapItem(pixmap)
        self.addItem(g_item)
        return g_item

    def add_polygon(
        self,
        polygon: gui.QPolygonF | gui.QPolygon,
        pen: gui.QPen | None = None,
        brush: gui.QBrush | None = None,
    ) -> widgets.GraphicsPolygonItem:
        if isinstance(polygon, gui.QPolygon):
            polygon = gui.PolygonF(polygon)
        g_item = widgets.GraphicsPolygonItem(polygon)
        if brush is not None:
            g_item.setBrush(brush)
        if pen is not None:
            g_item.setPen(pen)
        self.addItem(g_item)
        return g_item

    def add_path(
        self,
        path: gui.QPainterPath,
        pen: gui.QPen | None = None,
        brush: gui.QBrush | None = None,
    ) -> widgets.GraphicsPathItem:
        g_item = widgets.GraphicsPathItem(path)
        if brush is not None:
            g_item.setBrush(brush)
        if pen is not None:
            g_item.setPen(pen)
        self.addItem(g_item)
        return g_item

    def add_rect(
        self,
        rect: datatypes.RectType | datatypes.RectFType,
        pen: gui.QPen | None = None,
        brush: gui.QBrush | None = None,
    ) -> widgets.GraphicsRectItem:
        g_item = widgets.GraphicsRectItem(datatypes.to_rectf(rect))
        if brush is not None:
            g_item.setBrush(brush)
        if pen is not None:
            g_item.setPen(pen)
        self.addItem(g_item)
        return g_item

    def add_line(
        self,
        line: core.QLineF | core.QLine | tuple[float, float, float, float],
        pen: gui.QPen | None = None,
    ) -> widgets.GraphicsLineItem:
        g_item = widgets.GraphicsLineItem(datatypes.to_linef(line))
        if pen is not None:
            g_item.setPen(pen)
        self.addItem(g_item)
        return g_item

    def add_ellipse(
        self,
        ellipse: datatypes.RectType | datatypes.RectFType,
        pen: gui.QPen | None = None,
        brush: gui.QBrush | None = None,
    ) -> widgets.GraphicsEllipseItem:
        g_item = widgets.GraphicsEllipseItem(datatypes.to_rectf(ellipse))
        if brush is not None:
            g_item.setBrush(brush)
        if pen is not None:
            g_item.setPen(pen)
        self.addItem(g_item)
        return g_item

    def add_text(
        self, text: str, font: gui.QFont | None = None
    ) -> widgets.GraphicsTextItem:
        g_item = widgets.GraphicsTextItem(text)
        if font is not None:
            g_item.setFont(font)
        self.addItem(g_item)
        return g_item

    def add_simple_text(
        self, text: str, font: gui.QFont | None = None
    ) -> widgets.GraphicsSimpleTextItem:
        g_item = widgets.GraphicsSimpleTextItem(text)
        if font is not None:
            g_item.setFont(font)
        self.addItem(g_item)
        return g_item

    def add_widget(self, widget: widgets.QWidget) -> widgets.GraphicsProxyWidget:
        g_item = widgets.GraphicsProxyWidget()
        g_item.setWidget(widget)
        self.addItem(g_item)
        return g_item

    def colliding_items(
        self,
        item: widgets.QGraphicsItem,
        mode: constants.ItemSelectionModeStr
        | constants.ItemSelectionMode = "intersects_shape",
    ) -> listdelegators.ListDelegator[widgets.QGraphicsItem]:
        items = self.collidingItems(item, constants.ITEM_SELECTION_MODE[mode])
        return listdelegators.ListDelegator(items)

    def add_item_group(self, *items: widgets.QGraphicsItem) -> widgets.GraphicsItemGroup:
        group = widgets.GraphicsItemGroup()
        for item in items:
            group.addToGroup(item)
        return group

    def _draw_grid(
        self,
        painter: gui.QPainter,
        rect: core.QRectF,
        pen: gui.QPen,
        grid_size: int,
    ):
        left = int(rect.left())
        right = int(rect.right())
        top = int(rect.top())
        bottom = int(rect.bottom())

        first_left = left - (left % grid_size)
        first_top = top - (top % grid_size)

        lines = [
            core.QLineF(x, top, x, bottom) for x in range(first_left, right, grid_size)
        ]
        lines.extend(
            [core.QLineF(left, y, right, y) for y in range(first_top, bottom, grid_size)]
        )

        painter.setPen(pen)
        painter.drawLines(lines)

    def _draw_dots(
        self,
        painter: gui.QPainter,
        rect: core.QRectF,
        pen: gui.QPen,
        grid_size: int,
    ):
        if (zoom := self._get_viewer_zoom()) < 0:
            grid_size *= int(abs(zoom) / 0.3 + 1)

        left = int(rect.left())
        right = int(rect.right())
        top = int(rect.top())
        bottom = int(rect.bottom())

        first_left = left - (left % grid_size)
        first_top = top - (top % grid_size)

        pen.setWidth(grid_size / 10)
        painter.setPen(pen)

        [
            painter.drawPoint(int(x), int(y))
            for x in range(first_left, right, grid_size)
            for y in range(first_top, bottom, grid_size)
        ]

    def drawBackground(self, painter: gui.QPainter, rect: core.QRect):
        super().drawBackground(painter, rect)

        painter.save()
        painter.setRenderHint(gui.QPainter.RenderHint.Antialiasing, False)
        painter.setBrush(self.backgroundBrush())

        if self._grid_mode == self.GridType.DotGrid:
            pen = gui.QPen(self.grid_color, self._pen_width)
            self._draw_dots(painter, rect, pen, self._grid_size)

        elif self._grid_mode == self.GridType.LineGrid:
            zoom = self._get_viewer_zoom()
            if zoom > -0.5:
                pen = gui.QPen(self.grid_color, self._pen_width)
                self._draw_grid(painter, rect, pen, self._grid_size)
            color = self._bg_color.darker(150)
            if zoom < -0.0:
                color = color.darker(100 - int(zoom * 110))
            pen = gui.QPen(color, self._pen_width)
            self._draw_grid(painter, rect, pen, self._grid_size * 8)

        painter.restore()

    def _get_viewer_zoom(self):
        viewer = self.viewer()
        if viewer is None:
            return 1.0
        transform = viewer.transform()
        cur_scale = (transform.m11(), transform.m22())
        return float(f"{cur_scale[0] - 1.0:0.2f}")

    # def mousePressEvent(self, event):
    #     selected = self.viewer().selectedItems()
    #     if viewer := self.viewer():
    #         viewer.sceneMousePressEvent(event)
    #     super().mousePressEvent(event)
    #     keep_selection = any(
    #         [
    #             event.button() == core.Qt.MiddleButton,
    #             event.button() == core.Qt.RightButton,
    #             event.modifiers() == core.Qt.AltModifier,
    #         ]
    #     )
    #     if keep_selection:
    #         for node in selected:
    #             node.setSelected(True)

    # def mouseMoveEvent(self, event):
    #     if viewer := self.viewer():
    #         viewer.sceneMouseMoveEvent(event)
    #     super().mouseMoveEvent(event)

    # def mouseReleaseEvent(self, event):
    #     if viewer := self.viewer():
    #         viewer.sceneMouseReleaseEvent(event)
    #     super().mouseReleaseEvent(event)

    def viewer(self):
        return self.views()[0] if self.views() else None

    def get_grid_mode(self) -> GridType:
        return self._grid_mode

    def set_grid_mode(self, mode: GridType | None = None):
        # alternative?
        # brush = gui.Brush()
        # brush.set_style("cross")
        # scene.setBackgroundBrush(brush)
        if mode is None:
            mode = self.GridType.NoGrid
        self._grid_mode = mode

    def get_grid_color(self) -> gui.Color:
        return self._grid_color

    def set_grid_color(self, color: datatypes.ColorType):
        self._grid_color = colors.get_color(color)

    def get_background_color(self) -> gui.Color:
        return self._bg_color

    def set_background_color(self, color: datatypes.ColorType):
        self._bg_color = colors.get_color(color)
        self.setBackgroundBrush(self._bg_color)

    def set_item_index_method(
        self, method: ItemIndexMethodStr | widgets.QGraphicsScene.ItemIndexMethod
    ):
        """Set item index method.

        Args:
            method: item index method to use
        """
        self.setItemIndexMethod(ITEM_INDEX_METHOD.get_enum_value(method))

    def get_item_index_method(self) -> ItemIndexMethodStr:
        """Return item index method.

        Returns:
            item index method
        """
        return ITEM_INDEX_METHOD.inverse[self.itemIndexMethod()]

    bg_color = core.Property(gui.QColor, get_background_color, set_background_color)
    grid_color = core.Property(gui.QColor, get_grid_color, set_grid_color)
    grid_mode = core.Property(int, get_grid_mode, set_grid_mode)


if __name__ == "__main__":
    app = widgets.app()
    scene = GraphicsScene()
    scene.add_line(core.Line(0, 0, 10, 10))
    view = widgets.GraphicsView(scene)
    view.show()
    app.exec()
