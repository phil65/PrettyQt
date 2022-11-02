"""Constants module."""
from typing import Literal

from bidict import bidict
from prettyqt.qt import QtCore
import prettyqt.qt
from prettyqt.utils import mappers

Qt = QtCore.Qt

if prettyqt.qt.API != "pyqt6":
    ImageConversionFlag = Qt.ImageConversionFlags
else:
    ImageConversionFlag = Qt.ImageConversionFlag  # type: ignore

DISPLAY_ROLE = Qt.ItemDataRole.DisplayRole
USER_ROLE = Qt.ItemDataRole.UserRole
SORT_ROLE = Qt.ItemDataRole.UserRole + 1  # type: ignore
NAME_ROLE = Qt.ItemDataRole.UserRole + 2  # type: ignore
EDIT_ROLE = Qt.ItemDataRole.EditRole
BACKGROUND_ROLE = Qt.ItemDataRole.BackgroundRole
FOREGROUND_ROLE = Qt.ItemDataRole.ForegroundRole
TOOLTIP_ROLE = Qt.ItemDataRole.ToolTipRole
STATUSTIP_ROLE = Qt.ItemDataRole.StatusTipRole
DECORATION_ROLE = Qt.ItemDataRole.DecorationRole
CHECKSTATE_ROLE = Qt.ItemDataRole.CheckStateRole
ALIGNMENT_ROLE = Qt.ItemDataRole.TextAlignmentRole
FONT_ROLE = Qt.ItemDataRole.FontRole

ALIGN_NONE = Qt.AlignmentFlag(0)
ALIGN_LEFT = Qt.AlignmentFlag.AlignLeft
ALIGN_RIGHT = Qt.AlignmentFlag.AlignRight
ALIGN_H_CENTER = Qt.AlignmentFlag.AlignHCenter
ALIGN_JUSTIFY = Qt.AlignmentFlag.AlignJustify

ALIGN_TOP = Qt.AlignmentFlag.AlignTop
ALIGN_BOTTOM = Qt.AlignmentFlag.AlignBottom
ALIGN_V_CENTER = Qt.AlignmentFlag.AlignVCenter
ALIGN_BASELINE = Qt.AlignmentFlag.AlignBaseline

Flag = Qt.AlignmentFlag
ALIGN_CENTER = Flag.AlignCenter
ALIGN_CENTER_LEFT = Flag.AlignVCenter | Flag.AlignLeft  # type: ignore
ALIGN_CENTER_RIGHT = Flag.AlignVCenter | Flag.AlignRight  # type: ignore
ALIGN_TOP_LEFT = Flag.AlignTop | Flag.AlignLeft  # type: ignore
ALIGN_TOP_RIGHT = Flag.AlignTop | Flag.AlignRight  # type: ignore
ALIGN_TOP_CENTER = Flag.AlignTop | Flag.AlignHCenter  # type: ignore
ALIGN_BOTTOM_LEFT = Flag.AlignBottom | Flag.AlignLeft  # type: ignore
ALIGN_BOTTOM_RIGHT = Flag.AlignBottom | Flag.AlignRight  # type: ignore
ALIGN_BOTTOM_CENTER = Flag.AlignBottom | Flag.AlignHCenter  # type: ignore

ORIENTATION_NONE = Qt.Orientation(0)
HORIZONTAL = Qt.Orientation.Horizontal
VERTICAL = Qt.Orientation.Vertical

ASCENDING = Qt.SortOrder.AscendingOrder
DESCENDING = Qt.SortOrder.DescendingOrder

DROP_ENABLED = Qt.ItemFlag.ItemIsDropEnabled
DRAG_ENABLED = Qt.ItemFlag.ItemIsDragEnabled
IS_ENABLED = Qt.ItemFlag.ItemIsEnabled
IS_SELECTABLE = Qt.ItemFlag.ItemIsSelectable
IS_EDITABLE = Qt.ItemFlag.ItemIsEditable
IS_CHECKABLE = Qt.ItemFlag.ItemIsUserCheckable
IS_AUTO_TRISTATE = Qt.ItemFlag.ItemIsAutoTristate
IS_USER_TRISTATE = Qt.ItemFlag.ItemIsUserTristate
NO_FLAGS = Qt.ItemFlag.NoItemFlags
NO_CHILDREN = Qt.ItemFlag.ItemNeverHasChildren

MOVE_ACTION = Qt.DropAction.MoveAction
COPY_ACTION = Qt.DropAction.CopyAction

TEXT_WORD_WRAP = Qt.TextFlag.TextWordWrap

CTRL_MOD = Qt.KeyboardModifier.ControlModifier

KEY_F11 = Qt.Key.Key_F11
KEY_DELETE = Qt.Key.Key_Delete


ThemeStr = Literal["default", "dark"]

ITEM_DATA_ROLE = bidict(
    display=DISPLAY_ROLE,
    user=USER_ROLE,
    sort=SORT_ROLE,
    edit=EDIT_ROLE,
    tooltip=TOOLTIP_ROLE,
    statustip=STATUSTIP_ROLE,
    decoration=DECORATION_ROLE,
    checkstate=CHECKSTATE_ROLE,
    alignment=ALIGNMENT_ROLE,
    font=FONT_ROLE,
    foreground=FOREGROUND_ROLE,
    background=BACKGROUND_ROLE,
)

ItemDataRoleStr = Literal[
    "display",
    "user",
    "sort",
    "edit",
    "tooltip",
    "statustip",
    "decoration",
    "checkstate",
    "alignment",
    "font",
    "foreground",
    "background",
]

ALIGNMENTS = mappers.FlagMap(
    Qt.AlignmentFlag,
    # none=int(Qt.Alignment(0)),
    left=ALIGN_LEFT,
    right=ALIGN_RIGHT,
    top=ALIGN_TOP,
    bottom=ALIGN_BOTTOM,
    top_left=ALIGN_TOP_LEFT,
    top_right=ALIGN_TOP_RIGHT,
    bottom_left=ALIGN_BOTTOM_LEFT,
    bottom_right=ALIGN_BOTTOM_RIGHT,
    center=ALIGN_CENTER,
)

