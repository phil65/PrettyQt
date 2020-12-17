"""Constants module."""
from typing import Literal

from bidict import bidict
from qtpy import QtCore

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

ORIENTATION = bidict(horizontal=QtCore.Qt.Horizontal, vertical=QtCore.Qt.Vertical)

OrientationStr = Literal["horizontal", "vertical"]

STATE = bidict(
    unchecked=QtCore.Qt.Unchecked,
    partial=QtCore.Qt.PartiallyChecked,
    checked=QtCore.Qt.Checked,
)

StateStr = Literal["unchecked", "partial", "checked"]

MATCH_FLAGS = dict(
    exact=QtCore.Qt.MatchExactly,
    contains=QtCore.Qt.MatchContains,
    starts_with=QtCore.Qt.MatchStartsWith,
    ends_with=QtCore.Qt.MatchEndsWith,
    wildcard=QtCore.Qt.MatchWildcard,
    regex=QtCore.Qt.MatchRegExp,
)

MatchFlagStr = Literal[
    "exact", "containts", "starts_with", "ends_with", "wildcard", "regex"
]

FILTER_MODES = mappers.FlagMap(
    QtCore.Qt.MatchFlags,
    starts_with=QtCore.Qt.MatchStartsWith,
    contains=QtCore.Qt.MatchContains,
    ends_with=QtCore.Qt.MatchEndsWith,
)

FilterModeStr = Literal["starts_with", "contains", "ends_with"]

DROP_ACTION = bidict(
    copy=QtCore.Qt.CopyAction,
    move=QtCore.Qt.MoveAction,
    link=QtCore.Qt.LinkAction,
    action_mask=QtCore.Qt.ActionMask,
    ignore=QtCore.Qt.IgnoreAction,
    target_move=QtCore.Qt.TargetMoveAction,
)

DropActionStr = Literal["copy", "move", "link", "action_mask", "ignore", "target_move"]

DOCK_POSITION = bidict(
    top=QtCore.Qt.TopDockWidgetArea,
    bottom=QtCore.Qt.BottomDockWidgetArea,
    left=QtCore.Qt.LeftDockWidgetArea,
    right=QtCore.Qt.RightDockWidgetArea,
)

DockPositionStr = Literal["top", "bottom", "left", "right"]

DOCK_POSITIONS = bidict(
    top=QtCore.Qt.TopDockWidgetArea,
    bottom=QtCore.Qt.BottomDockWidgetArea,
    left=QtCore.Qt.LeftDockWidgetArea,
    right=QtCore.Qt.RightDockWidgetArea,
    all=QtCore.Qt.AllDockWidgetAreas,
)

DockPositionsStr = Literal["top", "bottom", "left", "right", "all"]

TOOLBAR_AREA = bidict(
    left=QtCore.Qt.LeftToolBarArea,
    right=QtCore.Qt.RightToolBarArea,
    top=QtCore.Qt.TopToolBarArea,
    bottom=QtCore.Qt.BottomToolBarArea,
    all=QtCore.Qt.AllToolBarAreas,
    none=QtCore.Qt.NoToolBarArea,
)

ToolbarAreaStr = Literal["top", "bottom", "left", "right", "all", "none"]

TOOLBUTTON_STYLE = bidict(
    icon=QtCore.Qt.ToolButtonIconOnly,
    text=QtCore.Qt.ToolButtonTextOnly,
    text_beside_icon=QtCore.Qt.ToolButtonTextBesideIcon,
    text_below_icon=QtCore.Qt.ToolButtonTextUnderIcon,
)

ToolButtonStyleStr = Literal["icon", "text", "text_beside_icon", "text_below_icon"]

ARROW_TYPE = bidict(
    none=QtCore.Qt.NoArrow,
    up=QtCore.Qt.UpArrow,
    down=QtCore.Qt.DownArrow,
    left=QtCore.Qt.LeftArrow,
    right=QtCore.Qt.RightArrow,
)

ArrowTypeStr = Literal["none", "up", "down", "left", "right"]

EVENT_PRIORITY = bidict(
    high=QtCore.Qt.HighEventPriority,
    normal=QtCore.Qt.NormalEventPriority,
    low=QtCore.Qt.LowEventPriority,
)

