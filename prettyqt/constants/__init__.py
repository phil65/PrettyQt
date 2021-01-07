"""Constants module."""
from typing import Literal

from bidict import bidict
from prettyqt.qt import QtCore

from prettyqt.utils import mappers


DISPLAY_ROLE = QtCore.Qt.DisplayRole
USER_ROLE = QtCore.Qt.UserRole
SORT_ROLE = QtCore.Qt.UserRole + 1
NAME_ROLE = QtCore.Qt.UserRole + 2
EDIT_ROLE = QtCore.Qt.EditRole
BACKGROUND_ROLE = QtCore.Qt.BackgroundRole
FOREGROUND_ROLE = QtCore.Qt.ForegroundRole
TOOLTIP_ROLE = QtCore.Qt.ToolTipRole
STATUSTIP_ROLE = QtCore.Qt.StatusTipRole
DECORATION_ROLE = QtCore.Qt.DecorationRole
CHECKSTATE_ROLE = QtCore.Qt.CheckStateRole
ALIGNMENT_ROLE = QtCore.Qt.TextAlignmentRole
FONT_ROLE = QtCore.Qt.FontRole

ALIGN_LEFT = QtCore.Qt.AlignLeft
ALIGN_RIGHT = QtCore.Qt.AlignRight
ALIGN_H_CENTER = QtCore.Qt.AlignHCenter
ALIGN_JUSTIFY = QtCore.Qt.AlignJustify

ALIGN_TOP = QtCore.Qt.AlignTop
ALIGN_BOTTOM = QtCore.Qt.AlignBottom
ALIGN_V_CENTER = QtCore.Qt.AlignVCenter
ALIGN_BASELINE = QtCore.Qt.AlignBaseline

ALIGN_CENTER = QtCore.Qt.AlignCenter
ALIGN_CENTER_LEFT = QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft
ALIGN_CENTER_RIGHT = QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight
ALIGN_TOP_LEFT = QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft
ALIGN_TOP_RIGHT = QtCore.Qt.AlignTop | QtCore.Qt.AlignRight
ALIGN_TOP_CENTER = QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter
ALIGN_BOTTOM_LEFT = QtCore.Qt.AlignBottom | QtCore.Qt.AlignLeft
ALIGN_BOTTOM_RIGHT = QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight
ALIGN_BOTTOM_CENTER = QtCore.Qt.AlignBottom | QtCore.Qt.AlignHCenter

HORIZONTAL = QtCore.Qt.Horizontal
VERTICAL = QtCore.Qt.Vertical

ASCENDING = QtCore.Qt.AscendingOrder
DESCENDING = QtCore.Qt.DescendingOrder

DROP_ENABLED = QtCore.Qt.ItemIsDropEnabled
DRAG_ENABLED = QtCore.Qt.ItemIsDragEnabled
IS_ENABLED = QtCore.Qt.ItemIsEnabled
IS_SELECTABLE = QtCore.Qt.ItemIsSelectable
IS_EDITABLE = QtCore.Qt.ItemIsEditable
IS_CHECKABLE = QtCore.Qt.ItemIsUserCheckable
IS_AUTO_TRISTATE = QtCore.Qt.ItemIsAutoTristate
IS_USER_TRISTATE = QtCore.Qt.ItemIsUserTristate
NO_FLAGS = QtCore.Qt.NoItemFlags
NO_CHILDREN = QtCore.Qt.ItemNeverHasChildren

MOVE_ACTION = QtCore.Qt.MoveAction
COPY_ACTION = QtCore.Qt.CopyAction

TEXT_WORD_WRAP = QtCore.Qt.TextWordWrap

CTRL_MOD = QtCore.Qt.ControlModifier

KEY_F11 = QtCore.Qt.Key_F11
KEY_DELETE = QtCore.Qt.Key_Delete


ALIGNMENTS = mappers.FlagMap(
    QtCore.Qt.Alignment,
    # none=int(QtCore.Qt.Alignment(0)),
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
    QtCore.Qt.Alignment,
    left=QtCore.Qt.AlignLeft,
    right=QtCore.Qt.AlignRight,
    top=QtCore.Qt.AlignTop,
    bottom=QtCore.Qt.AlignBottom,
)

SideStr = Literal["left", "right", "top", "bottom"]

