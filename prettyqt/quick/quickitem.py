from typing import Literal

from qtpy import QtQuick

from prettyqt import core, gui, qml
from prettyqt.utils import InvalidParamError, bidict


FLAGS = bidict(
    clips_children_to_shape=QtQuick.QQuickItem.ItemClipsChildrenToShape,
    accepts_input_method=QtQuick.QQuickItem.ItemAcceptsInputMethod,
    is_focus_scope=QtQuick.QQuickItem.ItemIsFocusScope,
    has_contents=QtQuick.QQuickItem.ItemHasContents,
    accepts_drops=QtQuick.QQuickItem.ItemAcceptsDrops,
)

FlagStr = Literal[
    "clips_children_to_shape",
    "accepts_input_method",
    "is_focus_scope",
    "has_contents",
    "accepts_drops",
]

ITEM_CHANGE = bidict(
    child_added_change=QtQuick.QQuickItem.ItemChildAddedChange,
    child_removed_change=QtQuick.QQuickItem.ItemChildRemovedChange,
    item_scene_change=QtQuick.QQuickItem.ItemSceneChange,
    visible_has_changed=QtQuick.QQuickItem.ItemVisibleHasChanged,
    parent_has_changed=QtQuick.QQuickItem.ItemParentHasChanged,
    opacity_has_changed=QtQuick.QQuickItem.ItemOpacityHasChanged,
    active_focus_has_changed=QtQuick.QQuickItem.ItemActiveFocusHasChanged,
    rotation_has_changed=QtQuick.QQuickItem.ItemRotationHasChanged,
    pixel_ratio_has_changed=QtQuick.QQuickItem.ItemDevicePixelRatioHasChanged,
    anti_aliasing_has_changed=QtQuick.QQuickItem.ItemAntialiasingHasChanged,
    enabled_has_changed=QtQuick.QQuickItem.ItemEnabledHasChanged,
)

ItemChangeStr = Literal[
    "child_added_change",
    "child_removed_change",
    "item_scene_change",
    "visible_has_changed",
    "parent_has_changed",
    "opacity_has_changed",
    "active_focus_has_changed",
    "rotation_has_changed",
    "pixel_ratio_has_changed",
    "anti_aliasing_has_changed",
    "enabled_has_changed",
]

TRANSFORM_ORIGIN = bidict(
    top_left=QtQuick.QQuickItem.TopLeft,
    top=QtQuick.QQuickItem.Top,
    top_right=QtQuick.QQuickItem.TopRight,
    left=QtQuick.QQuickItem.Left,
    center=QtQuick.QQuickItem.Center,
    right=QtQuick.QQuickItem.Right,
    bottom_left=QtQuick.QQuickItem.BottomLeft,
    bottom=QtQuick.QQuickItem.Bottom,
    bottom_right=QtQuick.QQuickItem.BottomRight,
)

TransformOriginStr = Literal[
    "top_left",
    "top",
    "top_right",
    "left",
    "center",
    "right",
    "bottom_left",
    "bottom",
    "bottom_right",
]

QtQuick.QQuickItem.__bases__ = (core.Object, qml.QmlParserStatus)


class QuickItem(QtQuick.QQuickItem):
    def get_children_rect(self) -> core.RectF:
        return core.RectF(self.childrenRect())

    def get_cursor(self) -> gui.Cursor:
        return gui.Cursor(self.cursor())

    def get_flags(self):
        pass

    def set_transform_origin(self, origin: TransformOriginStr):
        """Set the origin point around which scale and rotation transform.

        The default is "center".

        Args:
            origin: transform origin to use

        Raises:
            InvalidParamError: transform origin does not exist
        """
        if origin not in TRANSFORM_ORIGIN:
            raise InvalidParamError(origin, TRANSFORM_ORIGIN)
        self.setTransformOrigin(TRANSFORM_ORIGIN[origin])

    def get_transform_origin(self) -> TransformOriginStr:
        """Return the render type of text-like elements in Qt Quick.

        Returns:
            transform origin
        """
        return TRANSFORM_ORIGIN.inverse[self.transformOrigin()]


if __name__ == "__main__":
    item = QuickItem()