EventPriorityStr = Literal["high", "normal", "low"]

CURSOR_SHAPE = bidict(
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

LAYOUT_DIRECTION = bidict(
    left_to_right=QtCore.Qt.LeftToRight,
    right_to_left=QtCore.Qt.RightToLeft,
    auto=QtCore.Qt.LayoutDirectionAuto,
)

LayoutDirectionStr = Literal["left_to_right", "right_to_left", "auto"]

APPLICATION_STATES = bidict(
    suspended=QtCore.Qt.ApplicationSuspended,
    hidden=QtCore.Qt.ApplicationHidden,
    inactive=QtCore.Qt.ApplicationInactive,
    active=QtCore.Qt.ApplicationActive,
)

ApplicationStateStr = Literal["suspended", "hidden", "inactive", "active"]


HIGH_DPI_SCALE_FACTOR_ROUNDING_POLICY = bidict(
    round=QtCore.Qt.HighDpiScaleFactorRoundingPolicy.Round,
    ceil=QtCore.Qt.HighDpiScaleFactorRoundingPolicy.Ceil,
    floor=QtCore.Qt.HighDpiScaleFactorRoundingPolicy.Floor,
    round_prefer_floor=QtCore.Qt.HighDpiScaleFactorRoundingPolicy.RoundPreferFloor,
    pass_through=QtCore.Qt.HighDpiScaleFactorRoundingPolicy.PassThrough,
)

HighDpiScaleFactorRoundingPolicyStr = Literal[
    "round", "ceil", "floor", "round_prefer_floor", "pass_through"
]

UI_EFFECTS = bidict(
    animate_menu=QtCore.Qt.UI_AnimateMenu,
    fade_menu=QtCore.Qt.UI_FadeMenu,
    animate_combo=QtCore.Qt.UI_AnimateCombo,
    animate_tooltip=QtCore.Qt.UI_AnimateTooltip,
    fade_tooltip=QtCore.Qt.UI_FadeTooltip,
    animate_toolbox=QtCore.Qt.UI_AnimateToolBox,
)

UiEffectStr = Literal[
    "animate_menu",
    "fade_menu",
    "animate_combo",
    "animate_tooltip",
    "fade_tooltip",
    "animate_toolbox",
]

NAVIGATION_MODES = bidict(
    none=QtCore.Qt.NavigationModeNone,
    keypad_tab_order=QtCore.Qt.NavigationModeKeypadTabOrder,
    keypad_directional=QtCore.Qt.NavigationModeKeypadDirectional,
    cursor_auto=QtCore.Qt.NavigationModeCursorAuto,
    cursor_force_visible=QtCore.Qt.NavigationModeCursorForceVisible,
)

NavigationModeStr = Literal[
    "none",
    "keypad_tab_order",
    "keypad_directional",
    "cursor_auto",
    "cursor_force_visible",
]

ITEM_SELECTION_MODE = bidict(
    contains_shape=QtCore.Qt.ContainsItemShape,
    intersects_shape=QtCore.Qt.IntersectsItemShape,
    contains_bounding_rect=QtCore.Qt.ContainsItemBoundingRect,
    intersects_bounding_rect=QtCore.Qt.IntersectsItemBoundingRect,
)

ItemSelectionModeStr = Literal[
    "contains_shape",
    "intersects_shape",
    "contains_bounding_rect",
    "intersects_bounding_rect",
]

FOCUS_REASONS = bidict(
    mouse=QtCore.Qt.MouseFocusReason,
    tab=QtCore.Qt.TabFocusReason,
    backtab=QtCore.Qt.BacktabFocusReason,
    active_window=QtCore.Qt.ActiveWindowFocusReason,
    popup=QtCore.Qt.PopupFocusReason,
    shortcut=QtCore.Qt.ShortcutFocusReason,
    menu_bar=QtCore.Qt.MenuBarFocusReason,
    other=QtCore.Qt.OtherFocusReason,
)

FocusReasonStr = Literal[
    "mouse", "tab", "backtab", "active_window", "popup", "shortcut", "menu_bar", "other"
]

ELIDE_MODE = bidict(
    left=QtCore.Qt.ElideLeft,
    right=QtCore.Qt.ElideRight,
    middle=QtCore.Qt.ElideMiddle,
    none=QtCore.Qt.ElideNone,
)

ElideModeStr = Literal["left", "right", "middle", "none"]

PEN_STYLE = bidict(
    none=QtCore.Qt.NoPen,
    solid=QtCore.Qt.SolidLine,
    dash=QtCore.Qt.DashLine,
    dot=QtCore.Qt.DotLine,
    dash_dot=QtCore.Qt.DashDotLine,
    dash_dot_dot=QtCore.Qt.DashDotDotLine,
    custom_dash=QtCore.Qt.CustomDashLine,
)

PenStyleStr = Literal[
    "none", "solid", "dash", "dot", "dash_dot", "dash_dot_dot", "custom_dash"
]

CAP_STYLE = bidict(
    flat=QtCore.Qt.FlatCap, square=QtCore.Qt.SquareCap, round=QtCore.Qt.RoundCap
)

CapStyleStr = Literal["flat", "square", "round"]

JOIN_STYLE = bidict(
    miter=QtCore.Qt.MiterJoin,
    bevel=QtCore.Qt.BevelJoin,
    round=QtCore.Qt.RoundJoin,
    svg_miter=QtCore.Qt.SvgMiterJoin,
)

JoinStyleStr = Literal["miter", "bevel", "round" "svg_miter"]

PATTERN = bidict(
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

CLIP_OPERATION = bidict(
    none=QtCore.Qt.NoClip,
    replace=QtCore.Qt.ReplaceClip,
    intersect=QtCore.Qt.IntersectClip,
)

ClipOperationStr = Literal["none", "replace", "intersect"]

CONTEXT = bidict(
    widget=QtCore.Qt.WidgetShortcut,
    widget_with_children=QtCore.Qt.WidgetWithChildrenShortcut,
    window=QtCore.Qt.WindowShortcut,
    application=QtCore.Qt.ApplicationShortcut,
)

ContextStr = Literal["widget", "widget_with_children", "window", "application"]

GESTURE_TYPE = bidict(
    tap=QtCore.Qt.TapGesture,
    tap_and_hold=QtCore.Qt.TapAndHoldGesture,
    pan=QtCore.Qt.PanGesture,
    pinch=QtCore.Qt.PinchGesture,
    swipe=QtCore.Qt.SwipeGesture,
    custom=QtCore.Qt.CustomGesture,
)

GestureTypeStr = Literal["tap", "tap_and_hold", "pan", "pinch", "swipe", "custom"]

GESTURE_STATE = bidict(
    none=0,  # QtCore.Qt.NoGesture,
    started=QtCore.Qt.GestureStarted,
    updated=QtCore.Qt.GestureUpdated,
    finished=QtCore.Qt.GestureFinished,
    canceled=QtCore.Qt.GestureCanceled,
)

GestureStateStr = Literal["none", "started", "updated", "finished", "canceled"]

SCROLLBAR_POLICY = bidict(
    always_on=QtCore.Qt.ScrollBarAlwaysOn,
    always_off=QtCore.Qt.ScrollBarAlwaysOff,
    as_needed=QtCore.Qt.ScrollBarAsNeeded,
)

ScrollBarPolicyStr = Literal["always_on", "always_off", "as_needed"]

CONTEXT_POLICY = bidict(
    none=QtCore.Qt.NoContextMenu,
    prevent=QtCore.Qt.PreventContextMenu,
    default=QtCore.Qt.DefaultContextMenu,
    actions=QtCore.Qt.ActionsContextMenu,
    custom=QtCore.Qt.CustomContextMenu,
    # showhide_menu="showhide_menu",
)

ContextPolicyStr = Literal["none", "prevent", "default", "actions", "custom"]

MODALITY = bidict(
    window=QtCore.Qt.WindowModal,
    application=QtCore.Qt.ApplicationModal,
    none=QtCore.Qt.NonModal,
)

ModalityStr = Literal["window", "application", "none"]

FOCUS_POLICY = bidict(
    tab=QtCore.Qt.TabFocus,
    click=QtCore.Qt.ClickFocus,
    strong=QtCore.Qt.StrongFocus,
    wheel=QtCore.Qt.WheelFocus,
    none=QtCore.Qt.NoFocus,
)

FocusPolicyStr = Literal["tab", "click", "strong", "wheel", "none"]

WINDOW_FLAGS = bidict(
    frameless=QtCore.Qt.FramelessWindowHint,
    popup=QtCore.Qt.Popup,
    stay_on_top=QtCore.Qt.WindowStaysOnTopHint,
    tool=QtCore.Qt.Tool,
    window_title=QtCore.Qt.WindowTitleHint,
    customize_window=QtCore.Qt.CustomizeWindowHint,
)

WindowFlagStr = Literal[
    "frameless", "popup", "stay_on_top", "tool", "window_title", "customize_window"
]

WINDOW_ATTRIBUTES = bidict(
    native_window=QtCore.Qt.WA_NativeWindow,
    no_native_ancestors=QtCore.Qt.WA_DontCreateNativeAncestors,
)

WindowAttributeStr = Literal["native_window", "no_native_ancestors"]

WINDOW_STATES = mappers.FlagMap(
    QtCore.Qt.WindowStates,
    none=QtCore.Qt.WindowNoState,
    minimized=QtCore.Qt.WindowMinimized,
    maximized=QtCore.Qt.WindowMaximized,
    fullscreen=QtCore.Qt.WindowFullScreen,
    active=QtCore.Qt.WindowActive,
)

WindowStateStr = Literal["none", "minimized", "maximized", "fullscreen", "active"]

FILL_RULE = bidict(odd_even=QtCore.Qt.OddEvenFill, winding=QtCore.Qt.WindingFill)

FillRuleStr = Literal["odd_even", "winding"]

TIMER_TYPE = bidict(
    precise=QtCore.Qt.PreciseTimer,
    coarse=QtCore.Qt.CoarseTimer,
    very_coarse=QtCore.Qt.VeryCoarseTimer,
)

TimerTypeStr = Literal["precise", "coarse", "very_coarse"]

CURSOR_MOVE_STYLE = bidict(
    logical=QtCore.Qt.LogicalMoveStyle, visual=QtCore.Qt.VisualMoveStyle
)

CursorMoveStyleStr = Literal["logical", "visual"]

CORNER = bidict(
    top_left=QtCore.Qt.TopLeftCorner,
    top_right=QtCore.Qt.TopRightCorner,
    bottom_left=QtCore.Qt.BottomLeftCorner,
    bottom_right=QtCore.Qt.BottomRightCorner,
)

CornerStr = Literal["top_left", "top_right", "bottom_left", "bottom_right"]

SCREEN_ORIENTATION = bidict(
    primary=QtCore.Qt.PrimaryOrientation,
    landscape=QtCore.Qt.LandscapeOrientation,
    portrait=QtCore.Qt.PortraitOrientation,
    inverted_landscape=QtCore.Qt.InvertedLandscapeOrientation,
    inverted_portrait=QtCore.Qt.InvertedPortraitOrientation,
)

ScreenOrientationStr = Literal[
    "primary", "landscape", "portrait", "inverted_landscape", "inverted_portrait"
]

ASPECT_RATIO_MODE = bidict(
    ignore=QtCore.Qt.IgnoreAspectRatio,
    keep=QtCore.Qt.KeepAspectRatio,
    keep_by_expanding=QtCore.Qt.KeepAspectRatioByExpanding,
)

AspectRatioModeStr = Literal["ignore", "keep", "keep_by_expanding"]

DATE_FORMAT = bidict(
    text=QtCore.Qt.TextDate,
    iso=QtCore.Qt.ISODate,
    iso_with_ms=QtCore.Qt.ISODateWithMs,
    rfc_2822=QtCore.Qt.RFC2822Date,
)

DateFormatStr = Literal["text", "iso", "iso_with_ms", "rfc_2822"]

TIME_SPEC = bidict(
    local_time=QtCore.Qt.LocalTime,
    utc=QtCore.Qt.UTC,
    offset_from_utc=QtCore.Qt.OffsetFromUTC,
    timezone=QtCore.Qt.TimeZone,
)

TimeSpecStr = Literal["local_time", "utc", "offset_from_utc", "timezone"]

AXIS = bidict(x=QtCore.Qt.XAxis, y=QtCore.Qt.YAxis, z=QtCore.Qt.ZAxis)

AxisStr = Literal["x", "y", "z"]
