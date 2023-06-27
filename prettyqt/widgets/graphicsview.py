from __future__ import annotations

from typing import Literal

from prettyqt import constants, core, gui, widgets
from prettyqt.utils import bidict, datatypes


mod = widgets.QGraphicsView


DragModeStr = Literal["none", "scroll_hand", "rubber_band"]

DRAG_MODE: bidict[DragModeStr, mod.DragMode] = bidict(
    none=mod.DragMode.NoDrag,
    scroll_hand=mod.DragMode.ScrollHandDrag,
    rubber_band=mod.DragMode.RubberBandDrag,
)

CacheModeStr = Literal["none", "background"]

CACHE_MODES: bidict[CacheModeStr, mod.CacheModeFlag] = bidict(
    none=mod.CacheModeFlag.CacheNone,
    background=mod.CacheModeFlag.CacheBackground,
)

OptimizationFlagStr = Literal["dont_save_painter_state", "dont_adjust_for_antialiasing"]

OPTIMIZATION_FLAGS: bidict[OptimizationFlagStr, mod.OptimizationFlag] = bidict(
    # dont_clip_painter=mod.OptimizationFlag.DontClipPainter,
    dont_save_painter_state=mod.OptimizationFlag.DontSavePainterState,
    dont_adjust_for_antialiasing=mod.OptimizationFlag.DontAdjustForAntialiasing,
)

ViewportAnchorStr = Literal["none", "view_center", "under_mouse"]

VIEWPORT_ANCHOR: bidict[ViewportAnchorStr, mod.ViewportAnchor] = bidict(
    none=mod.ViewportAnchor.NoAnchor,
    view_center=mod.ViewportAnchor.AnchorViewCenter,
    under_mouse=mod.ViewportAnchor.AnchorUnderMouse,
)

ViewportUpdateModeStr = Literal["full", "minimal", "smart", "bounding_rect", "none"]

VIEWPORT_UPDATE_MODE: bidict[ViewportUpdateModeStr, mod.ViewportUpdateMode] = bidict(
    full=mod.ViewportUpdateMode.FullViewportUpdate,
    minimal=mod.ViewportUpdateMode.MinimalViewportUpdate,
    smart=mod.ViewportUpdateMode.SmartViewportUpdate,
    bounding_rect=mod.ViewportUpdateMode.BoundingRectViewportUpdate,
    none=mod.ViewportUpdateMode.NoViewportUpdate,
)