AlignmentStr = Literal[
    "top",
    "left",
    "right",
    "bottom",
    "top_left",
    "top_right",
    "bottom_left",
    "bottom_right",
]

SIDES = mappers.FlagMap(
    Qt.AlignmentFlag,
    left=Qt.AlignmentFlag.AlignLeft,
    right=Qt.AlignmentFlag.AlignRight,
    top=Qt.AlignmentFlag.AlignTop,
    bottom=Qt.AlignmentFlag.AlignBottom,
)

SideStr = Literal["left", "right", "top", "bottom"]

EDGES = mappers.FlagMap(
    Qt.Edge,
    top=Qt.Edge.TopEdge,
    left=Qt.Edge.LeftEdge,
    right=Qt.Edge.RightEdge,
    bottom=Qt.Edge.BottomEdge,
    top_left=Qt.Edge.TopEdge | Qt.Edge.LeftEdge,  # type: ignore
    top_right=Qt.Edge.TopEdge | Qt.Edge.RightEdge,  # type: ignore
    bottom_left=Qt.Edge.BottomEdge | Qt.Edge.LeftEdge,  # type: ignore
    bottom_right=Qt.Edge.BottomEdge | Qt.Edge.RightEdge,  # type: ignore
)

EdgeStr = Literal[
    "top",
    "left",
    "right",
    "bottom",
    "top_left",
    "top_right",
    "bottom_left",
    "bottom_right",
]

H_ALIGNMENT = mappers.FlagMap(
    Qt.AlignmentFlag,
    left=Qt.AlignmentFlag.AlignLeft,
    right=Qt.AlignmentFlag.AlignRight,
    center=Qt.AlignmentFlag.AlignHCenter,
    justify=Qt.AlignmentFlag.AlignJustify,
)

HorizontalAlignmentStr = Literal[
    "left",
    "right",
    "center",
    "justify",
]

V_ALIGNMENT = mappers.FlagMap(
    Qt.AlignmentFlag,
    top=Qt.AlignmentFlag.AlignTop,
    bottom=Qt.AlignmentFlag.AlignBottom,
    center=Qt.AlignmentFlag.AlignVCenter,
    baseline=Qt.AlignmentFlag.AlignBaseline,
)

VerticalAlignmentStr = Literal[
    "top",
    "bottom",
    "center",
    "baseline",
]

MODIFIER_TO_KEY = {
    QtCore.Qt.KeyboardModifier.ShiftModifier: QtCore.Qt.Modifier.SHIFT,
    QtCore.Qt.KeyboardModifier.ControlModifier: QtCore.Qt.Modifier.CTRL,
    QtCore.Qt.KeyboardModifier.AltModifier: QtCore.Qt.Modifier.ALT,
    QtCore.Qt.KeyboardModifier.MetaModifier: QtCore.Qt.Modifier.META,
}

KeyboardmodifierStr = Literal[
    "none", "shift", "ctrl", "alt", "meta", "keypad", "group_switch"
]
KEYBOARD_MODIFIERS: bidict[KeyboardmodifierStr, Qt.KeyboardModifier] = bidict(
    none=Qt.KeyboardModifier.NoModifier,
    shift=Qt.KeyboardModifier.ShiftModifier,
    ctrl=Qt.KeyboardModifier.ControlModifier,
    alt=Qt.KeyboardModifier.AltModifier,
    meta=Qt.KeyboardModifier.MetaModifier,
    keypad=Qt.KeyboardModifier.KeypadModifier,
    group_switch=Qt.KeyboardModifier.GroupSwitchModifier,
)

OrientationStr = Literal["horizontal", "vertical"]
ORIENTATION: bidict[OrientationStr, Qt.Orientation] = bidict(
    horizontal=Qt.Orientation.Horizontal, vertical=Qt.Orientation.Vertical
)

StateStr = Literal["unchecked", "partial", "checked"]
STATE: bidict[StateStr, Qt.CheckState] = bidict(
    unchecked=Qt.CheckState.Unchecked,
    partial=Qt.CheckState.PartiallyChecked,
    checked=Qt.CheckState.Checked,
)

MATCH_FLAGS = dict(
    exact=Qt.MatchFlag.MatchExactly,
    fixed_string=Qt.MatchFlag.MatchFixedString,
    contains=Qt.MatchFlag.MatchContains,
    starts_with=Qt.MatchFlag.MatchStartsWith,
    ends_with=Qt.MatchFlag.MatchEndsWith,
    case_sensitive=Qt.MatchFlag.MatchCaseSensitive,
    regex=Qt.MatchFlag.MatchRegularExpression,
    wildcard=Qt.MatchFlag.MatchWildcard,
    wrap=Qt.MatchFlag.MatchWrap,
    recursive=Qt.MatchFlag.MatchRecursive,
)

MatchFlagStr = Literal[
    "exact",
    "fixed_string",
    "contains",
    "starts_with",
    "ends_with",
    "case_sensitive",
    "regex",
    "wildcard",
    "wrap",
    "recursive",
]

ImageConversionFlagStr = Literal[
    "auto",
    "color_only",
    "mono_only",
    # "diffuse_dither",
    "ordered_dither",
    "threshold_dither",
    # "threshold_alpha_dither",
    "ordered_alpha_dither",
    "diffuse_alpha_filter",
    "prefer_dither",
    "avoid_dither",
    # "auto_dither",
    "no_opaque_detection",
    "no_format_conversion",
]
IMAGE_CONVERSION_FLAGS: bidict[ImageConversionFlagStr, Qt.ImageConversionFlag] = bidict(
    # Color/Mono preference (ignored for QBitmap):
    auto=Qt.ImageConversionFlag.AutoColor,
    color_only=Qt.ImageConversionFlag.ColorOnly,
    mono_only=Qt.ImageConversionFlag.MonoOnly,
    # Dithering mode preference:
    # diffuse_dither=Qt.ImageConversionFlag.DiffuseDither,
    ordered_dither=Qt.ImageConversionFlag.OrderedDither,
    threshold_dither=Qt.ImageConversionFlag.ThresholdDither,
    # Dithering mode preference for 1-bit alpha masks:
    # threshold_alpha_dither=Qt.ImageConversionFlag.ThresholdAlphaDither,
    ordered_alpha_dither=Qt.ImageConversionFlag.OrderedAlphaDither,
    diffuse_alpha_filter=Qt.ImageConversionFlag.DiffuseAlphaDither,
    # Color matching versus dithering preference:
    prefer_dither=Qt.ImageConversionFlag.PreferDither,
    avoid_dither=Qt.ImageConversionFlag.AvoidDither,
    # auto_dither=Qt.ImageConversionFlag.AutoDither,
    no_opaque_detection=Qt.ImageConversionFlag.NoOpaqueDetection,
    no_format_conversion=Qt.ImageConversionFlag.NoFormatConversion,
)

