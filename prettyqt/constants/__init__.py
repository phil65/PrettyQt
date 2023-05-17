"""Constants module."""
from typing import Literal

from prettyqt.qt import QtCore
from prettyqt.utils import bidict

Qt = QtCore.Qt


def __getattr__(name: str):
    return getattr(Qt, name)


DISPLAY_ROLE = Qt.ItemDataRole.DisplayRole
USER_ROLE = Qt.ItemDataRole.UserRole
SORT_ROLE = Qt.ItemDataRole(Qt.ItemDataRole.UserRole + 100)
NAME_ROLE = Qt.ItemDataRole(Qt.ItemDataRole.UserRole + 101)
EDIT_ROLE = Qt.ItemDataRole.EditRole
BACKGROUND_ROLE = Qt.ItemDataRole.BackgroundRole
FOREGROUND_ROLE = Qt.ItemDataRole.ForegroundRole
TOOLTIP_ROLE = Qt.ItemDataRole.ToolTipRole
STATUSTIP_ROLE = Qt.ItemDataRole.StatusTipRole
DECORATION_ROLE = Qt.ItemDataRole.DecorationRole
CHECKSTATE_ROLE = Qt.ItemDataRole.CheckStateRole
ALIGNMENT_ROLE = Qt.ItemDataRole.TextAlignmentRole
SIZE_HINT_ROLE = Qt.ItemDataRole.SizeHintRole
WHATS_THIS_ROLE = Qt.ItemDataRole.WhatsThisRole
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
ALIGN_CENTER_LEFT = Flag.AlignVCenter | Flag.AlignLeft
ALIGN_CENTER_RIGHT = Flag.AlignVCenter | Flag.AlignRight
ALIGN_TOP_LEFT = Flag.AlignTop | Flag.AlignLeft
ALIGN_TOP_RIGHT = Flag.AlignTop | Flag.AlignRight
ALIGN_TOP_CENTER = Flag.AlignTop | Flag.AlignHCenter
ALIGN_BOTTOM_LEFT = Flag.AlignBottom | Flag.AlignLeft
ALIGN_BOTTOM_RIGHT = Flag.AlignBottom | Flag.AlignRight
ALIGN_BOTTOM_CENTER = Flag.AlignBottom | Flag.AlignHCenter

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