EDGES = mappers.FlagMap(
    QtCore.Qt.Edges,
    top=QtCore.Qt.TopEdge,
    left=QtCore.Qt.LeftEdge,
    right=QtCore.Qt.RightEdge,
    bottom=QtCore.Qt.BottomEdge,
    top_left=QtCore.Qt.TopEdge | QtCore.Qt.LeftEdge,
    top_right=QtCore.Qt.TopEdge | QtCore.Qt.RightEdge,
    bottom_left=QtCore.Qt.BottomEdge | QtCore.Qt.LeftEdge,
    bottom_right=QtCore.Qt.BottomEdge | QtCore.Qt.RightEdge,
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
    QtCore.Qt.Alignment,
    left=QtCore.Qt.AlignLeft,
    right=QtCore.Qt.AlignRight,
    center=QtCore.Qt.AlignHCenter,
    justify=QtCore.Qt.AlignJustify,
)

HorizontalAlignmentStr = Literal[
    "left",
    "right",
    "center",
    "justify",
]

V_ALIGNMENT = mappers.FlagMap(
    QtCore.Qt.Alignment,
    top=QtCore.Qt.AlignTop,
    bottom=QtCore.Qt.AlignBottom,
    center=QtCore.Qt.AlignVCenter,
    baseline=QtCore.Qt.AlignBaseline,
)

VerticalAlignmentStr = Literal[
    "top",
    "bottom",
    "center",
    "baseline",
]

OrientationStr = Literal["horizontal", "vertical"]
ORIENTATION: bidict[OrientationStr, QtCore.Qt.Orientation] = bidict(
    horizontal=QtCore.Qt.Horizontal, vertical=QtCore.Qt.Vertical
)

StateStr = Literal["unchecked", "partial", "checked"]
STATE: bidict[StateStr, QtCore.Qt.CheckState] = bidict(
    unchecked=QtCore.Qt.Unchecked,
    partial=QtCore.Qt.PartiallyChecked,
    checked=QtCore.Qt.Checked,
)