FilterModeStr = Literal["starts_with", "contains", "ends_with"]
FILTER_MODES = mappers.FlagMap(
    Qt.MatchFlag,
    starts_with=Qt.MatchFlag.MatchStartsWith,
    contains=Qt.MatchFlag.MatchContains,
    ends_with=Qt.MatchFlag.MatchEndsWith,
)

DropActionStr = Literal["copy", "move", "link", "action_mask", "ignore", "target_move"]
DROP_ACTION: bidict[DropActionStr, Qt.DropAction] = bidict(
    copy=Qt.DropAction.CopyAction,
    move=Qt.DropAction.MoveAction,
    link=Qt.DropAction.LinkAction,
    action_mask=Qt.DropAction.ActionMask,
    ignore=Qt.DropAction.IgnoreAction,
    target_move=Qt.DropAction.TargetMoveAction,
)

DockPositionStr = Literal["top", "bottom", "left", "right"]
DOCK_POSITION: bidict[DockPositionStr, Qt.DockWidgetArea] = bidict(
    top=Qt.DockWidgetArea.TopDockWidgetArea,
    bottom=Qt.DockWidgetArea.BottomDockWidgetArea,
    left=Qt.DockWidgetArea.LeftDockWidgetArea,
    right=Qt.DockWidgetArea.RightDockWidgetArea,
)

DockPositionsStr = Literal["top", "bottom", "left", "right", "all"]
DOCK_POSITIONS: bidict[DockPositionsStr, Qt.DockWidgetArea] = bidict(
    top=Qt.DockWidgetArea.TopDockWidgetArea,
    bottom=Qt.DockWidgetArea.BottomDockWidgetArea,
    left=Qt.DockWidgetArea.LeftDockWidgetArea,
    right=Qt.DockWidgetArea.RightDockWidgetArea,
    all=Qt.DockWidgetArea.AllDockWidgetAreas,
)

ToolbarAreaStr = Literal["top", "bottom", "left", "right", "all", "none"]
TOOLBAR_AREA: bidict[ToolbarAreaStr, Qt.ToolBarArea] = bidict(
    left=Qt.ToolBarArea.LeftToolBarArea,
    right=Qt.ToolBarArea.RightToolBarArea,
    top=Qt.ToolBarArea.TopToolBarArea,
    bottom=Qt.ToolBarArea.BottomToolBarArea,
    all=Qt.ToolBarArea.AllToolBarAreas,
    none=Qt.ToolBarArea.NoToolBarArea,
)

ToolButtonStyleStr = Literal["icon", "text", "text_beside_icon", "text_below_icon"]
TOOLBUTTON_STYLE: bidict[ToolButtonStyleStr, Qt.ToolButtonStyle] = bidict(
    icon=Qt.ToolButtonStyle.ToolButtonIconOnly,
    text=Qt.ToolButtonStyle.ToolButtonTextOnly,
    text_beside_icon=Qt.ToolButtonStyle.ToolButtonTextBesideIcon,
    text_below_icon=Qt.ToolButtonStyle.ToolButtonTextUnderIcon,
)

WindowFrameSectionStr = Literal["none", "text", "text_beside_icon", "text_below_icon"]
WINDOW_FRAME_SECTION: bidict[WindowFrameSectionStr, Qt.WindowFrameSection] = bidict(
    none=Qt.WindowFrameSection.NoSection,
    left=Qt.WindowFrameSection.LeftSection,
    top_left=Qt.WindowFrameSection.TopLeftSection,
    top=Qt.WindowFrameSection.TopSection,
    top_right=Qt.WindowFrameSection.TopRightSection,
    right=Qt.WindowFrameSection.RightSection,
    bottom_right=Qt.WindowFrameSection.BottomRightSection,
    bottom=Qt.WindowFrameSection.BottomSection,
    bottom_left=Qt.WindowFrameSection.BottomLeftSection,
    title_bar=Qt.WindowFrameSection.TitleBarArea,
)

ArrowTypeStr = Literal["none", "up", "down", "left", "right"]
ARROW_TYPE: bidict[ArrowTypeStr, Qt.ArrowType] = bidict(
    none=Qt.ArrowType.NoArrow,
    up=Qt.ArrowType.UpArrow,
    down=Qt.ArrowType.DownArrow,
    left=Qt.ArrowType.LeftArrow,
    right=Qt.ArrowType.RightArrow,
)

EventPriorityStr = Literal["high", "normal", "low"]

# using int instead of Qt.EventPriority here
EVENT_PRIORITY: bidict[EventPriorityStr, int] = bidict(
    high=1,  # HighEventPriority
    normal=0,  # NormalEventPriority
    low=-1,  # LowEventPriority
)

