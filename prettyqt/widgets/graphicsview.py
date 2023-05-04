from __future__ import annotations

from typing import Literal

from prettyqt import constants, core, gui, widgets
from prettyqt.qt import QtCore, QtWidgets
from prettyqt.utils import InvalidParamError, bidict, datatypes, helpers


mod = QtWidgets.QGraphicsView

DRAG_MODE = bidict(
    none=mod.DragMode.NoDrag,
    scroll_hand=mod.DragMode.ScrollHandDrag,
    rubber_band=mod.DragMode.RubberBandDrag,
)

DragModeStr = Literal["none", "scroll_hand", "rubber_band"]

CACHE_MODES = bidict(
    none=mod.CacheModeFlag.CacheNone,
    background=mod.CacheModeFlag.CacheBackground,
)

CacheModeStr = Literal["none", "background"]

OPTIMIZATION_FLAGS = bidict(
    # dont_clip_painter=mod.OptimizationFlag.DontClipPainter,
    dont_save_painter_state=mod.OptimizationFlag.DontSavePainterState,
    dont_adjust_for_antialiasing=mod.OptimizationFlag.DontAdjustForAntialiasing,
)

OptimizationFlagStr = Literal["dont_save_painter_state", "dont_adjust_for_antialiasing"]

VIEWPORT_ANCHOR = bidict(
    none=mod.ViewportAnchor.NoAnchor,
    view_center=mod.ViewportAnchor.AnchorViewCenter,
    under_mouse=mod.ViewportAnchor.AnchorUnderMouse,
)

ViewportAnchorStr = Literal["none", "view_center", "under_mouse"]

VIEWPORT_UPDATE_MODE = bidict(
    full=mod.ViewportUpdateMode.FullViewportUpdate,
    minimal=mod.ViewportUpdateMode.MinimalViewportUpdate,
    smart=mod.ViewportUpdateMode.SmartViewportUpdate,
    bounding_rect=mod.ViewportUpdateMode.BoundingRectViewportUpdate,
    none=mod.ViewportUpdateMode.NoViewportUpdate,
)

ViewportUpdateModeStr = Literal["full", "minimal", "smart", "bounding_rect", "none"]