class GraphicsViewMixin(widgets.AbstractScrollAreaMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not args or not isinstance(args[0], widgets.QGraphicsScene):
            self.setScene(widgets.GraphicsScene())

    def _get_map(self):
        maps = super()._get_map()
        maps |= {
            "alignment": constants.ALIGNMENTS,
            "resizeAnchor": VIEWPORT_ANCHOR,
            "transformationAnchor": VIEWPORT_ANCHOR,
            "cacheMode": CACHE_MODES,
            "dragMode": DRAG_MODE,
            "viewportUpdateMode": VIEWPORT_UPDATE_MODE,
            "rubberBandSelectionMode": constants.ITEM_SELECTION_MODE,
            "renderHints": gui.painter.RENDER_HINTS,
            "optimizationFlags": OPTIMIZATION_FLAGS,
        }
        return maps

    def enable_mousewheel_zoom(self, state: bool = True):
        if state:
            self.viewport().installEventFilter(self)
        else:
            self.viewport().removeEventFilter(self)

    def __getitem__(self, index: int) -> widgets.QGraphicsItem:
        return self.items()[index]

    def eventFilter(self, source, event) -> bool:
        if source is not self.viewport() or event.type() != event.Type.Wheel:
            return super().eventFilter(source, event)
        # Zoom Factor
        zoom_in_factor = 1.25
        zoom_out_factor = 1 / zoom_in_factor

        # Set Anchors
        self.setTransformationAnchor(self.ViewportAnchor.NoAnchor)
        self.setResizeAnchor(self.ViewportAnchor.NoAnchor)

        # Save the scene pos
        old_pos = self.mapToScene(event.position().toPoint())

        # Zoom
        zoom_factor = zoom_in_factor if event.angleDelta().y() > 0 else zoom_out_factor
        self.scale(zoom_factor, zoom_factor)

        # # Get the new position
        new_pos = self.mapToScene(event.position().toPoint())

        # Move scene to old position
        delta = new_pos - old_pos
        self.translate(delta.x(), delta.y())
        return True

    def get_zoom(self) -> float:
        """Return the viewer zoom level.

        Returns:
            float: zoom level.
        """
        transform = self.transform()
        cur_scale = (transform.m11(), transform.m22())
        return float(f"{cur_scale[0] - 1.0:0.2f}")

    def add_item(self, *args):
        return self.scene().addItem(*args)

    def remove_item(self, *args):
        return self.scene().removeItem(*args)

    def get_view_rect(self) -> core.QRect:
        """Return the boundaries of the view in scene coordinates."""
        r = core.QRectF(self.rect())
        return self.viewportTransform().inverted()[0].mapRect(r)

    def get_pixel_size(self):
        """Return vector with length and width of one view pixel in scene coordinates."""
        p0 = core.PointF(0, 0)
        p1 = core.PointF(1, 1)
        tr = self.transform().inverted()[0]
        p01 = tr.map(p0)
        p11 = tr.map(p1)
        return core.PointF(p11 - p01)

    def get_background_brush(self) -> gui.Brush:
        return gui.Brush(self.backgroundBrush())

    def get_foreground_brush(self) -> gui.Brush:
        return gui.Brush(self.foregroundBrush())

    def invalidate_scene(
        self,
        rect: core.QRectF,
        layer: widgets.graphicsscene.SceneLayerStr
        | widgets.QGraphicsScene.SceneLayer = "all",
    ):
        self.invalidateScene(
            rect, widgets.graphicsscene.SCENE_LAYER.get_enum_value(layer)
        )

    def set_transformation_anchor(self, mode: ViewportAnchorStr | mod.ViewportAnchor):
        """Set how the view should position the scene during transformations.

        Args:
            mode: transformation anchor to use
        """
        self.setTransformationAnchor(VIEWPORT_ANCHOR.get_enum_value(mode))

    def get_transformation_anchor(self) -> ViewportAnchorStr:
        """Return current transformation anchor.

        Returns:
            viewport anchor
        """
        return VIEWPORT_ANCHOR.inverse[self.transformationAnchor()]

    def set_transform(self, transform: datatypes.TransformType, combine: bool = False):
        self.setTransform(datatypes.to_transform(transform), combine)

    def set_resize_anchor(self, mode: ViewportAnchorStr | mod.ViewportAnchor):
        """Set how the view should position the scene during resizes.

        Args:
            mode: resize anchor to use
        """
        self.setResizeAnchor(VIEWPORT_ANCHOR.get_enum_value(mode))

    def get_resize_anchor(self) -> ViewportAnchorStr:
        """Return current resize anchor.

        Returns:
            resize anchor
        """
        return VIEWPORT_ANCHOR.inverse[self.resizeAnchor()]

    def set_viewport_update_mode(
        self, mode: ViewportUpdateModeStr | mod.ViewportUpdateMode
    ):
        """Set how the viewport should update its contents.

        Args:
            mode: viewport update mode to use
        """
        self.setViewportUpdateMode(VIEWPORT_UPDATE_MODE.get_enum_value(mode))

    def get_viewport_update_mode(self) -> ViewportUpdateModeStr:
        """Return current viewport update mode.

        Returns:
            viewport update mode
        """
        return VIEWPORT_UPDATE_MODE.inverse[self.viewportUpdateMode()]

    def set_drag_mode(self, mode: DragModeStr | mod.DragMode):
        """Set the behavior for dragging the mouse while the left mouse button is pressed.

        Args:
            mode: drag mode to use
        """
        self.setDragMode(DRAG_MODE.get_enum_value(mode))

    def get_drag_mode(self) -> DragModeStr:
        """Return current drag mode.

        Returns:
            drag mode
        """
        return DRAG_MODE.inverse[self.dragMode()]

    def set_rubberband_selection_mode(
        self, mode: constants.ItemSelectionModeStr | constants.ItemSelectionMode
    ):
        """Set the behavior for selecting items with a rubber band selection rectangle.

        Args:
            mode: rubberband selection mode to use
        """
        self.setRubberBandSelectionMode(
            constants.ITEM_SELECTION_MODE.get_enum_value(mode)
        )

    def get_rubberband_selection_mode(self) -> constants.ItemSelectionModeStr:
        """Return current rubberband selection mode.

        Returns:
            rubberband selection mode
        """
        return constants.ITEM_SELECTION_MODE.inverse[self.rubberBandSelectionMode()]

    def set_cache_mode(self, mode: CacheModeStr | mod.CacheModeFlag):
        """Set the cache mode.

        Args:
            mode: cache mode to use
        """
        self.setCacheMode(CACHE_MODES.get_enum_value(mode))

    def get_cache_mode(self) -> CacheModeStr:
        """Return current cache mode.

        Returns:
            cache mode
        """
        return CACHE_MODES.inverse[self.cacheMode()]

    def set_optimization_flags(self, *items: OptimizationFlagStr):
        flags = OPTIMIZATION_FLAGS.merge_flags(items)
        self.setOptimizationFlags(flags)

    def get_optimization_flags(self) -> list[OptimizationFlagStr]:
        return OPTIMIZATION_FLAGS.get_list(self.optimizationFlags())


class GraphicsView(GraphicsViewMixin, widgets.QGraphicsView):
    pass


if __name__ == "__main__":
    app = widgets.app()
    view = GraphicsView()
    scene = widgets.GraphicsScene()
    scene.add_line(core.Line(0, 0, 200, 100))
    view.setScene(scene)
    view.show()
    app.exec()