CursorShapeStr = Literal[
    "arrow",
    "uparrow",
    "cross",
    "wait",
    "caret",
    "size_vertical",
    "size_horizontal",
    "size_topright",
    "size_topleft",
    "size_all",
    "blank",
    "split_vertical",
    "split_horizontal",
    "pointing_hand",
    "forbidden",
    "open_hand",
    "closed_hand",
    "whats_this",
    "busy",
    "drag_move",
    "drag_copy",
    "drag_link",
    "bitmap",
]
CURSOR_SHAPE: bidict[CursorShapeStr, Qt.CursorShape] = bidict(
    arrow=Qt.CursorShape.ArrowCursor,
    uparrow=Qt.CursorShape.UpArrowCursor,
    cross=Qt.CursorShape.CrossCursor,
    wait=Qt.CursorShape.WaitCursor,
    caret=Qt.CursorShape.IBeamCursor,
    size_vertical=Qt.CursorShape.SizeVerCursor,
    size_horizontal=Qt.CursorShape.SizeHorCursor,
    size_topright=Qt.CursorShape.SizeBDiagCursor,
    size_topleft=Qt.CursorShape.SizeFDiagCursor,
    size_all=Qt.CursorShape.SizeAllCursor,
    blank=Qt.CursorShape.BlankCursor,
    split_vertical=Qt.CursorShape.SplitVCursor,
    split_horizontal=Qt.CursorShape.SplitHCursor,
    pointing_hand=Qt.CursorShape.PointingHandCursor,
    forbidden=Qt.CursorShape.ForbiddenCursor,
    open_hand=Qt.CursorShape.OpenHandCursor,
    closed_hand=Qt.CursorShape.ClosedHandCursor,
    whats_this=Qt.CursorShape.WhatsThisCursor,
    busy=Qt.CursorShape.BusyCursor,
    drag_move=Qt.CursorShape.DragMoveCursor,
    drag_copy=Qt.CursorShape.DragCopyCursor,
    drag_link=Qt.CursorShape.DragLinkCursor,
    bitmap=Qt.CursorShape.BitmapCursor,
)

LayoutDirectionStr = Literal["left_to_right", "right_to_left", "auto"]
LAYOUT_DIRECTION: bidict[LayoutDirectionStr, Qt.LayoutDirection] = bidict(
    left_to_right=Qt.LayoutDirection.LeftToRight,
    right_to_left=Qt.LayoutDirection.RightToLeft,
    auto=Qt.LayoutDirection.LayoutDirectionAuto,
)

ApplicationStateStr = Literal["suspended", "hidden", "inactive", "active"]
APPLICATION_STATES: bidict[ApplicationStateStr, Qt.ApplicationState] = bidict(
    suspended=Qt.ApplicationState.ApplicationSuspended,
    hidden=Qt.ApplicationState.ApplicationHidden,
    inactive=Qt.ApplicationState.ApplicationInactive,
    active=Qt.ApplicationState.ApplicationActive,
)

HighDpiScaleFactorRoundingPolicyStr = Literal[
    "round", "ceil", "floor", "round_prefer_floor", "pass_through"
]
HIGH_DPI_SCALE_FACTOR_ROUNDING_POLICY: bidict[
    HighDpiScaleFactorRoundingPolicyStr, Qt.HighDpiScaleFactorRoundingPolicy
] = bidict(
    round=Qt.HighDpiScaleFactorRoundingPolicy.Round,
    ceil=Qt.HighDpiScaleFactorRoundingPolicy.Ceil,
    floor=Qt.HighDpiScaleFactorRoundingPolicy.Floor,
    round_prefer_floor=Qt.HighDpiScaleFactorRoundingPolicy.RoundPreferFloor,
    pass_through=Qt.HighDpiScaleFactorRoundingPolicy.PassThrough,
)

UiEffectStr = Literal[
    "animate_menu",
    "fade_menu",
    "animate_combo",
    "animate_tooltip",
    "fade_tooltip",
    "animate_toolbox",
]
UI_EFFECTS: bidict[UiEffectStr, Qt.UIEffect] = bidict(
    animate_menu=Qt.UIEffect.UI_AnimateMenu,
    fade_menu=Qt.UIEffect.UI_FadeMenu,
    animate_combo=Qt.UIEffect.UI_AnimateCombo,
    animate_tooltip=Qt.UIEffect.UI_AnimateTooltip,
    fade_tooltip=Qt.UIEffect.UI_FadeTooltip,
    animate_toolbox=Qt.UIEffect.UI_AnimateToolBox,
)

NavigationModeStr = Literal[
    "none",
    "keypad_tab_order",
    "keypad_directional",
    "cursor_auto",
    "cursor_force_visible",
]
NAVIGATION_MODES: bidict[NavigationModeStr, Qt.NavigationMode] = bidict(
    none=Qt.NavigationMode.NavigationModeNone,
    keypad_tab_order=Qt.NavigationMode.NavigationModeKeypadTabOrder,
    keypad_directional=Qt.NavigationMode.NavigationModeKeypadDirectional,
    cursor_auto=Qt.NavigationMode.NavigationModeCursorAuto,
    cursor_force_visible=Qt.NavigationMode.NavigationModeCursorForceVisible,
)

ItemSelectionModeStr = Literal[
    "contains_shape",
    "intersects_shape",
    "contains_bounding_rect",
    "intersects_bounding_rect",
]
ITEM_SELECTION_MODE: bidict[ItemSelectionModeStr, Qt.ItemSelectionMode] = bidict(
    contains_shape=Qt.ItemSelectionMode.ContainsItemShape,
    intersects_shape=Qt.ItemSelectionMode.IntersectsItemShape,
    contains_bounding_rect=Qt.ItemSelectionMode.ContainsItemBoundingRect,
    intersects_bounding_rect=Qt.ItemSelectionMode.IntersectsItemBoundingRect,
)

FocusReasonStr = Literal[
    "mouse", "tab", "backtab", "active_window", "popup", "shortcut", "menu_bar", "other"
]
FOCUS_REASONS: bidict[FocusReasonStr, Qt.FocusReason] = bidict(
    mouse=Qt.FocusReason.MouseFocusReason,
    tab=Qt.FocusReason.TabFocusReason,
    backtab=Qt.FocusReason.BacktabFocusReason,
    active_window=Qt.FocusReason.ActiveWindowFocusReason,
    popup=Qt.FocusReason.PopupFocusReason,
    shortcut=Qt.FocusReason.ShortcutFocusReason,
    menu_bar=Qt.FocusReason.MenuBarFocusReason,
    other=Qt.FocusReason.OtherFocusReason,
)