class GraphicsViewMixin(widgets.AbstractScrollAreaMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not args or not isinstance(args[0], QtWidgets.QGraphicsScene):
            self.setScene(widgets.GraphicsScene())

    def enable_mousewheel_zoom(self, state: bool = True):
        if state:
            self.viewport().installEventFilter(self)
        else:
            self.viewport().removeEventFilter(self)

    def __getitem__(self, index: int) -> QtWidgets.QGraphicsItem:
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

    def get_view_rect(self) -> QtCore.QRect:
        """Return the boundaries of the view in scene coordinates."""
        r = QtCore.QRectF(self.rect())
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
        self, rect: QtCore.QRectF, layer: widgets.graphicsscene.SceneLayerStr = "all"
    ):
        if layer not in widgets.graphicsscene.SCENE_LAYER:
            raise InvalidParamError(layer, widgets.graphicsscene.SCENE_LAYER)
        self.invalidateScene(rect, widgets.graphicsscene.SCENE_LAYER[layer])

    def set_transformation_anchor(self, mode: ViewportAnchorStr):
        """Set how the view should position the scene during transformations.

        Args:
            mode: transformation anchor to use

        Raises:
            InvalidParamError: mode does not exist
        """
        if mode not in VIEWPORT_ANCHOR:
            raise InvalidParamError(mode, VIEWPORT_ANCHOR)
        self.setTransformationAnchor(VIEWPORT_ANCHOR[mode])

    def get_transformation_anchor(self) -> ViewportAnchorStr:
        """Return current transformation anchor.

        Returns:
            viewport anchor
        """
        return VIEWPORT_ANCHOR.inverse[self.transformationAnchor()]

    def set_transform(self, transform: datatypes.TransformType, combine: bool = False):
        if isinstance(transform, tuple):
            transform = gui.Transform(*transform)
        self.setTransform(transform, combine)

    def set_resize_anchor(self, mode: ViewportAnchorStr):
        """Set how the view should position the scene during resizes.

        Args:
            mode: resize anchor to use

        Raises:
            InvalidParamError: mode does not exist
        """
        if mode not in VIEWPORT_ANCHOR:
            raise InvalidParamError(mode, VIEWPORT_ANCHOR)
        self.setResizeAnchor(VIEWPORT_ANCHOR[mode])

    def get_resize_anchor(self) -> ViewportAnchorStr:
        """Return current resize anchor.

        Returns:
            resize anchor
        """
        return VIEWPORT_ANCHOR.inverse[self.resizeAnchor()]

    def set_viewport_update_mode(self, mode: ViewportUpdateModeStr):
        """Set how the viewport should update its contents.

        Args:
            mode: viewport update mode to use

        Raises:
            InvalidParamError: mode does not exist
        """
        if mode not in VIEWPORT_UPDATE_MODE:
            raise InvalidParamError(mode, VIEWPORT_UPDATE_MODE)
        self.setViewportUpdateMode(VIEWPORT_UPDATE_MODE[mode])

    def get_viewport_update_mode(self) -> ViewportUpdateModeStr:
        """Return current viewport update mode.

        Returns:
            viewport update mode
        """
        return VIEWPORT_UPDATE_MODE.inverse[self.viewportUpdateMode()]

    def set_drag_mode(self, mode: DragModeStr):
        """Set the behavior for dragging the mouse while the left mouse button is pressed.

        Args:
            mode: drag mode to use

        Raises:
            InvalidParamError: mode does not exist
        """
        if mode not in DRAG_MODE:
            raise InvalidParamError(mode, DRAG_MODE)
        self.setDragMode(DRAG_MODE[mode])

    def get_drag_mode(self) -> DragModeStr:
        """Return current drag mode.

        Returns:
            drag mode
        """
        return DRAG_MODE.inverse[self.dragMode()]

    def set_rubberband_selection_mode(self, mode: constants.ItemSelectionModeStr):
        """Set the behavior for selecting items with a rubber band selection rectangle.

        Args:
            mode: rubberband selection mode to use

        Raises:
            InvalidParamError: mode does not exist
        """
        if mode not in constants.ITEM_SELECTION_MODE:
            raise InvalidParamError(mode, constants.ITEM_SELECTION_MODE)
        self.setRubberBandSelectionMode(constants.ITEM_SELECTION_MODE[mode])

    def get_rubberband_selection_mode(self) -> constants.ItemSelectionModeStr:
        """Return current rubberband selection mode.

        Returns:
            rubberband selection mode
        """
        return constants.ITEM_SELECTION_MODE.inverse[self.rubberBandSelectionMode()]

    def set_cache_mode(self, mode: CacheModeStr):
        """Set the cache mode.

        Args:
            mode: cache mode to use

        Raises:
            InvalidParamError: mode does not exist
        """
        if mode not in CACHE_MODES:
            raise InvalidParamError(mode, CACHE_MODES)
        self.setCacheMode(CACHE_MODES[mode])

    def get_cache_mode(self) -> CacheModeStr:
        """Return current cache mode.

        Returns:
            cache mode
        """
        return CACHE_MODES.inverse[self.cacheMode()]

    def set_optimization_flags(self, *items: OptimizationFlagStr):
        for item in items:
            if item not in OPTIMIZATION_FLAGS:
                raise InvalidParamError(item, OPTIMIZATION_FLAGS)
        flags = helpers.merge_flags(items, OPTIMIZATION_FLAGS)
        self.setOptimizationFlags(flags)

    def get_optimization_flags(self) -> list[OptimizationFlagStr]:
        return OPTIMIZATION_FLAGS.get_list(self.optimizationFlags())


class GraphicsView(GraphicsViewMixin, QtWidgets.QGraphicsView):
    pass


if __name__ == "__main__":
    app = widgets.app()
    view = GraphicsView()
    scene = widgets.GraphicsScene()
    scene.add_line(core.Line(0, 0, 200, 100))
    view.setScene(scene)
    view.show()
    app.main_loop()