MATCH_FLAGS = dict(
    exact=QtCore.Qt.MatchExactly,
    fixed_string=QtCore.Qt.MatchFixedString,
    contains=QtCore.Qt.MatchContains,
    starts_with=QtCore.Qt.MatchStartsWith,
    ends_with=QtCore.Qt.MatchEndsWith,
    case_sensitive=QtCore.Qt.MatchCaseSensitive,
    regex=QtCore.Qt.MatchRegularExpression,
    wildcard=QtCore.Qt.MatchWildcard,
    wrap=QtCore.Qt.MatchWrap,
    recursive=QtCore.Qt.MatchRecursive,
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

FilterModeStr = Literal["starts_with", "contains", "ends_with"]
FILTER_MODES = mappers.FlagMap(
    QtCore.Qt.MatchFlags,
    starts_with=QtCore.Qt.MatchStartsWith,
    contains=QtCore.Qt.MatchContains,
    ends_with=QtCore.Qt.MatchEndsWith,
)

DropActionStr = Literal["copy", "move", "link", "action_mask", "ignore", "target_move"]
DROP_ACTION: bidict[DropActionStr, QtCore.Qt.DropAction] = bidict(
    copy=QtCore.Qt.CopyAction,
    move=QtCore.Qt.MoveAction,
    link=QtCore.Qt.LinkAction,
    action_mask=QtCore.Qt.ActionMask,
    ignore=QtCore.Qt.IgnoreAction,
    target_move=QtCore.Qt.TargetMoveAction,
)

DockPositionStr = Literal["top", "bottom", "left", "right"]
DOCK_POSITION: bidict[DockPositionStr, QtCore.Qt.DockWidgetArea] = bidict(
    top=QtCore.Qt.TopDockWidgetArea,
    bottom=QtCore.Qt.BottomDockWidgetArea,
    left=QtCore.Qt.LeftDockWidgetArea,
    right=QtCore.Qt.RightDockWidgetArea,
)

DockPositionsStr = Literal["top", "bottom", "left", "right", "all"]
DOCK_POSITIONS: bidict[DockPositionsStr, QtCore.Qt.DockWidgetAreas] = bidict(
    top=QtCore.Qt.TopDockWidgetArea,
    bottom=QtCore.Qt.BottomDockWidgetArea,
    left=QtCore.Qt.LeftDockWidgetArea,
    right=QtCore.Qt.RightDockWidgetArea,
    all=QtCore.Qt.AllDockWidgetAreas,
)

ToolbarAreaStr = Literal["top", "bottom", "left", "right", "all", "none"]
TOOLBAR_AREA: bidict[ToolbarAreaStr, QtCore.Qt.ToolBarArea] = bidict(
    left=QtCore.Qt.LeftToolBarArea,
    right=QtCore.Qt.RightToolBarArea,
    top=QtCore.Qt.TopToolBarArea,
    bottom=QtCore.Qt.BottomToolBarArea,
    all=QtCore.Qt.AllToolBarAreas,
    none=QtCore.Qt.NoToolBarArea,
)

ToolButtonStyleStr = Literal["icon", "text", "text_beside_icon", "text_below_icon"]
TOOLBUTTON_STYLE: bidict[ToolButtonStyleStr, QtCore.Qt.ToolButtonStyle] = bidict(
    icon=QtCore.Qt.ToolButtonIconOnly,
    text=QtCore.Qt.ToolButtonTextOnly,
    text_beside_icon=QtCore.Qt.ToolButtonTextBesideIcon,
    text_below_icon=QtCore.Qt.ToolButtonTextUnderIcon,
)

WindowFrameSectionStr = Literal["none", "text", "text_beside_icon", "text_below_icon"]
WINDOW_FRAME_SECTION: bidict[
    WindowFrameSectionStr, QtCore.Qt.WindowFrameSection
] = bidict(
    none=QtCore.Qt.NoSection,
    left=QtCore.Qt.LeftSection,
    top_left=QtCore.Qt.TopLeftSection,
    top=QtCore.Qt.TopSection,
    top_right=QtCore.Qt.TopRightSection,
    right=QtCore.Qt.RightSection,
    bottom_right=QtCore.Qt.BottomRightSection,
    bottom=QtCore.Qt.BottomSection,
    bottom_left=QtCore.Qt.BottomLeftSection,
    title_bar=QtCore.Qt.TitleBarArea,
)

ArrowTypeStr = Literal["none", "up", "down", "left", "right"]
ARROW_TYPE: bidict[ArrowTypeStr, QtCore.Qt.ArrowType] = bidict(
    none=QtCore.Qt.NoArrow,
    up=QtCore.Qt.UpArrow,
    down=QtCore.Qt.DownArrow,
    left=QtCore.Qt.LeftArrow,
    right=QtCore.Qt.RightArrow,
)

EventPriorityStr = Literal["high", "normal", "low"]

# using int instead of QtCore.Qt.EventPriority here
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
    "size_horizonal",
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
CURSOR_SHAPE: bidict[CursorShapeStr, QtCore.Qt.CursorShape] = bidict(
    arrow=QtCore.Qt.ArrowCursor,
    uparrow=QtCore.Qt.UpArrowCursor,
    cross=QtCore.Qt.CrossCursor,
    wait=QtCore.Qt.WaitCursor,
    caret=QtCore.Qt.IBeamCursor,
    size_vertical=QtCore.Qt.SizeVerCursor,
    size_horizonal=QtCore.Qt.SizeHorCursor,
    size_topright=QtCore.Qt.SizeBDiagCursor,
    size_topleft=QtCore.Qt.SizeFDiagCursor,
    size_all=QtCore.Qt.SizeAllCursor,
    blank=QtCore.Qt.BlankCursor,
    split_vertical=QtCore.Qt.SplitVCursor,
    split_horizontal=QtCore.Qt.SplitHCursor,
    pointing_hand=QtCore.Qt.PointingHandCursor,
    forbidden=QtCore.Qt.ForbiddenCursor,
    open_hand=QtCore.Qt.OpenHandCursor,
    closed_hand=QtCore.Qt.ClosedHandCursor,
    whats_this=QtCore.Qt.WhatsThisCursor,
    busy=QtCore.Qt.BusyCursor,
    drag_move=QtCore.Qt.DragMoveCursor,
    drag_copy=QtCore.Qt.DragCopyCursor,
    drag_link=QtCore.Qt.DragLinkCursor,
    bitmap=QtCore.Qt.BitmapCursor,
)

LayoutDirectionStr = Literal["left_to_right", "right_to_left", "auto"]
LAYOUT_DIRECTION: bidict[LayoutDirectionStr, QtCore.Qt.LayoutDirection] = bidict(
    left_to_right=QtCore.Qt.LeftToRight,
    right_to_left=QtCore.Qt.RightToLeft,
    auto=QtCore.Qt.LayoutDirectionAuto,
)

ApplicationStateStr = Literal["suspended", "hidden", "inactive", "active"]
APPLICATION_STATES: bidict[ApplicationStateStr, QtCore.Qt.ApplicationState] = bidict(
    suspended=QtCore.Qt.ApplicationSuspended,
    hidden=QtCore.Qt.ApplicationHidden,
    inactive=QtCore.Qt.ApplicationInactive,
    active=QtCore.Qt.ApplicationActive,
)

HighDpiScaleFactorRoundingPolicyStr = Literal[
    "round", "ceil", "floor", "round_prefer_floor", "pass_through"
]
HIGH_DPI_SCALE_FACTOR_ROUNDING_POLICY: bidict[
    HighDpiScaleFactorRoundingPolicyStr, QtCore.Qt.HighDpiScaleFactorRoundingPolicy
] = bidict(
    round=QtCore.Qt.HighDpiScaleFactorRoundingPolicy.Round,
    ceil=QtCore.Qt.HighDpiScaleFactorRoundingPolicy.Ceil,
    floor=QtCore.Qt.HighDpiScaleFactorRoundingPolicy.Floor,
    round_prefer_floor=QtCore.Qt.HighDpiScaleFactorRoundingPolicy.RoundPreferFloor,
    pass_through=QtCore.Qt.HighDpiScaleFactorRoundingPolicy.PassThrough,
)

UiEffectStr = Literal[
    "animate_menu",
    "fade_menu",
    "animate_combo",
    "animate_tooltip",
    "fade_tooltip",
    "animate_toolbox",
]
UI_EFFECTS: bidict[UiEffectStr, QtCore.Qt.UIEffect] = bidict(
    animate_menu=QtCore.Qt.UI_AnimateMenu,
    fade_menu=QtCore.Qt.UI_FadeMenu,
    animate_combo=QtCore.Qt.UI_AnimateCombo,
    animate_tooltip=QtCore.Qt.UI_AnimateTooltip,
    fade_tooltip=QtCore.Qt.UI_FadeTooltip,
    animate_toolbox=QtCore.Qt.UI_AnimateToolBox,
)

NavigationModeStr = Literal[
    "none",
    "keypad_tab_order",
    "keypad_directional",
    "cursor_auto",
    "cursor_force_visible",
]
NAVIGATION_MODES: bidict[NavigationModeStr, QtCore.Qt.NavigationMode] = bidict(
    none=QtCore.Qt.NavigationModeNone,
    keypad_tab_order=QtCore.Qt.NavigationModeKeypadTabOrder,
    keypad_directional=QtCore.Qt.NavigationModeKeypadDirectional,
    cursor_auto=QtCore.Qt.NavigationModeCursorAuto,
    cursor_force_visible=QtCore.Qt.NavigationModeCursorForceVisible,
)

ItemSelectionModeStr = Literal[
    "contains_shape",
    "intersects_shape",
    "contains_bounding_rect",
    "intersects_bounding_rect",
]
ITEM_SELECTION_MODE: bidict[ItemSelectionModeStr, QtCore.Qt.ItemSelectionMode] = bidict(
    contains_shape=QtCore.Qt.ContainsItemShape,
    intersects_shape=QtCore.Qt.IntersectsItemShape,
    contains_bounding_rect=QtCore.Qt.ContainsItemBoundingRect,
    intersects_bounding_rect=QtCore.Qt.IntersectsItemBoundingRect,
)

FocusReasonStr = Literal[
    "mouse", "tab", "backtab", "active_window", "popup", "shortcut", "menu_bar", "other"
]
FOCUS_REASONS: bidict[FocusReasonStr, QtCore.Qt.FocusReason] = bidict(
    mouse=QtCore.Qt.MouseFocusReason,
    tab=QtCore.Qt.TabFocusReason,
    backtab=QtCore.Qt.BacktabFocusReason,
    active_window=QtCore.Qt.ActiveWindowFocusReason,
    popup=QtCore.Qt.PopupFocusReason,
    shortcut=QtCore.Qt.ShortcutFocusReason,
    menu_bar=QtCore.Qt.MenuBarFocusReason,
    other=QtCore.Qt.OtherFocusReason,
)

ElideModeStr = Literal["left", "right", "middle", "none"]
ELIDE_MODE: bidict[ElideModeStr, QtCore.Qt.TextElideMode] = bidict(
    left=QtCore.Qt.ElideLeft,
    right=QtCore.Qt.ElideRight,
    middle=QtCore.Qt.ElideMiddle,
    none=QtCore.Qt.ElideNone,
)

PenStyleStr = Literal[
    "none", "solid", "dash", "dot", "dash_dot", "dash_dot_dot", "custom_dash"
]
PEN_STYLE: bidict[PenStyleStr, QtCore.Qt.PenStyle] = bidict(
    none=QtCore.Qt.NoPen,
    solid=QtCore.Qt.SolidLine,
    dash=QtCore.Qt.DashLine,
    dot=QtCore.Qt.DotLine,
    dash_dot=QtCore.Qt.DashDotLine,
    dash_dot_dot=QtCore.Qt.DashDotDotLine,
    custom_dash=QtCore.Qt.CustomDashLine,
)

CapStyleStr = Literal["flat", "square", "round"]
CAP_STYLE: bidict[CapStyleStr, QtCore.Qt.PenCapStyle] = bidict(
    flat=QtCore.Qt.FlatCap, square=QtCore.Qt.SquareCap, round=QtCore.Qt.RoundCap
)

JoinStyleStr = Literal["miter", "bevel", "round" "svg_miter"]
JOIN_STYLE: bidict[JoinStyleStr, QtCore.Qt.PenJoinStyle] = bidict(
    miter=QtCore.Qt.MiterJoin,
    bevel=QtCore.Qt.BevelJoin,
    round=QtCore.Qt.RoundJoin,
    svg_miter=QtCore.Qt.SvgMiterJoin,
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

PATTERN: bidict[PatternStr, QtCore.Qt.BrushStyle] = bidict(
    none=QtCore.Qt.NoBrush,
    solid=QtCore.Qt.SolidPattern,
    dense_1=QtCore.Qt.Dense1Pattern,
    dense_2=QtCore.Qt.Dense2Pattern,
    dense_3=QtCore.Qt.Dense3Pattern,
    dense_4=QtCore.Qt.Dense4Pattern,
    dense_5=QtCore.Qt.Dense5Pattern,
    dense_6=QtCore.Qt.Dense6Pattern,
    dense_7=QtCore.Qt.Dense7Pattern,
    horizontal=QtCore.Qt.HorPattern,
    vertical=QtCore.Qt.VerPattern,
    cross=QtCore.Qt.CrossPattern,
    backward_diagonal=QtCore.Qt.BDiagPattern,
    forward_diagonal=QtCore.Qt.FDiagPattern,
    crossing_diagonal=QtCore.Qt.DiagCrossPattern,
    linear_gradient=QtCore.Qt.LinearGradientPattern,
    conical_gradient=QtCore.Qt.ConicalGradientPattern,
    radial_gradient=QtCore.Qt.RadialGradientPattern,
    texture=QtCore.Qt.TexturePattern,
)

ClipOperationStr = Literal["none", "replace", "intersect"]
CLIP_OPERATION: bidict[ClipOperationStr, QtCore.Qt.ClipOperation] = bidict(
    none=QtCore.Qt.NoClip,
    replace=QtCore.Qt.ReplaceClip,
    intersect=QtCore.Qt.IntersectClip,
)

ContextStr = Literal["widget", "widget_with_children", "window", "application"]
CONTEXT: bidict[ContextStr, QtCore.Qt.ShortcutContext] = bidict(
    widget=QtCore.Qt.WidgetShortcut,
    widget_with_children=QtCore.Qt.WidgetWithChildrenShortcut,
    window=QtCore.Qt.WindowShortcut,
    application=QtCore.Qt.ApplicationShortcut,
)

TileRuleStr = Literal["stretch", "repeat", "round"]
TILE_RULE: bidict[TileRuleStr, QtCore.Qt.TileRule] = bidict(
    stretch=QtCore.Qt.StretchTile,
    repeat=QtCore.Qt.RepeatTile,
    round=QtCore.Qt.RoundTile,
)

TransformationModeStr = Literal["fast", "smooth"]
TRANSFORMATION_MODE: bidict[TransformationModeStr, QtCore.Qt.TransformationMode] = bidict(
    fast=QtCore.Qt.FastTransformation,
    smooth=QtCore.Qt.SmoothTransformation,
)

GestureTypeStr = Literal["tap", "tap_and_hold", "pan", "pinch", "swipe", "custom"]
GESTURE_TYPE: bidict[GestureTypeStr, QtCore.Qt.GestureType] = bidict(
    tap=QtCore.Qt.TapGesture,
    tap_and_hold=QtCore.Qt.TapAndHoldGesture,
    pan=QtCore.Qt.PanGesture,
    pinch=QtCore.Qt.PinchGesture,
    swipe=QtCore.Qt.SwipeGesture,
    custom=QtCore.Qt.CustomGesture,
)

GestureStateStr = Literal["none", "started", "updated", "finished", "canceled"]
GESTURE_STATE: bidict[GestureStateStr, QtCore.Qt.GestureState] = bidict(
    none=QtCore.Qt.GestureState(0),  # type: ignore # QtCore.Qt.NoGesture,
    started=QtCore.Qt.GestureStarted,
    updated=QtCore.Qt.GestureUpdated,
    finished=QtCore.Qt.GestureFinished,
    canceled=QtCore.Qt.GestureCanceled,
)

ScrollBarPolicyStr = Literal["always_on", "always_off", "as_needed"]
SCROLLBAR_POLICY: bidict[ScrollBarPolicyStr, QtCore.Qt.ScrollBarPolicy] = bidict(
    always_on=QtCore.Qt.ScrollBarAlwaysOn,
    always_off=QtCore.Qt.ScrollBarAlwaysOff,
    as_needed=QtCore.Qt.ScrollBarAsNeeded,
)

ContextPolicyStr = Literal["none", "prevent", "default", "actions", "custom"]
CONTEXT_POLICY: bidict[ContextPolicyStr, QtCore.Qt.ContextMenuPolicy] = bidict(
    none=QtCore.Qt.NoContextMenu,
    prevent=QtCore.Qt.PreventContextMenu,
    default=QtCore.Qt.DefaultContextMenu,
    actions=QtCore.Qt.ActionsContextMenu,
    custom=QtCore.Qt.CustomContextMenu,
    # showhide_menu="showhide_menu",
)

ModalityStr = Literal["window", "application", "none"]
MODALITY: bidict[ModalityStr, QtCore.Qt.WindowModality] = bidict(
    window=QtCore.Qt.WindowModal,
    application=QtCore.Qt.ApplicationModal,
    none=QtCore.Qt.NonModal,
)

FocusPolicyStr = Literal["tab", "click", "strong", "wheel", "none"]
FOCUS_POLICY: bidict[FocusPolicyStr, QtCore.Qt.FocusPolicy] = bidict(
    tab=QtCore.Qt.TabFocus,
    click=QtCore.Qt.ClickFocus,
    strong=QtCore.Qt.StrongFocus,
    wheel=QtCore.Qt.WheelFocus,
    none=QtCore.Qt.NoFocus,
)

WindowFlagStr = Literal[
    "frameless", "popup", "stay_on_top", "tool", "window_title", "customize_window"
]

WINDOW_FLAGS: bidict[WindowFlagStr, QtCore.Qt.WindowType] = bidict(
    frameless=QtCore.Qt.FramelessWindowHint,
    popup=QtCore.Qt.Popup,
    stay_on_top=QtCore.Qt.WindowStaysOnTopHint,
    tool=QtCore.Qt.Tool,
    window_title=QtCore.Qt.WindowTitleHint,
    customize_window=QtCore.Qt.CustomizeWindowHint,
)

WindowStateStr = Literal["none", "minimized", "maximized", "fullscreen", "active"]
WINDOW_STATES = mappers.FlagMap(
    QtCore.Qt.WindowStates,
    none=QtCore.Qt.WindowNoState,
    minimized=QtCore.Qt.WindowMinimized,
    maximized=QtCore.Qt.WindowMaximized,
    fullscreen=QtCore.Qt.WindowFullScreen,
    active=QtCore.Qt.WindowActive,
)

FillRuleStr = Literal["odd_even", "winding"]
FILL_RULE: bidict[FillRuleStr, QtCore.Qt.FillRule] = bidict(
    odd_even=QtCore.Qt.OddEvenFill, winding=QtCore.Qt.WindingFill
)

TimerTypeStr = Literal["precise", "coarse", "very_coarse"]
TIMER_TYPE: bidict[TimerTypeStr, QtCore.Qt.TimerType] = bidict(
    precise=QtCore.Qt.PreciseTimer,
    coarse=QtCore.Qt.CoarseTimer,
    very_coarse=QtCore.Qt.VeryCoarseTimer,
)

CursorMoveStyleStr = Literal["logical", "visual"]
CURSOR_MOVE_STYLE: bidict[CursorMoveStyleStr, QtCore.Qt.CursorMoveStyle] = bidict(
    logical=QtCore.Qt.LogicalMoveStyle, visual=QtCore.Qt.VisualMoveStyle
)

CornerStr = Literal["top_left", "top_right", "bottom_left", "bottom_right"]
CORNER: bidict[CornerStr, QtCore.Qt.Corner] = bidict(
    top_left=QtCore.Qt.TopLeftCorner,
    top_right=QtCore.Qt.TopRightCorner,
    bottom_left=QtCore.Qt.BottomLeftCorner,
    bottom_right=QtCore.Qt.BottomRightCorner,
)

ScreenOrientationStr = Literal[
    "primary", "landscape", "portrait", "inverted_landscape", "inverted_portrait"
]
SCREEN_ORIENTATION: bidict[ScreenOrientationStr, QtCore.Qt.ScreenOrientation] = bidict(
    primary=QtCore.Qt.PrimaryOrientation,
    landscape=QtCore.Qt.LandscapeOrientation,
    portrait=QtCore.Qt.PortraitOrientation,
    inverted_landscape=QtCore.Qt.InvertedLandscapeOrientation,
    inverted_portrait=QtCore.Qt.InvertedPortraitOrientation,
)

AspectRatioModeStr = Literal["ignore", "keep", "keep_by_expanding"]
ASPECT_RATIO_MODE: bidict[AspectRatioModeStr, QtCore.Qt.AspectRatioMode] = bidict(
    ignore=QtCore.Qt.IgnoreAspectRatio,
    keep=QtCore.Qt.KeepAspectRatio,
    keep_by_expanding=QtCore.Qt.KeepAspectRatioByExpanding,
)

DateFormatStr = Literal["text", "iso", "iso_with_ms", "rfc_2822"]
DATE_FORMAT: bidict[DateFormatStr, QtCore.Qt.DateFormat] = bidict(
    text=QtCore.Qt.TextDate,
    iso=QtCore.Qt.ISODate,
    iso_with_ms=QtCore.Qt.ISODateWithMs,
    rfc_2822=QtCore.Qt.RFC2822Date,
)

TimeSpecStr = Literal["local_time", "utc", "offset_from_utc", "timezone"]
TIME_SPEC: bidict[TimeSpecStr, QtCore.Qt.TimeSpec] = bidict(
    local_time=QtCore.Qt.LocalTime,
    utc=QtCore.Qt.UTC,
    offset_from_utc=QtCore.Qt.OffsetFromUTC,
    timezone=QtCore.Qt.TimeZone,
)

AxisStr = Literal["x", "y", "z"]
AXIS: bidict[AxisStr, QtCore.Qt.Axis] = bidict(
    x=QtCore.Qt.XAxis, y=QtCore.Qt.YAxis, z=QtCore.Qt.ZAxis
)

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
WIDGET_ATTRIBUTE: bidict[WidgetAttributeStr, QtCore.Qt.WidgetAttribute] = bidict(
    accept_drops=QtCore.Qt.WA_AcceptDrops,
    always_show_tooltips=QtCore.Qt.WA_AlwaysShowToolTips,
    custom_whats_this=QtCore.Qt.WA_CustomWhatsThis,
    delete_on_close=QtCore.Qt.WA_DeleteOnClose,
    disabled=QtCore.Qt.WA_Disabled,
    dont_show_on_screen=QtCore.Qt.WA_DontShowOnScreen,
    force_disabled=QtCore.Qt.WA_ForceDisabled,
    force_updates_disabled=QtCore.Qt.WA_ForceUpdatesDisabled,
    hover=QtCore.Qt.WA_Hover,
    input_method_enabled=QtCore.Qt.WA_InputMethodEnabled,
    keyboard_focus_change=QtCore.Qt.WA_KeyboardFocusChange,
    key_compression=QtCore.Qt.WA_KeyCompression,
    layout_on_entire_rect=QtCore.Qt.WA_LayoutOnEntireRect,
    layout_uses_widget_rect=QtCore.Qt.WA_LayoutUsesWidgetRect,
    mac_opaque_size_grip=QtCore.Qt.WA_MacOpaqueSizeGrip,
    mac_show_focus_rect=QtCore.Qt.WA_MacShowFocusRect,
    mac_normal_size=QtCore.Qt.WA_MacNormalSize,
    mac_small_size=QtCore.Qt.WA_MacSmallSize,
    mac_mini_size=QtCore.Qt.WA_MacMiniSize,
    # mac_variable_size=QtCore.Qt.WA_MacVariableSize,
    mapped=QtCore.Qt.WA_Mapped,
    mouse_no_mask=QtCore.Qt.WA_MouseNoMask,
    mouse_tracking=QtCore.Qt.WA_MouseTracking,
    moved=QtCore.Qt.WA_Moved,
    no_child_events_for_parent=QtCore.Qt.WA_NoChildEventsForParent,
    no_child_events_from_children=QtCore.Qt.WA_NoChildEventsFromChildren,
    no_mouse_replay=QtCore.Qt.WA_NoMouseReplay,
    no_mouse_propagation=QtCore.Qt.WA_NoMousePropagation,
    transparent_for_mouse_events=QtCore.Qt.WA_TransparentForMouseEvents,
    no_system_background=QtCore.Qt.WA_NoSystemBackground,
    opaque_paint_event=QtCore.Qt.WA_OpaquePaintEvent,
    outside_ws_range=QtCore.Qt.WA_OutsideWSRange,
    paint_on_screen=QtCore.Qt.WA_PaintOnScreen,
    paint_unclipped=QtCore.Qt.WA_PaintUnclipped,
    pending_move_event=QtCore.Qt.WA_PendingMoveEvent,
    pending_resize_egent=QtCore.Qt.WA_PendingResizeEvent,
    quit_on_close=QtCore.Qt.WA_QuitOnClose,
    resized=QtCore.Qt.WA_Resized,
    right_to_left=QtCore.Qt.WA_RightToLeft,
    set_cursor=QtCore.Qt.WA_SetCursor,
    set_font=QtCore.Qt.WA_SetFont,
    set_palette=QtCore.Qt.WA_SetPalette,
    set_style=QtCore.Qt.WA_SetStyle,
    # show_modal=QtCore.Qt.WA_ShowModal,
    static_contents=QtCore.Qt.WA_StaticContents,
    style_sheet=QtCore.Qt.WA_StyleSheet,
    style_sheet_target=QtCore.Qt.WA_StyleSheetTarget,
    tablet_tracking=QtCore.Qt.WA_TabletTracking,
    translucent_background=QtCore.Qt.WA_TranslucentBackground,
    under_mouse=QtCore.Qt.WA_UnderMouse,
    updates_disabled=QtCore.Qt.WA_UpdatesDisabled,
    window_modified=QtCore.Qt.WA_WindowModified,
    window_propagation=QtCore.Qt.WA_WindowPropagation,
    mac_always_show_tool_window=QtCore.Qt.WA_MacAlwaysShowToolWindow,
    set_locale=QtCore.Qt.WA_SetLocale,
    styled_background=QtCore.Qt.WA_StyledBackground,
    show_without_activating=QtCore.Qt.WA_ShowWithoutActivating,
    native_window=QtCore.Qt.WA_NativeWindow,
    dont_create_native_ancestors=QtCore.Qt.WA_DontCreateNativeAncestors,
    x11_net_wm_window_type_desktop=QtCore.Qt.WA_X11NetWmWindowTypeDesktop,
    x11_net_wm_window_type_dock=QtCore.Qt.WA_X11NetWmWindowTypeDock,
    x11_net_wm_window_type_toolbar=QtCore.Qt.WA_X11NetWmWindowTypeToolBar,
    x11_net_wm_window_type_menu=QtCore.Qt.WA_X11NetWmWindowTypeMenu,
    x11_net_wm_window_type_utility=QtCore.Qt.WA_X11NetWmWindowTypeUtility,
    x11_net_wm_window_type_splash=QtCore.Qt.WA_X11NetWmWindowTypeSplash,
    x11_net_wm_window_type_dialog=QtCore.Qt.WA_X11NetWmWindowTypeDialog,
    x11_net_wm_window_type_dropdown_menu=QtCore.Qt.WA_X11NetWmWindowTypeDropDownMenu,
    x11_net_wm_window_type_popup_menu=QtCore.Qt.WA_X11NetWmWindowTypePopupMenu,
    x11_net_wm_window_type_tooltip=QtCore.Qt.WA_X11NetWmWindowTypeToolTip,
    x11_net_wm_window_type_notification=QtCore.Qt.WA_X11NetWmWindowTypeNotification,
    x11_net_wm_window_type_combo=QtCore.Qt.WA_X11NetWmWindowTypeCombo,
    x11_net_wm_window_type_dnd=QtCore.Qt.WA_X11NetWmWindowTypeDND,
    accept_touch_events=QtCore.Qt.WA_AcceptTouchEvents,
    touch_pad_single_touch_events=QtCore.Qt.WA_TouchPadAcceptSingleTouchEvents,
    x11_do_not_accept_focus=QtCore.Qt.WA_X11DoNotAcceptFocus,
    always_stack_on_top=QtCore.Qt.WA_AlwaysStackOnTop,
    contents_margins_respects_safe_area=QtCore.Qt.WA_ContentsMarginsRespectsSafeArea,
)