ElideModeStr = Literal["left", "right", "middle", "none"]
ELIDE_MODE: bidict[ElideModeStr, Qt.TextElideMode] = bidict(
    left=Qt.TextElideMode.ElideLeft,
    right=Qt.TextElideMode.ElideRight,
    middle=Qt.TextElideMode.ElideMiddle,
    none=Qt.TextElideMode.ElideNone,
)

PenStyleStr = Literal[
    "none", "solid", "dash", "dot", "dash_dot", "dash_dot_dot", "custom_dash"
]
PEN_STYLE: bidict[PenStyleStr, Qt.PenStyle] = bidict(
    none=Qt.PenStyle.NoPen,
    solid=Qt.PenStyle.SolidLine,
    dash=Qt.PenStyle.DashLine,
    dot=Qt.PenStyle.DotLine,
    dash_dot=Qt.PenStyle.DashDotLine,
    dash_dot_dot=Qt.PenStyle.DashDotDotLine,
    custom_dash=Qt.PenStyle.CustomDashLine,
)

CapStyleStr = Literal["flat", "square", "round"]
CAP_STYLE: bidict[CapStyleStr, Qt.PenCapStyle] = bidict(
    flat=Qt.PenCapStyle.FlatCap,
    square=Qt.PenCapStyle.SquareCap,
    round=Qt.PenCapStyle.RoundCap,
)

JoinStyleStr = Literal["miter", "bevel", "round" "svg_miter"]
JOIN_STYLE: bidict[JoinStyleStr, Qt.PenJoinStyle] = bidict(
    miter=Qt.PenJoinStyle.MiterJoin,
    bevel=Qt.PenJoinStyle.BevelJoin,
    round=Qt.PenJoinStyle.RoundJoin,
    svg_miter=Qt.PenJoinStyle.SvgMiterJoin,
)

PatternStr = Literal[
    "none",
    "solid",
    "dense_1",
    "dense_2",
    "dense_3",
    "dense_4",
    "dense_5",
    "dense_6",
    "dense_7",
    "horizontal",
    "vertical",
    "cross",
    "backward_diagonal",
    "forward_diagonal",
    "crossing_diagonal",
    "linear_gradient",
    "conical_gradient",
    "radial_gradient",
    "texture",
]

PATTERN: bidict[PatternStr, Qt.BrushStyle] = bidict(
    none=Qt.BrushStyle.NoBrush,
    solid=Qt.BrushStyle.SolidPattern,
    dense_1=Qt.BrushStyle.Dense1Pattern,
    dense_2=Qt.BrushStyle.Dense2Pattern,
    dense_3=Qt.BrushStyle.Dense3Pattern,
    dense_4=Qt.BrushStyle.Dense4Pattern,
    dense_5=Qt.BrushStyle.Dense5Pattern,
    dense_6=Qt.BrushStyle.Dense6Pattern,
    dense_7=Qt.BrushStyle.Dense7Pattern,
    horizontal=Qt.BrushStyle.HorPattern,
    vertical=Qt.BrushStyle.VerPattern,
    cross=Qt.BrushStyle.CrossPattern,
    backward_diagonal=Qt.BrushStyle.BDiagPattern,
    forward_diagonal=Qt.BrushStyle.FDiagPattern,
    crossing_diagonal=Qt.BrushStyle.DiagCrossPattern,
    linear_gradient=Qt.BrushStyle.LinearGradientPattern,
    conical_gradient=Qt.BrushStyle.ConicalGradientPattern,
    radial_gradient=Qt.BrushStyle.RadialGradientPattern,
    texture=Qt.BrushStyle.TexturePattern,
)

ClipOperationStr = Literal["none", "replace", "intersect"]
CLIP_OPERATION: bidict[ClipOperationStr, Qt.ClipOperation] = bidict(
    none=Qt.ClipOperation.NoClip,
    replace=Qt.ClipOperation.ReplaceClip,
    intersect=Qt.ClipOperation.IntersectClip,
)

ContextStr = Literal["widget", "widget_with_children", "window", "application"]
CONTEXT: bidict[ContextStr, Qt.ShortcutContext] = bidict(
    widget=Qt.ShortcutContext.WidgetShortcut,
    widget_with_children=Qt.ShortcutContext.WidgetWithChildrenShortcut,
    window=Qt.ShortcutContext.WindowShortcut,
    application=Qt.ShortcutContext.ApplicationShortcut,
)

TileRuleStr = Literal["stretch", "repeat", "round"]
TILE_RULE: bidict[TileRuleStr, Qt.TileRule] = bidict(
    stretch=Qt.TileRule.StretchTile,
    repeat=Qt.TileRule.RepeatTile,
    round=Qt.TileRule.RoundTile,
)

TransformationModeStr = Literal["fast", "smooth"]
TRANSFORMATION_MODE: bidict[TransformationModeStr, Qt.TransformationMode] = bidict(
    fast=Qt.TransformationMode.FastTransformation,
    smooth=Qt.TransformationMode.SmoothTransformation,
)

GestureTypeStr = Literal["tap", "tap_and_hold", "pan", "pinch", "swipe", "custom"]
GESTURE_TYPE: bidict[GestureTypeStr, Qt.GestureType] = bidict(
    tap=Qt.GestureType.TapGesture,
    tap_and_hold=Qt.GestureType.TapAndHoldGesture,
    pan=Qt.GestureType.PanGesture,
    pinch=Qt.GestureType.PinchGesture,
    swipe=Qt.GestureType.SwipeGesture,
    custom=Qt.GestureType.CustomGesture,
)

GestureStateStr = Literal["none", "started", "updated", "finished", "canceled"]
GESTURE_STATE: bidict[GestureStateStr, Qt.GestureState] = bidict(
    none=Qt.GestureState(0),  # GestureNone not available in PyQt6
    started=Qt.GestureState.GestureStarted,
    updated=Qt.GestureState.GestureUpdated,
    finished=Qt.GestureState.GestureFinished,
    canceled=Qt.GestureState.GestureCanceled,
)