ITEM_DATA_ROLE: bidict[ItemDataRoleStr, QtCore.Qt.ItemDataRole | int] = bidict(
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

ALIGNMENTS = bidict(
    none=Qt.AlignmentFlag(0),
    left=ALIGN_LEFT,
    center_left=ALIGN_CENTER_LEFT,
    right=ALIGN_RIGHT,
    center_right=ALIGN_CENTER_RIGHT,
    top_center=ALIGN_TOP_CENTER,
    top=ALIGN_TOP,
    bottom=ALIGN_BOTTOM,
    bottom_center=ALIGN_BOTTOM_CENTER,
    top_left=ALIGN_TOP_LEFT,
    top_right=ALIGN_TOP_RIGHT,
    bottom_left=ALIGN_BOTTOM_LEFT,
    bottom_right=ALIGN_BOTTOM_RIGHT,
    center=ALIGN_CENTER,
)

AlignmentStr = Literal[
    "none",
    "left",
    "right",
    "top",
    "bottom",
    "top_left",
    "top_right",
    "bottom_left",
    "bottom_right",
    "center",
]

SIDES = bidict(
    left=Qt.AlignmentFlag.AlignLeft,
    right=Qt.AlignmentFlag.AlignRight,
    top=Qt.AlignmentFlag.AlignTop,
    bottom=Qt.AlignmentFlag.AlignBottom,
)

SideStr = Literal["left", "right", "top", "bottom"]

EDGES = bidict(
    top=Qt.Edge.TopEdge,
    left=Qt.Edge.LeftEdge,
    right=Qt.Edge.RightEdge,
    bottom=Qt.Edge.BottomEdge,
    top_left=Qt.Edge.TopEdge | Qt.Edge.LeftEdge,
    top_right=Qt.Edge.TopEdge | Qt.Edge.RightEdge,
    bottom_left=Qt.Edge.BottomEdge | Qt.Edge.LeftEdge,
    bottom_right=Qt.Edge.BottomEdge | Qt.Edge.RightEdge,
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

H_ALIGNMENT = bidict(
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

V_ALIGNMENT = bidict(
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

KeyboardModifierStr = Literal[
    "none", "shift", "ctrl", "alt", "meta", "keypad", "group_switch"
]
KEYBOARD_MODIFIERS: bidict[KeyboardModifierStr, Qt.KeyboardModifier] = bidict(
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


CaseSensitivityStr = Literal["case_sensitive", "case_insensitive"]
CASE_SENSITIVITY: bidict[CaseSensitivityStr, Qt.CaseSensitivity] = bidict(
    case_insensitive=Qt.CaseSensitivity.CaseInsensitive,
    case_sensitive=Qt.CaseSensitivity.CaseSensitive,
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

ColorPreferenceStr = Literal["auto", "color_only", "mono_only"]
COLOR_PREFERENCE: bidict[ColorPreferenceStr, Qt.ImageConversionFlag] = bidict(
    # Color/Mono preference (ignored for QBitmap):
    auto=Qt.ImageConversionFlag.AutoColor,
    color_only=Qt.ImageConversionFlag.ColorOnly,
    mono_only=Qt.ImageConversionFlag.MonoOnly,
)

DitherPreferenceStr = Literal["diffuse", "ordered", "threshold"]
DITHER_PREFERENCE: bidict[ImageConversionFlagStr, Qt.ImageConversionFlag] = bidict(
    # Dithering mode preference:
    diffuse=Qt.ImageConversionFlag.DiffuseDither,
    ordered=Qt.ImageConversionFlag.OrderedDither,
    threshold=Qt.ImageConversionFlag.ThresholdDither,
)

AlphaDitherPreferenceStr = Literal["diffuse", "ordered", "threshold"]
ALPHA_DITHER_PREFERENCE: bidict[ImageConversionFlagStr, Qt.ImageConversionFlag] = bidict(
    # Dithering mode preference for 1-bit alpha masks:
    threshold=Qt.ImageConversionFlag.ThresholdAlphaDither,
    ordered=Qt.ImageConversionFlag.OrderedAlphaDither,
    diffuse=Qt.ImageConversionFlag.DiffuseAlphaDither,
)

ModePreferenceStr = Literal[
    "prefer_dither",
    "avoid_dither",
    "auto_dither",
    "no_opaque_detection",
    "no_format_conversion",
]
MODE_PREFERENCE: bidict[ImageConversionFlagStr, Qt.ImageConversionFlag] = bidict(
    # Color matching versus dithering preference:
    prefer_dither=Qt.ImageConversionFlag.PreferDither,
    avoid_dither=Qt.ImageConversionFlag.AvoidDither,
    auto_dither=Qt.ImageConversionFlag.AutoDither,
    no_opaque_detection=Qt.ImageConversionFlag.NoOpaqueDetection,
    no_format_conversion=Qt.ImageConversionFlag.NoFormatConversion,
)

FilterModeStr = Literal["starts_with", "contains", "ends_with"]
FILTER_MODES = bidict(
    starts_with=Qt.MatchFlag.MatchStartsWith,
    contains=Qt.MatchFlag.MatchContains,
    ends_with=Qt.MatchFlag.MatchEndsWith,
)

ColorSchemeStr = Literal["unknown", "light", "dark"]
COLOR_SCHEME: bidict[ColorSchemeStr, Qt.ColorScheme] = bidict(
    unknown=Qt.ColorScheme.Unknown,
    light=Qt.ColorScheme.Light,
    dark=Qt.ColorScheme.Dark,
)

TabFocusBehaviorStr = Literal["none", "text_controls", "list_controls", "all_controls"]
TAB_FOCUS_BEHAVIOR: bidict[TabFocusBehaviorStr, Qt.TabFocusBehavior] = bidict(
    none=Qt.TabFocusBehavior.NoTabFocus,
    text_controls=Qt.TabFocusBehavior.TabFocusTextControls,
    list_controls=Qt.TabFocusBehavior.TabFocusListControls,
    all_controls=Qt.TabFocusBehavior.TabFocusAllControls,
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

ConnectionTypeStr = Literal[
    "auto",
    "direct",
    "queued",
    "blocking_queued",
    "unique",
    "single_shot",
]
CONNECTION_TYPE: bidict[ConnectionTypeStr, Qt.ConnectionType] = bidict(
    auto=Qt.ConnectionType.AutoConnection,
    direct=Qt.ConnectionType.DirectConnection,
    queued=Qt.ConnectionType.QueuedConnection,
    blocking_queued=Qt.ConnectionType.BlockingQueuedConnection,
    unique=Qt.ConnectionType.UniqueConnection,
    single_shot=Qt.ConnectionType.SingleShotConnection,
)


InputMethodQueryStr = Literal[
    "enabled",
    "cursor_rectangle",
    "font",
    "cursor_position",
    "surrounding_text",
    "current_selection",
    "maximum_text_length",
    "anchor_position",
    "hints",
    "preferred_language",
    "platform_data",
    "absolute_position",
    "text_before_cursor",
    "text_after_cursor",
    "enter_key_type",
    "anchor_rectangle",
    "input_item_clip_rectangle",
    "read_only",
]
INPUT_METHOD_QUERY: bidict[InputMethodQueryStr, Qt.InputMethodQuery] = bidict(
    enabled=Qt.InputMethodQuery.ImEnabled,
    cursor_rectangle=Qt.InputMethodQuery.ImCursorRectangle,
    font=Qt.InputMethodQuery.ImFont,
    cursor_position=Qt.InputMethodQuery.ImCursorPosition,
    surrounding_text=Qt.InputMethodQuery.ImSurroundingText,
    current_selection=Qt.InputMethodQuery.ImCurrentSelection,
    maximum_text_length=Qt.InputMethodQuery.ImMaximumTextLength,
    anchor_position=Qt.InputMethodQuery.ImAnchorPosition,
    hints=Qt.InputMethodQuery.ImHints,
    preferred_language=Qt.InputMethodQuery.ImPreferredLanguage,
    platform_data=Qt.InputMethodQuery.ImPlatformData,
    absolute_position=Qt.InputMethodQuery.ImAbsolutePosition,
    text_before_cursor=Qt.InputMethodQuery.ImTextBeforeCursor,
    text_after_cursor=Qt.InputMethodQuery.ImTextAfterCursor,
    enter_key_type=Qt.InputMethodQuery.ImEnterKeyType,
    anchor_rectangle=Qt.InputMethodQuery.ImAnchorRectangle,
    input_item_clip_rectangle=Qt.InputMethodQuery.ImInputItemClipRectangle,
    read_only=Qt.InputMethodQuery.ImReadOnly,
)


DayOfWeekStr = Literal[
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday",
]
DAY_OF_WEEK: bidict[DayOfWeekStr, Qt.DayOfWeek] = bidict(
    monday=Qt.DayOfWeek.Monday,
    tuesday=Qt.DayOfWeek.Tuesday,
    wednesday=Qt.DayOfWeek.Wednesday,
    thursday=Qt.DayOfWeek.Thursday,
    friday=Qt.DayOfWeek.Friday,
    saturday=Qt.DayOfWeek.Saturday,
    sunday=Qt.DayOfWeek.Sunday,
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

JoinStyleStr = Literal["miter", "bevel", "round", "svg_miter"]
JOIN_STYLE: bidict[JoinStyleStr, Qt.PenJoinStyle] = bidict(
    miter=Qt.PenJoinStyle.MiterJoin,
    bevel=Qt.PenJoinStyle.BevelJoin,
    round=Qt.PenJoinStyle.RoundJoin,
    svg_miter=Qt.PenJoinStyle.SvgMiterJoin,
)

BrushStyleStr = Literal[
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

BRUSH_STYLE: bidict[BrushStyleStr, Qt.BrushStyle] = bidict(
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

ShortcutContextStr = Literal["widget", "widget_with_children", "window", "application"]
SHORTCUT_CONTEXT: bidict[ShortcutContextStr, Qt.ShortcutContext] = bidict(
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

AnchorPointStr = Literal[
    "left", "horizontal_center", "right", "top", "vertical_center", "bottom"
]
ANCHOR_POINT = bidict[AnchorPointStr, Qt.AnchorPoint](
    left=QtCore.Qt.AnchorPoint.AnchorLeft,
    horizontal_center=QtCore.Qt.AnchorPoint.AnchorHorizontalCenter,
    right=QtCore.Qt.AnchorPoint.AnchorRight,
    top=QtCore.Qt.AnchorPoint.AnchorTop,
    vertical_center=QtCore.Qt.AnchorPoint.AnchorVerticalCenter,
    bottom=QtCore.Qt.AnchorPoint.AnchorBottom,
)


WindowModalityStr = Literal["window", "application", "none"]
WINDOW_MODALITY: bidict[WindowModalityStr, Qt.WindowModality] = bidict(
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

WindowTypeStr = Literal[
    "frameless", "popup", "stay_on_top", "tool", "window_title", "customize_window"
]

WINDOW_TYPE: bidict[WindowTypeStr, Qt.WindowType] = bidict(
    frameless=Qt.WindowType.FramelessWindowHint,
    popup=Qt.WindowType.Popup,
    stay_on_top=Qt.WindowType.WindowStaysOnTopHint,
    tool=Qt.WindowType.Tool,
    window_title=Qt.WindowType.WindowTitleHint,
    customize_window=Qt.WindowType.CustomizeWindowHint,
)

WindowStateStr = Literal["none", "minimized", "maximized", "fullscreen", "active"]
WINDOW_STATES = bidict(
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

KeyStr = Literal[
    "escape",
    "backtab",
    "backspace",
    "insert",
    "delete",
    "print",
    "sysreq",
    "left",
    "right",
    "pageup",
    "pagedown",
    "control",
    "altgr",
    "capslock",
    "scrolllock",
    "f2",
    "f3",
    "f4",
    "f5",
    "f6",
    "f7",
    "f8",
    "f9",
    "f10",
    "f11",
    "f12",
    "f13",
    "f14",
    "f15",
    "f16",
    "f17",
    "f18",
    "f19",
    "f20",
    "f21",
    "f22",
    "f23",
    "f24",
    "f25",
    "f26",
    "f27",
    "f28",
    "f29",
    "f30",
    "f31",
    "f32",
    "f33",
    "f34",
    "f35",
    "super_l",
    "super_r",
    "hyper_l",
    "hyper_r",
    "direction_l",
    "direction_r",
    "exclam",
    "quotedbl",
    "numbersign",
    "percent",
    "ampersand",
    "apostrophe",
    "parenright",
    "comma",
    "minus",
    "period",
    "num_1",
    "num_2",
    "num_3",
    "num_4",
    "num_5",
    "num_6",
    "num_7",
    "num_8",
    "num_9",
    "colon",
    "semicolon",
    "equal",
    "greater",
    "question",
    "at",
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
    "bracketleft",
    "bracketright",
    "braceleft",
    "braceright",
    "asciitilde",
    "nobreakspace",
    "sterling",
    "currency",
    "brokenbar",
    "diaeresis",
    "copyright",
    "ordfeminine",
    "guillemotleft",
    "registered",
    "degree",
    "plusminus",
    "twosuperior",
    "threesuperior",
    "paragraph",
    "periodcentered",
    "onesuperior",
    "guillemotright",
    "threequarters",
    "aacute",
    "acircumflex",
    "adiaeresis",
    "ccedilla",
    "eacute",
    "ecircumflex",
    "iacute",
    "icircumflex",
    "ntilde",
    "ograve",
    "oacute",
    "ocircumflex",
    "odiaeresis",
    "ooblique",
    "uacute",
    "ucircumflex",
    "ssharp",
    "division",
    "ydiaeresis",
    "codeinput",
    "singlecandidate",
    "multiplecandidate",
    "previouscandidate",
    "muhenkan",
    "romaji",
    "hiragana",
    "katakana",
    "hiragana_katakana",
    "hankaku",
    "zenkaku_hankaku",
    "kana_lock",
    "kana_shift",
    "eisu_shift",
    "eisu_toggle",
    "hangul_start",
    "hangul_hanja",
    "hangul_romaja",
    "hangul_jeonja",
    "hangul_prehanja",
    "hangul_posthanja",
    "dead_acute",
    "dead_circumflex",
    "dead_macron",
    "dead_abovedot",
    "dead_diaeresis",
    "dead_abovering",
    "dead_doubleacute",
    "dead_cedilla",
    "dead_voiced_sound",
    "dead_semivoiced_sound",
    "dead_horn",
    "dead_stroke",
    "dead_abovecomma",
    "dead_abovereversedcomma",
    "dead_belowmacron",
    "dead_belowcircumflex",
    "dead_belowbreve",
    "dead_belowdiaeresis",
    "dead_A",
    "dead_e",
    "dead_E",
    "dead_i",
    "dead_I",
    "dead_o",
    "dead_O",
    "dead_u",
    "dead_U",
    "dead_small_schwa",
    "dead_capital_schwa",
    "dead_lowline",
    "dead_aboveverticalline",
    "dead_belowverticalline",
    "dead_longsolidusoverlay",
    "forward",
    "refresh",
    "volumedown",
    "volumemute",
    "bassboost",
    "bassdown",
    "trebleup",
    "trebledown",
    "mediastop",
    "mediaprevious",
    "mediarecord",
    "mediatoggleplaypause",
    "favorites",
    "standby",
    "openurl",
    "launchmail",
    "launchmedia",
    "launch1",
    "launch2",
    "launch3",
    "launch4",
    "launch5",
    "launch6",
    "launch7",
    "launch8",
    "launch9",
    "launcha",
    "launchb",
    "launchc",
    "launchd",
    "launche",
    "launchf",
    "launchg",
    "launchh",
    "monbrightnessup",
    "monbrightnessdown",
    "keyboardlightonoff",
    "keyboardbrightnessup",
    "keyboardbrightnessdown",
    "screensaver",
    "memo",
    "lightbulb",
    "history",
    "addfavorite",
    "brightnessadjust",
    "community",
    "audiorewind",
    "backforward",
    "applicationleft",
    "applicationright",
    "calculator",
    "cleargrab",
    "display",
    "documents",
    "explorer",
    "itouch",
    "logoff",
    "market",
    "meeting",
    "menupb",
    "mysites",
    "officehome",
    "phone",
    "calendar",
    "reload",
    "rotatewindows",
    "rotationkb",
    "send",
    "spell",
    "splitscreen",
    "taskpane",
    "terminal",
    "travel",
    "xfer",
    "zoomin",
    "zoomout",
    "messenger",
    "mailforward",
    "battery",
    "bluetooth",
    "audioforward",
    "audiorandomplay",
    "audiocycletrack",
    "hibernate",
    "topmenu",
    "powerdown",
    "contrastadjust",
    "touchpadtoggle",
    "touchpadoff",
    "green",
    "yellow",
    "channelup",
    "channeldown",
    "settings",
    "micvolumeup",
    "micvolumedown",
    "open",
    "find",
    "undo",
    "redo",
    "medialast",
    "camerafocus",
    "context2",
    "context3",
    "context4",
    "hangup",
    "select",
    "togglecallhangup",
    "lastnumberredial",
    "printer",
    "sleep",
    "exit",
]

KEY: bidict[KeyStr, Qt.Key] = bidict(
    escape=Qt.Key.Key_Escape,
    backtab=Qt.Key.Key_Backtab,
    backspace=Qt.Key.Key_Backspace,
    insert=Qt.Key.Key_Insert,
    delete=Qt.Key.Key_Delete,
    print=Qt.Key.Key_Print,
    sys_req=Qt.Key.Key_SysReq,
    left=Qt.Key.Key_Left,
    right=Qt.Key.Key_Right,
    page_up=Qt.Key.Key_PageUp,
    page_down=Qt.Key.Key_PageDown,
    control=Qt.Key.Key_Control,
    alt_gr=Qt.Key.Key_AltGr,
    caps_lock=Qt.Key.Key_CapsLock,
    scroll_lock=Qt.Key.Key_ScrollLock,
    f2=Qt.Key.Key_F2,
    f3=Qt.Key.Key_F3,
    f4=Qt.Key.Key_F4,
    f5=Qt.Key.Key_F5,
    f6=Qt.Key.Key_F6,
    f7=Qt.Key.Key_F7,
    f8=Qt.Key.Key_F8,
    f9=Qt.Key.Key_F9,
    f10=Qt.Key.Key_F10,
    f11=Qt.Key.Key_F11,
    f12=Qt.Key.Key_F12,
    f13=Qt.Key.Key_F13,
    f14=Qt.Key.Key_F14,
    f15=Qt.Key.Key_F15,
    f16=Qt.Key.Key_F16,
    f17=Qt.Key.Key_F17,
    f18=Qt.Key.Key_F18,
    f19=Qt.Key.Key_F19,
    f20=Qt.Key.Key_F20,
    f21=Qt.Key.Key_F21,
    f22=Qt.Key.Key_F22,
    f23=Qt.Key.Key_F23,
    f24=Qt.Key.Key_F24,
    f25=Qt.Key.Key_F25,
    f26=Qt.Key.Key_F26,
    f27=Qt.Key.Key_F27,
    f28=Qt.Key.Key_F28,
    f29=Qt.Key.Key_F29,
    f30=Qt.Key.Key_F30,
    f31=Qt.Key.Key_F31,
    f32=Qt.Key.Key_F32,
    f33=Qt.Key.Key_F33,
    f34=Qt.Key.Key_F34,
    f35=Qt.Key.Key_F35,
    super_l=Qt.Key.Key_Super_L,
    super_r=Qt.Key.Key_Super_R,
    hyper_l=Qt.Key.Key_Hyper_L,
    hyper_r=Qt.Key.Key_Hyper_R,
    direction_l=Qt.Key.Key_Direction_L,
    direction_r=Qt.Key.Key_Direction_R,
    exclam=Qt.Key.Key_Exclam,
    quote_dbl=Qt.Key.Key_QuoteDbl,
    number_sign=Qt.Key.Key_NumberSign,
    percent=Qt.Key.Key_Percent,
    ampersand=Qt.Key.Key_Ampersand,
    apostrophe=Qt.Key.Key_Apostrophe,
    paren_right=Qt.Key.Key_ParenRight,
    comma=Qt.Key.Key_Comma,
    minus=Qt.Key.Key_Minus,
    period=Qt.Key.Key_Period,
    num_1=Qt.Key.Key_1,
    num_2=Qt.Key.Key_2,
    num_3=Qt.Key.Key_3,
    num_4=Qt.Key.Key_4,
    num_5=Qt.Key.Key_5,
    num_6=Qt.Key.Key_6,
    num_7=Qt.Key.Key_7,
    num_8=Qt.Key.Key_8,
    num_9=Qt.Key.Key_9,
    colon=Qt.Key.Key_Colon,
    semicolon=Qt.Key.Key_Semicolon,
    equal=Qt.Key.Key_Equal,
    greater=Qt.Key.Key_Greater,
    question=Qt.Key.Key_Question,
    at=Qt.Key.Key_At,
    a=Qt.Key.Key_A,
    b=Qt.Key.Key_B,
    c=Qt.Key.Key_C,
    d=Qt.Key.Key_D,
    e=Qt.Key.Key_E,
    f=Qt.Key.Key_F,
    g=Qt.Key.Key_G,
    h=Qt.Key.Key_H,
    i=Qt.Key.Key_I,
    j=Qt.Key.Key_J,
    k=Qt.Key.Key_K,
    l=Qt.Key.Key_L,
    m=Qt.Key.Key_M,
    n=Qt.Key.Key_N,
    o=Qt.Key.Key_O,
    p=Qt.Key.Key_P,
    q=Qt.Key.Key_Q,
    r=Qt.Key.Key_R,
    s=Qt.Key.Key_S,
    t=Qt.Key.Key_T,
    u=Qt.Key.Key_U,
    v=Qt.Key.Key_V,
    w=Qt.Key.Key_W,
    x=Qt.Key.Key_X,
    y=Qt.Key.Key_Y,
    z=Qt.Key.Key_Z,
    bracket_left=Qt.Key.Key_BracketLeft,
    bracket_right=Qt.Key.Key_BracketRight,
    brace_left=Qt.Key.Key_BraceLeft,
    brace_right=Qt.Key.Key_BraceRight,
    ascii_tilde=Qt.Key.Key_AsciiTilde,
    nobreakspace=Qt.Key.Key_nobreakspace,
    sterling=Qt.Key.Key_sterling,
    currency=Qt.Key.Key_currency,
    brokenbar=Qt.Key.Key_brokenbar,
    diaeresis=Qt.Key.Key_diaeresis,
    copyright=Qt.Key.Key_copyright,
    ordfeminine=Qt.Key.Key_ordfeminine,
    guillemotleft=Qt.Key.Key_guillemotleft,
    registered=Qt.Key.Key_registered,
    degree=Qt.Key.Key_degree,
    plusminus=Qt.Key.Key_plusminus,
    twosuperior=Qt.Key.Key_twosuperior,
    threesuperior=Qt.Key.Key_threesuperior,
    paragraph=Qt.Key.Key_paragraph,
    periodcentered=Qt.Key.Key_periodcentered,
    onesuperior=Qt.Key.Key_onesuperior,
    guillemotright=Qt.Key.Key_guillemotright,
    threequarters=Qt.Key.Key_threequarters,
    aacute=Qt.Key.Key_Aacute,
    acircumflex=Qt.Key.Key_Acircumflex,
    adiaeresis=Qt.Key.Key_Adiaeresis,
    ccedilla=Qt.Key.Key_Ccedilla,
    eacute=Qt.Key.Key_Eacute,
    ecircumflex=Qt.Key.Key_Ecircumflex,
    iacute=Qt.Key.Key_Iacute,
    icircumflex=Qt.Key.Key_Icircumflex,
    ntilde=Qt.Key.Key_Ntilde,
    ograve=Qt.Key.Key_Ograve,
    oacute=Qt.Key.Key_Oacute,
    ocircumflex=Qt.Key.Key_Ocircumflex,
    odiaeresis=Qt.Key.Key_Odiaeresis,
    ooblique=Qt.Key.Key_Ooblique,
    uacute=Qt.Key.Key_Uacute,
    ucircumflex=Qt.Key.Key_Ucircumflex,
    ssharp=Qt.Key.Key_ssharp,
    division=Qt.Key.Key_division,
    ydiaeresis=Qt.Key.Key_ydiaeresis,
    codeinput=Qt.Key.Key_Codeinput,
    single_candidate=Qt.Key.Key_SingleCandidate,
    multiple_candidate=Qt.Key.Key_MultipleCandidate,
    previous_candidate=Qt.Key.Key_PreviousCandidate,
    muhenkan=Qt.Key.Key_Muhenkan,
    romaji=Qt.Key.Key_Romaji,
    hiragana=Qt.Key.Key_Hiragana,
    katakana=Qt.Key.Key_Katakana,
    hiragana_katakana=Qt.Key.Key_Hiragana_Katakana,
    hankaku=Qt.Key.Key_Hankaku,
    zenkaku_hankaku=Qt.Key.Key_Zenkaku_Hankaku,
    kana_lock=Qt.Key.Key_Kana_Lock,
    kana_shift=Qt.Key.Key_Kana_Shift,
    eisu_shift=Qt.Key.Key_Eisu_Shift,
    eisu_toggle=Qt.Key.Key_Eisu_toggle,
    hangul_start=Qt.Key.Key_Hangul_Start,
    hangul_hanja=Qt.Key.Key_Hangul_Hanja,
    hangul_romaja=Qt.Key.Key_Hangul_Romaja,
    hangul_jeonja=Qt.Key.Key_Hangul_Jeonja,
    hangul_prehanja=Qt.Key.Key_Hangul_PreHanja,
    hangul_posthanja=Qt.Key.Key_Hangul_PostHanja,
    dead_acute=Qt.Key.Key_Dead_Acute,
    dead_circumflex=Qt.Key.Key_Dead_Circumflex,
    dead_macron=Qt.Key.Key_Dead_Macron,
    dead_abovedot=Qt.Key.Key_Dead_Abovedot,
    dead_diaeresis=Qt.Key.Key_Dead_Diaeresis,
    dead_abovering=Qt.Key.Key_Dead_Abovering,
    dead_doubleacute=Qt.Key.Key_Dead_Doubleacute,
    dead_cedilla=Qt.Key.Key_Dead_Cedilla,
    dead_voiced_sound=Qt.Key.Key_Dead_Voiced_Sound,
    dead_semivoiced_sound=Qt.Key.Key_Dead_Semivoiced_Sound,
    dead_horn=Qt.Key.Key_Dead_Horn,
    dead_stroke=Qt.Key.Key_Dead_Stroke,
    dead_abovecomma=Qt.Key.Key_Dead_Abovecomma,
    dead_abovereversedcomma=Qt.Key.Key_Dead_Abovereversedcomma,
    dead_belowmacron=Qt.Key.Key_Dead_Belowmacron,
    dead_belowcircumflex=Qt.Key.Key_Dead_Belowcircumflex,
    dead_belowbreve=Qt.Key.Key_Dead_Belowbreve,
    dead_belowdiaeresis=Qt.Key.Key_Dead_Belowdiaeresis,
    dead_A=Qt.Key.Key_Dead_A,
    dead_e=Qt.Key.Key_Dead_e,
    dead_E=Qt.Key.Key_Dead_E,
    dead_i=Qt.Key.Key_Dead_i,
    dead_I=Qt.Key.Key_Dead_I,
    dead_o=Qt.Key.Key_Dead_o,
    dead_O=Qt.Key.Key_Dead_O,
    dead_u=Qt.Key.Key_Dead_u,
    dead_U=Qt.Key.Key_Dead_U,
    dead_small_schwa=Qt.Key.Key_Dead_Small_Schwa,
    dead_capital_schwa=Qt.Key.Key_Dead_Capital_Schwa,
    dead_lowline=Qt.Key.Key_Dead_Lowline,
    dead_aboveverticalline=Qt.Key.Key_Dead_Aboveverticalline,
    dead_belowverticalline=Qt.Key.Key_Dead_Belowverticalline,
    dead_longsolidusoverlay=Qt.Key.Key_Dead_Longsolidusoverlay,
    forward=Qt.Key.Key_Forward,
    refresh=Qt.Key.Key_Refresh,
    volume_down=Qt.Key.Key_VolumeDown,
    volume_mute=Qt.Key.Key_VolumeMute,
    bass_boost=Qt.Key.Key_BassBoost,
    bass_down=Qt.Key.Key_BassDown,
    treble_up=Qt.Key.Key_TrebleUp,
    treble_down=Qt.Key.Key_TrebleDown,
    media_stop=Qt.Key.Key_MediaStop,
    media_previous=Qt.Key.Key_MediaPrevious,
    media_record=Qt.Key.Key_MediaRecord,
    media_toggle_play_pause=Qt.Key.Key_MediaTogglePlayPause,
    favorites=Qt.Key.Key_Favorites,
    standby=Qt.Key.Key_Standby,
    open_url=Qt.Key.Key_OpenUrl,
    launch_mail=Qt.Key.Key_LaunchMail,
    launch_media=Qt.Key.Key_LaunchMedia,
    launch_1=Qt.Key.Key_Launch1,
    launch_2=Qt.Key.Key_Launch2,
    launch_3=Qt.Key.Key_Launch3,
    launch_4=Qt.Key.Key_Launch4,
    launch_5=Qt.Key.Key_Launch5,
    launch_6=Qt.Key.Key_Launch6,
    launch_7=Qt.Key.Key_Launch7,
    launch_8=Qt.Key.Key_Launch8,
    launch_9=Qt.Key.Key_Launch9,
    launch_a=Qt.Key.Key_LaunchA,
    launch_b=Qt.Key.Key_LaunchB,
    launch_c=Qt.Key.Key_LaunchC,
    launch_d=Qt.Key.Key_LaunchD,
    launch_e=Qt.Key.Key_LaunchE,
    launch_f=Qt.Key.Key_LaunchF,
    launch_g=Qt.Key.Key_LaunchG,
    launch_h=Qt.Key.Key_LaunchH,
    mon_brightness_up=Qt.Key.Key_MonBrightnessUp,
    mon_brightness_down=Qt.Key.Key_MonBrightnessDown,
    keyboard_light_on_off=Qt.Key.Key_KeyboardLightOnOff,
    keyboard_brightness_up=Qt.Key.Key_KeyboardBrightnessUp,
    keyboard_brightness_down=Qt.Key.Key_KeyboardBrightnessDown,
    screen_saver=Qt.Key.Key_ScreenSaver,
    memo=Qt.Key.Key_Memo,
    light_bulb=Qt.Key.Key_LightBulb,
    history=Qt.Key.Key_History,
    add_favorite=Qt.Key.Key_AddFavorite,
    brightness_adjust=Qt.Key.Key_BrightnessAdjust,
    community=Qt.Key.Key_Community,
    audio_rewind=Qt.Key.Key_AudioRewind,
    back_forward=Qt.Key.Key_BackForward,
    application_left=Qt.Key.Key_ApplicationLeft,
    application_right=Qt.Key.Key_ApplicationRight,
    calculator=Qt.Key.Key_Calculator,
    clear_grab=Qt.Key.Key_ClearGrab,
    display=Qt.Key.Key_Display,
    documents=Qt.Key.Key_Documents,
    explorer=Qt.Key.Key_Explorer,
    i_touch=Qt.Key.Key_iTouch,
    log_off=Qt.Key.Key_LogOff,
    market=Qt.Key.Key_Market,
    meeting=Qt.Key.Key_Meeting,
    menu_pb=Qt.Key.Key_MenuPB,
    my_sites=Qt.Key.Key_MySites,
    office_home=Qt.Key.Key_OfficeHome,
    phone=Qt.Key.Key_Phone,
    calendar=Qt.Key.Key_Calendar,
    reload=Qt.Key.Key_Reload,
    rotate_windows=Qt.Key.Key_RotateWindows,
    rotation_kb=Qt.Key.Key_RotationKB,
    send=Qt.Key.Key_Send,
    spell=Qt.Key.Key_Spell,
    split_screen=Qt.Key.Key_SplitScreen,
    task_pane=Qt.Key.Key_TaskPane,
    terminal=Qt.Key.Key_Terminal,
    travel=Qt.Key.Key_Travel,
    xfer=Qt.Key.Key_Xfer,
    zoom_in=Qt.Key.Key_ZoomIn,
    zoom_out=Qt.Key.Key_ZoomOut,
    messenger=Qt.Key.Key_Messenger,
    mail_forward=Qt.Key.Key_MailForward,
    battery=Qt.Key.Key_Battery,
    bluetooth=Qt.Key.Key_Bluetooth,
    audio_forward=Qt.Key.Key_AudioForward,
    audio_random_play=Qt.Key.Key_AudioRandomPlay,
    audio_cycle_track=Qt.Key.Key_AudioCycleTrack,
    hibernate=Qt.Key.Key_Hibernate,
    top_menu=Qt.Key.Key_TopMenu,
    power_down=Qt.Key.Key_PowerDown,
    contrast_adjust=Qt.Key.Key_ContrastAdjust,
    touchpad_toggle=Qt.Key.Key_TouchpadToggle,
    touchpad_off=Qt.Key.Key_TouchpadOff,
    green=Qt.Key.Key_Green,
    yellow=Qt.Key.Key_Yellow,
    channel_up=Qt.Key.Key_ChannelUp,
    channel_down=Qt.Key.Key_ChannelDown,
    settings=Qt.Key.Key_Settings,
    mic_volume_up=Qt.Key.Key_MicVolumeUp,
    mic_volume_down=Qt.Key.Key_MicVolumeDown,
    open=Qt.Key.Key_Open,
    find=Qt.Key.Key_Find,
    undo=Qt.Key.Key_Undo,
    redo=Qt.Key.Key_Redo,
    media_last=Qt.Key.Key_MediaLast,
    camera_focus=Qt.Key.Key_CameraFocus,
    context_2=Qt.Key.Key_Context2,
    context_3=Qt.Key.Key_Context3,
    context_4=Qt.Key.Key_Context4,
    hangup=Qt.Key.Key_Hangup,
    select=Qt.Key.Key_Select,
    toggle_call_hangup=Qt.Key.Key_ToggleCallHangup,
    last_number_redial=Qt.Key.Key_LastNumberRedial,
    printer=Qt.Key.Key_Printer,
    sleep=Qt.Key.Key_Sleep,
    exit=Qt.Key.Key_Exit,
)