ScrollBarPolicyStr = Literal["always_on", "always_off", "as_needed"]
SCROLLBAR_POLICY: bidict[ScrollBarPolicyStr, Qt.ScrollBarPolicy] = bidict(
    always_on=Qt.ScrollBarPolicy.ScrollBarAlwaysOn,
    always_off=Qt.ScrollBarPolicy.ScrollBarAlwaysOff,
    as_needed=Qt.ScrollBarPolicy.ScrollBarAsNeeded,
)

ContextPolicyStr = Literal["none", "prevent", "default", "actions", "custom"]
CONTEXT_POLICY: bidict[ContextPolicyStr, Qt.ContextMenuPolicy] = bidict(
    none=Qt.ContextMenuPolicy.NoContextMenu,
    prevent=Qt.ContextMenuPolicy.PreventContextMenu,
    default=Qt.ContextMenuPolicy.DefaultContextMenu,
    actions=Qt.ContextMenuPolicy.ActionsContextMenu,
    custom=Qt.ContextMenuPolicy.CustomContextMenu,
    # showhide_menu="showhide_menu",
)

ModalityStr = Literal["window", "application", "none"]
MODALITY: bidict[ModalityStr, Qt.WindowModality] = bidict(
    window=Qt.WindowModality.WindowModal,
    application=Qt.WindowModality.ApplicationModal,
    none=Qt.WindowModality.NonModal,
)

FocusPolicyStr = Literal["tab", "click", "strong", "wheel", "none"]
FOCUS_POLICY: bidict[FocusPolicyStr, Qt.FocusPolicy] = bidict(
    tab=Qt.FocusPolicy.TabFocus,
    click=Qt.FocusPolicy.ClickFocus,
    strong=Qt.FocusPolicy.StrongFocus,
    wheel=Qt.FocusPolicy.WheelFocus,
    none=Qt.FocusPolicy.NoFocus,
)

WindowFlagStr = Literal[
    "frameless", "popup", "stay_on_top", "tool", "window_title", "customize_window"
]

WINDOW_FLAGS: bidict[WindowFlagStr, Qt.WindowType] = bidict(
    frameless=Qt.WindowType.FramelessWindowHint,
    popup=Qt.WindowType.Popup,
    stay_on_top=Qt.WindowType.WindowStaysOnTopHint,
    tool=Qt.WindowType.Tool,
    window_title=Qt.WindowType.WindowTitleHint,
    customize_window=Qt.WindowType.CustomizeWindowHint,
)

WindowStateStr = Literal["none", "minimized", "maximized", "fullscreen", "active"]
WINDOW_STATES = mappers.FlagMap(
    Qt.WindowState,
    none=Qt.WindowState.WindowNoState,
    minimized=Qt.WindowState.WindowMinimized,
    maximized=Qt.WindowState.WindowMaximized,
    fullscreen=Qt.WindowState.WindowFullScreen,
    active=Qt.WindowState.WindowActive,
)

FillRuleStr = Literal["odd_even", "winding"]
FILL_RULE: bidict[FillRuleStr, Qt.FillRule] = bidict(
    odd_even=Qt.FillRule.OddEvenFill, winding=Qt.FillRule.WindingFill
)

TimerTypeStr = Literal["precise", "coarse", "very_coarse"]
TIMER_TYPE: bidict[TimerTypeStr, Qt.TimerType] = bidict(
    precise=Qt.TimerType.PreciseTimer,
    coarse=Qt.TimerType.CoarseTimer,
    very_coarse=Qt.TimerType.VeryCoarseTimer,
)

CursorMoveStyleStr = Literal["logical", "visual"]
CURSOR_MOVE_STYLE: bidict[CursorMoveStyleStr, Qt.CursorMoveStyle] = bidict(
    logical=Qt.CursorMoveStyle.LogicalMoveStyle,
    visual=Qt.CursorMoveStyle.VisualMoveStyle,
)

CornerStr = Literal["top_left", "top_right", "bottom_left", "bottom_right"]
CORNER: bidict[CornerStr, Qt.Corner] = bidict(
    top_left=Qt.Corner.TopLeftCorner,
    top_right=Qt.Corner.TopRightCorner,
    bottom_left=Qt.Corner.BottomLeftCorner,
    bottom_right=Qt.Corner.BottomRightCorner,
)

ScreenOrientationStr = Literal[
    "primary", "landscape", "portrait", "inverted_landscape", "inverted_portrait"
]
SCREEN_ORIENTATION: bidict[ScreenOrientationStr, Qt.ScreenOrientation] = bidict(
    primary=Qt.ScreenOrientation.PrimaryOrientation,
    landscape=Qt.ScreenOrientation.LandscapeOrientation,
    portrait=Qt.ScreenOrientation.PortraitOrientation,
    inverted_landscape=Qt.ScreenOrientation.InvertedLandscapeOrientation,
    inverted_portrait=Qt.ScreenOrientation.InvertedPortraitOrientation,
)

AspectRatioModeStr = Literal["ignore", "keep", "keep_by_expanding"]
ASPECT_RATIO_MODE: bidict[AspectRatioModeStr, Qt.AspectRatioMode] = bidict(
    ignore=Qt.AspectRatioMode.IgnoreAspectRatio,
    keep=Qt.AspectRatioMode.KeepAspectRatio,
    keep_by_expanding=Qt.AspectRatioMode.KeepAspectRatioByExpanding,
)

DateFormatStr = Literal["text", "iso", "iso_with_ms", "rfc_2822"]
DATE_FORMAT: bidict[DateFormatStr, Qt.DateFormat] = bidict(
    text=Qt.DateFormat.TextDate,
    iso=Qt.DateFormat.ISODate,
    iso_with_ms=Qt.DateFormat.ISODateWithMs,
    rfc_2822=Qt.DateFormat.RFC2822Date,
)

TimeSpecStr = Literal["local_time", "utc", "offset_from_utc", "timezone"]
TIME_SPEC: bidict[TimeSpecStr, Qt.TimeSpec] = bidict(
    local_time=Qt.TimeSpec.LocalTime,
    utc=Qt.TimeSpec.UTC,
    offset_from_utc=Qt.TimeSpec.OffsetFromUTC,
    timezone=Qt.TimeSpec.TimeZone,
)

AxisStr = Literal["x", "y", "z"]
AXIS: bidict[AxisStr, Qt.Axis] = bidict(x=Qt.Axis.XAxis, y=Qt.Axis.YAxis, z=Qt.Axis.ZAxis)

WidgetAttributeStr = Literal[
    "accept_drops",
    "always_show_tooltips",
    "custom_whats_this",
    "delete_on_close",
    "disabled",
    "dont_show_on_screen",
    "force_disabled",
    "force_updates_disabled",
    "hover",
    "input_method_enabled",
    "keyboard_focus_change",
    "key_compression",
    "layout_on_entire_rect",
    "layout_uses_widget_rect",
    "mac_opaque_size_grip",
    "mac_show_focus_rect",
    "mac_normal_size",
    "mac_small_size",
    "mac_mini_size",
    # "mac_variable_size",
    "mapped",
    "mouse_no_mask",
    "mouse_tracking",
    "moved",
    "no_child_events_for_parent",
    "no_child_events_from_children",
    "no_mouse_replay",
    "no_mouse_propagation",
    "transparent_for_mouse_events",
    "no_system_background",
    "opaque_paint_event",
    "outside_ws_range",
    "paint_on_screen",
    "paint_unclipped",
    "pending_move_event",
    "pending_resize_egent",
    "quit_on_close",
    "resized",
    "right_to_left",
    "set_cursor",
    "set_font",
    "set_palette",
    "set_style",
    "show_modal",
    "static_contents",
    "style_sheet",
    "style_sheet_target",
    "tablet_tracking",
    "translucent_background",
    "under_mouse",
    "updates_disabled",
    "window_modified",
    "window_propagation",
    "mac_always_show_tool_window",
    "set_locale",
    "styled_background",
    "show_without_activating",
    "native_window",
    "dont_create_native_ancestors",
    "x11_net_wm_window_type_desktop",
    "x11_net_wm_window_type_dock",
    "x11_net_wm_window_type_toolbar",
    "x11_net_wm_window_type_menu",
    "x11_net_wm_window_type_utility",
    "x11_net_wm_window_type_splash",
    "x11_net_wm_window_type_dialog",
    "x11_net_wm_window_type_dropdown_menu",
    "x11_net_wm_window_type_popup_menu",
    "x11_net_wm_window_type_tooltip",
    "x11_net_wm_window_type_notification",
    "x11_net_wm_window_type_combo",
    "x11_net_wm_window_type_dnd",
    "accept_touch_events",
    "touch_pad_single_touch_events",
    "x11_do_not_accept_focus",
    "always_stack_on_top",
    "contents_margins_respects_safe_area",
]
Attr = Qt.WidgetAttribute
WIDGET_ATTRIBUTE: bidict[WidgetAttributeStr, Qt.WidgetAttribute] = bidict(
    accept_drops=Attr.WA_AcceptDrops,
    always_show_tooltips=Attr.WA_AlwaysShowToolTips,
    custom_whats_this=Attr.WA_CustomWhatsThis,
    delete_on_close=Attr.WA_DeleteOnClose,
    disabled=Attr.WA_Disabled,
    dont_show_on_screen=Attr.WA_DontShowOnScreen,
    force_disabled=Attr.WA_ForceDisabled,
    force_updates_disabled=Attr.WA_ForceUpdatesDisabled,
    hover=Attr.WA_Hover,
    input_method_enabled=Attr.WA_InputMethodEnabled,
    keyboard_focus_change=Attr.WA_KeyboardFocusChange,
    key_compression=Attr.WA_KeyCompression,
    layout_on_entire_rect=Attr.WA_LayoutOnEntireRect,
    layout_uses_widget_rect=Attr.WA_LayoutUsesWidgetRect,
    mac_opaque_size_grip=Attr.WA_MacOpaqueSizeGrip,
    mac_show_focus_rect=Attr.WA_MacShowFocusRect,
    mac_normal_size=Attr.WA_MacNormalSize,
    mac_small_size=Attr.WA_MacSmallSize,
    mac_mini_size=Attr.WA_MacMiniSize,
    # mac_variable_size=Attr.WA_MacVariableSize,
    mapped=Attr.WA_Mapped,
    mouse_no_mask=Attr.WA_MouseNoMask,
    mouse_tracking=Attr.WA_MouseTracking,
    moved=Attr.WA_Moved,
    no_child_events_for_parent=Attr.WA_NoChildEventsForParent,
    no_child_events_from_children=Attr.WA_NoChildEventsFromChildren,
    no_mouse_replay=Attr.WA_NoMouseReplay,
    no_mouse_propagation=Attr.WA_NoMousePropagation,
    transparent_for_mouse_events=Attr.WA_TransparentForMouseEvents,
    no_system_background=Attr.WA_NoSystemBackground,
    opaque_paint_event=Attr.WA_OpaquePaintEvent,
    outside_ws_range=Attr.WA_OutsideWSRange,
    paint_on_screen=Attr.WA_PaintOnScreen,
    paint_unclipped=Attr.WA_PaintUnclipped,
    pending_move_event=Attr.WA_PendingMoveEvent,
    pending_resize_egent=Attr.WA_PendingResizeEvent,
    quit_on_close=Attr.WA_QuitOnClose,
    resized=Attr.WA_Resized,
    right_to_left=Attr.WA_RightToLeft,
    set_cursor=Attr.WA_SetCursor,
    set_font=Attr.WA_SetFont,
    set_palette=Attr.WA_SetPalette,
    set_style=Attr.WA_SetStyle,
    # show_modal=Attr.WA_ShowModal,
    static_contents=Attr.WA_StaticContents,
    style_sheet=Attr.WA_StyleSheet,
    style_sheet_target=Attr.WA_StyleSheetTarget,
    tablet_tracking=Attr.WA_TabletTracking,
    translucent_background=Attr.WA_TranslucentBackground,
    under_mouse=Attr.WA_UnderMouse,
    updates_disabled=Attr.WA_UpdatesDisabled,
    window_modified=Attr.WA_WindowModified,
    window_propagation=Attr.WA_WindowPropagation,
    mac_always_show_tool_window=Attr.WA_MacAlwaysShowToolWindow,
    set_locale=Attr.WA_SetLocale,
    styled_background=Attr.WA_StyledBackground,
    show_without_activating=Attr.WA_ShowWithoutActivating,
    native_window=Attr.WA_NativeWindow,
    dont_create_native_ancestors=Attr.WA_DontCreateNativeAncestors,
    x11_net_wm_window_type_desktop=Attr.WA_X11NetWmWindowTypeDesktop,
    x11_net_wm_window_type_dock=Attr.WA_X11NetWmWindowTypeDock,
    x11_net_wm_window_type_toolbar=Attr.WA_X11NetWmWindowTypeToolBar,
    x11_net_wm_window_type_menu=Attr.WA_X11NetWmWindowTypeMenu,
    x11_net_wm_window_type_utility=Attr.WA_X11NetWmWindowTypeUtility,
    x11_net_wm_window_type_splash=Attr.WA_X11NetWmWindowTypeSplash,
    x11_net_wm_window_type_dialog=Attr.WA_X11NetWmWindowTypeDialog,
    x11_net_wm_window_type_dropdown_menu=Attr.WA_X11NetWmWindowTypeDropDownMenu,
    x11_net_wm_window_type_popup_menu=Attr.WA_X11NetWmWindowTypePopupMenu,
    x11_net_wm_window_type_tooltip=Attr.WA_X11NetWmWindowTypeToolTip,
    x11_net_wm_window_type_notification=Attr.WA_X11NetWmWindowTypeNotification,
    x11_net_wm_window_type_combo=Attr.WA_X11NetWmWindowTypeCombo,
    x11_net_wm_window_type_dnd=Attr.WA_X11NetWmWindowTypeDND,
    accept_touch_events=Attr.WA_AcceptTouchEvents,
    touch_pad_single_touch_events=Attr.WA_TouchPadAcceptSingleTouchEvents,
    x11_do_not_accept_focus=Attr.WA_X11DoNotAcceptFocus,
    always_stack_on_top=Attr.WA_AlwaysStackOnTop,
    contents_margins_respects_safe_area=Attr.WA_ContentsMarginsRespectsSafeArea,
)

ApplicationAttributeStr = Literal[
    "dont_show_icons_in_menus",
    "dont_show_shortcuts_in_context_menus",
    "native_windows",
    "dont_create_native_widget_siblings",
    "plugin_application",
    "dont_use_native_menu_bar",
    "mac_dont_swap_ctrl_and_meta",
    "use_96_dpi",
    "synthesize_touch_for_mouse_events",
    "synthesize_touch_for_touch_events",
    "use_high_dpi_pixmaps",
    "force_raster_widgets",
    "use_desktop_open_gl",
    "use_open_gl_es",
    "use_software_open_gl",
    "share_open_gl_contexts",
    "set_palette",
    "enable_high_dpi_scaling",
    "disable_high_dpi_scaling",
    "use_style_sheet_propagation_in_styles",
    "dont_use_native_dialogs",
    "synthesize_mouse_for_tablet_events",
    "compress_tablet_events",
    "dont_check_open_gl_context_thread",
    "disable_shader_disk_cache",
    "disable_window_context_help_button",
    "disable_session_manager",
    "disable_native_virtual_keyboard",
]

Att = Qt.ApplicationAttribute

APPLICATION_ATTRIBUTE: bidict[ApplicationAttributeStr, Qt.ApplicationAttribute] = bidict(
    dont_show_icons_in_menus=Att.AA_DontShowIconsInMenus,
    dont_show_shortcuts_in_context_menus=Att.AA_DontShowShortcutsInContextMenus,
    native_windows=Att.AA_NativeWindows,
    dont_create_native_widget_siblings=Att.AA_DontCreateNativeWidgetSiblings,
    plugin_application=Att.AA_PluginApplication,
    dont_use_native_menu_bar=Att.AA_DontUseNativeMenuBar,
    mac_dont_swap_ctrl_and_meta=Att.AA_MacDontSwapCtrlAndMeta,
    use_96_dpi=Att.AA_Use96Dpi,
    synthesize_touch_for_mouse_events=Att.AA_SynthesizeTouchForUnhandledMouseEvents,
    synthesize_touch_for_touch_events=Att.AA_SynthesizeMouseForUnhandledTouchEvents,
    # use_high_dpi_pixmaps=Att.AA_UseHighDpiPixmaps, # not available on PyQt6
    force_raster_widgets=Att.AA_ForceRasterWidgets,
    use_desktop_open_gl=Att.AA_UseDesktopOpenGL,
    use_open_gl_es=Att.AA_UseOpenGLES,
    use_software_open_gl=Att.AA_UseSoftwareOpenGL,
    share_open_gl_contexts=Att.AA_ShareOpenGLContexts,
    set_palette=Att.AA_SetPalette,
    # enable_high_dpi_scaling=Att.AA_EnableHighDpiScaling, # not available on PyQt6
    # disable_high_dpi_scaling=Att.AA_DisableHighDpiScaling, # not available on PyQt6
    use_style_sheet_propagation_in_styles=Att.AA_UseStyleSheetPropagationInWidgetStyles,
    dont_use_native_dialogs=Att.AA_DontUseNativeDialogs,
    synthesize_mouse_for_tablet_events=Att.AA_SynthesizeMouseForUnhandledTabletEvents,
    compress_tablet_events=Att.AA_CompressTabletEvents,
    dont_check_open_gl_context_thread=Att.AA_DontCheckOpenGLContextThreadAffinity,
    disable_shader_disk_cache=Att.AA_DisableShaderDiskCache,
    # disable_window_context_help_button=Att.AA_DisableWindowContextHelpButton,
    disable_session_manager=Att.AA_DisableSessionManager,
    disable_native_virtual_keyboard=Att.AA_DisableNativeVirtualKeyboard,
)
