from __future__ import annotations

from typing import Literal

from prettyqt import core
from prettyqt.qt import QtGui, QtWidgets
from prettyqt.utils import InvalidParamError, bidict


mod = QtWidgets.QStyle

STANDARD_PIXMAP = dict(
    titlebar_min_button=mod.StandardPixmap.SP_TitleBarMinButton,
    titlebar_menu_button=mod.StandardPixmap.SP_TitleBarMenuButton,
    titlebar_max_button=mod.StandardPixmap.SP_TitleBarMaxButton,
    titlebar_close_button=mod.StandardPixmap.SP_TitleBarCloseButton,
    titlebar_normal_button=mod.StandardPixmap.SP_TitleBarNormalButton,
    titlebar_shade_button=mod.StandardPixmap.SP_TitleBarShadeButton,
    titlebar_unshade_button=mod.StandardPixmap.SP_TitleBarUnshadeButton,
    titlebar_context_help_button=mod.StandardPixmap.SP_TitleBarContextHelpButton,
    information=mod.StandardPixmap.SP_MessageBoxInformation,
    warning=mod.StandardPixmap.SP_MessageBoxWarning,
    critical=mod.StandardPixmap.SP_MessageBoxCritical,
    question=mod.StandardPixmap.SP_MessageBoxQuestion,
    desktop=mod.StandardPixmap.SP_DesktopIcon,
    trash=mod.StandardPixmap.SP_TrashIcon,
    computer=mod.StandardPixmap.SP_ComputerIcon,
    drive_fd=mod.StandardPixmap.SP_DriveFDIcon,
    drive_hd=mod.StandardPixmap.SP_DriveHDIcon,
    drive_cd=mod.StandardPixmap.SP_DriveCDIcon,
    drive_dvd=mod.StandardPixmap.SP_DriveDVDIcon,
    drive_net=mod.StandardPixmap.SP_DriveNetIcon,
    dir_home=mod.StandardPixmap.SP_DirHomeIcon,
    dir_open=mod.StandardPixmap.SP_DirOpenIcon,
    dir_closed=mod.StandardPixmap.SP_DirClosedIcon,
    dir=mod.StandardPixmap.SP_DirIcon,
    dir_link=mod.StandardPixmap.SP_DirLinkIcon,
    dir_link_open=mod.StandardPixmap.SP_DirLinkOpenIcon,
    file=mod.StandardPixmap.SP_FileIcon,
    file_link=mod.StandardPixmap.SP_FileLinkIcon,
    file_dialog_start=mod.StandardPixmap.SP_FileDialogStart,
    file_dialog_end=mod.StandardPixmap.SP_FileDialogEnd,
    file_dialog_to_parent=mod.StandardPixmap.SP_FileDialogToParent,
    file_dialog_new_folder=mod.StandardPixmap.SP_FileDialogNewFolder,
    file_dialog_detailed_view=mod.StandardPixmap.SP_FileDialogDetailedView,
    file_dialog_info_view=mod.StandardPixmap.SP_FileDialogInfoView,
    file_dialog_contents_view=mod.StandardPixmap.SP_FileDialogContentsView,
    file_dialog_list_view=mod.StandardPixmap.SP_FileDialogListView,
    file_dialog_back=mod.StandardPixmap.SP_FileDialogBack,
    dockwidget_close_button=mod.StandardPixmap.SP_DockWidgetCloseButton,
    toolbar_horizontal_extension=mod.StandardPixmap.SP_ToolBarHorizontalExtensionButton,
    toolbar_vertical_extension=mod.StandardPixmap.SP_ToolBarVerticalExtensionButton,
    dialog_ok=mod.StandardPixmap.SP_DialogOkButton,
    dialog_cancel=mod.StandardPixmap.SP_DialogCancelButton,
    dialog_help=mod.StandardPixmap.SP_DialogHelpButton,
    dialog_open=mod.StandardPixmap.SP_DialogOpenButton,
    dialog_save=mod.StandardPixmap.SP_DialogSaveButton,
    dialog_close=mod.StandardPixmap.SP_DialogCloseButton,
    dialog_apply=mod.StandardPixmap.SP_DialogApplyButton,
    dialor_reset=mod.StandardPixmap.SP_DialogResetButton,
    dialog_discard=mod.StandardPixmap.SP_DialogDiscardButton,
    dialog_yes=mod.StandardPixmap.SP_DialogYesButton,
    dialog_no=mod.StandardPixmap.SP_DialogNoButton,
    arrow_up=mod.StandardPixmap.SP_ArrowUp,
    arrow_down=mod.StandardPixmap.SP_ArrowDown,
    arrow_left=mod.StandardPixmap.SP_ArrowLeft,
    arrow_right=mod.StandardPixmap.SP_ArrowRight,
    arrow_back=mod.StandardPixmap.SP_ArrowBack,
    arrow_forward=mod.StandardPixmap.SP_ArrowForward,
    command_link=mod.StandardPixmap.SP_CommandLink,
    vista_shield=mod.StandardPixmap.SP_VistaShield,
    browser_reload=mod.StandardPixmap.SP_BrowserReload,
    browser_stop=mod.StandardPixmap.SP_BrowserStop,
    media_play=mod.StandardPixmap.SP_MediaPlay,
    media_stop=mod.StandardPixmap.SP_MediaStop,
    media_pause=mod.StandardPixmap.SP_MediaPause,
    media_skip_forward=mod.StandardPixmap.SP_MediaSkipForward,
    media_skip_backward=mod.StandardPixmap.SP_MediaSkipBackward,
    media_seek_forward=mod.StandardPixmap.SP_MediaSeekForward,
    media_seek_backward=mod.StandardPixmap.SP_MediaSeekBackward,
    media_volume=mod.StandardPixmap.SP_MediaVolume,
    media_volume_muted=mod.StandardPixmap.SP_MediaVolumeMuted,
    lineedit_clear=mod.StandardPixmap.SP_LineEditClearButton,
    custom_base=mod.StandardPixmap.SP_CustomBase,
)

StandardPixmapStr = Literal[
    "titlebar_min_button=",
    "titlebar_menu_button",
    "titlebar_max_button",
    "titlebar_close_button",
    "titlebar_normal_button",
    "titlebar_shade_button",
    "titlebar_unshade_button",
    "titlebar_context_help_button",
    "information",
    "warning",
    "critical",
    "question",
    "desktop",
    "trash",
    "computer",
    "drive_fd",
    "drive_hd",
    "drive_cd",
    "drive_dvd",
    "drive_net",
    "dir_home",
    "dir_open",
    "dir_closed",
    "dir",
    "dir_link",
    "dir_link_open",
    "file",
    "file_link",
    "file_dialog_start",
    "file_dialog_end",
    "file_dialog_to_parent",
    "file_dialog_new_folder",
    "file_dialog_detailed_view",
    "file_dialog_info_view",
    "file_dialog_contents_view",
    "file_dialog_list_view",
    "file_dialog_back",
    "dockwidget_close_button",
    "toolbar_horizontal_extension",
    "toolbar_vertical_extension",
    "dialog_ok",
    "dialog_cancel",
    "dialog_help",
    "dialog_open",
    "dialog_save",
    "dialog_close",
    "dialog_apply",
    "dialor_reset",
    "dialog_discard",
    "dialog_yes",
    "dialog_no",
    "arrow_up",
    "arrow_down",
    "arrow_left",
    "arrow_right",
    "arrow_back",
    "arrow_forward",
    "command_link",
    "vista_shield",
    "browser_reload",
    "browser_stop",
    "media_play",
    "media_stop",
    "media_pause",
    "media_skip_forward",
    "media_skip_backward",
    "media_seek_forward",
    "media_seek_backward",
    "media_volume",
    "media_volume_muted",
    "lineedit_clear",
    "custom_base",
]

if core.VersionNumber.get_qt_version() >= (5, 14, 0):
    STANDARD_PIXMAP["dialog_yes_to_all"] = mod.StandardPixmap.SP_DialogYesToAllButton
    STANDARD_PIXMAP["dialog_no_to_all"] = mod.StandardPixmap.SP_DialogNoToAllButton
    STANDARD_PIXMAP["dialog_save_all"] = mod.StandardPixmap.SP_DialogSaveAllButton
    STANDARD_PIXMAP["dialog_abort"] = mod.StandardPixmap.SP_DialogAbortButton
    STANDARD_PIXMAP["dialog_retry"] = mod.StandardPixmap.SP_DialogRetryButton
    STANDARD_PIXMAP["dialog_ignore"] = mod.StandardPixmap.SP_DialogIgnoreButton
    STANDARD_PIXMAP["restore_defaults"] = mod.StandardPixmap.SP_RestoreDefaultsButton

COMPLEX_CONTROL = bidict(
    spinbox=mod.ComplexControl.CC_SpinBox,
    combobox=mod.ComplexControl.CC_ComboBox,
    scrollbar=mod.ComplexControl.CC_ScrollBar,
    slider=mod.ComplexControl.CC_Slider,
    toolbutton=mod.ComplexControl.CC_ToolButton,
    titlebar=mod.ComplexControl.CC_TitleBar,
    groupbox=mod.ComplexControl.CC_GroupBox,
    dial=mod.ComplexControl.CC_Dial,
    mdi_controls=mod.ComplexControl.CC_MdiControls,
    custom_base=mod.ComplexControl.CC_CustomBase,
)

ComplexControlStr = Literal[
    "spinbox",
    "combobox",
    "scrollbar",
    "slider",
    "toolbutton",
    "titlebar",
    "groupbox",
    "dial",
    "mdi_controls",
    "custom_base",
]

CONTROL_ELEMENT = bidict(
    push_button=mod.ControlElement.CE_PushButton,
    push_button_bevel=mod.ControlElement.CE_PushButtonBevel,
    push_button_label=mod.ControlElement.CE_PushButtonLabel,
    dock_widget_title=mod.ControlElement.CE_DockWidgetTitle,
    splitter=mod.ControlElement.CE_Splitter,
    check_box=mod.ControlElement.CE_CheckBox,
    check_box_label=mod.ControlElement.CE_CheckBoxLabel,
    radio_button=mod.ControlElement.CE_RadioButton,
    radio_button_label=mod.ControlElement.CE_RadioButtonLabel,
    tab_bar_tab=mod.ControlElement.CE_TabBarTab,
    tab_bar_tab_shape=mod.ControlElement.CE_TabBarTabShape,
    tab_bar_tab_label=mod.ControlElement.CE_TabBarTabLabel,
    progress_bar=mod.ControlElement.CE_ProgressBar,
    progress_bar_groove=mod.ControlElement.CE_ProgressBarGroove,
    progress_bar_contents=mod.ControlElement.CE_ProgressBarContents,
    progress_bar_label=mod.ControlElement.CE_ProgressBarLabel,
    tool_button_label=mod.ControlElement.CE_ToolButtonLabel,
    menu_bar_item=mod.ControlElement.CE_MenuBarItem,
    menu_bar_empty_area=mod.ControlElement.CE_MenuBarEmptyArea,
    menu_item=mod.ControlElement.CE_MenuItem,
    menu_scroller=mod.ControlElement.CE_MenuScroller,
    menu_tear_off=mod.ControlElement.CE_MenuTearoff,
    menu_empty_area=mod.ControlElement.CE_MenuEmptyArea,
    menu_h_margin=mod.ControlElement.CE_MenuHMargin,
    menu_v_margin=mod.ControlElement.CE_MenuVMargin,
    tool_box_tab=mod.ControlElement.CE_ToolBoxTab,
    size_grip=mod.ControlElement.CE_SizeGrip,
    header=mod.ControlElement.CE_Header,
    header_section=mod.ControlElement.CE_HeaderSection,
    header_label=mod.ControlElement.CE_HeaderLabel,
    scroll_bar_add_line=mod.ControlElement.CE_ScrollBarAddLine,
    scroll_bar_sub_line=mod.ControlElement.CE_ScrollBarSubLine,
    scroll_bar_add_page=mod.ControlElement.CE_ScrollBarAddPage,
    scroll_bar_sub_page=mod.ControlElement.CE_ScrollBarSubPage,
    scroll_bar_slider=mod.ControlElement.CE_ScrollBarSlider,
    scroll_bar_first=mod.ControlElement.CE_ScrollBarFirst,
    scroll_bar_last=mod.ControlElement.CE_ScrollBarLast,
    rubber_band=mod.ControlElement.CE_RubberBand,
    focus_frame=mod.ControlElement.CE_FocusFrame,
    item_view_item=mod.ControlElement.CE_ItemViewItem,
    custom_base=mod.ControlElement.CE_CustomBase,
    combo_box_label=mod.ControlElement.CE_ComboBoxLabel,
    tool_bar=mod.ControlElement.CE_ToolBar,
    tool_box_tab_shape=mod.ControlElement.CE_ToolBoxTabShape,
    tool_box_tab_label=mod.ControlElement.CE_ToolBoxTabLabel,
    header_empty_area=mod.ControlElement.CE_HeaderEmptyArea,
    shaped_frame=mod.ControlElement.CE_ShapedFrame,
)

ControlElementStr = Literal[
    "push_button",
    "push_button_bevel",
    "push_button_label",
    "dock_widget_title",
    "splitter",
    "check_box",
    "check_box_label",
    "radio_button",
    "radio_button_label",
    "tab_bar_tab",
    "tab_bar_tab_shape",
    "tab_bar_tab_label",
    "progress_bar",
    "progress_bar_groove",
    "progress_bar_contents",
    "progress_bar_label",
    "tool_button_label",
    "menu_bar_item",
    "menu_bar_empty_area",
    "menu_item",
    "menu_scroller",
    "menu_tear_off",
    "menu_empty_area",
    "menu_h_margin",
    "menu_v_margin",
    "tool_box_tab",
    "size_grip",
    "header",
    "header_section",
    "header_label",
    "scroll_bar_add_line",
    "scroll_bar_sub_line",
    "scroll_bar_add_page",
    "scroll_bar_sub_page",
    "scroll_bar_slider",
    "scroll_bar_first",
    "scroll_bar_last",
    "rubber_band",
    "focus_frame",
    "item_view_item",
    "custom_base",
    "combo_box_label",
    "tool_bar",
    "tool_box_tab_shape",
    "tool_box_tab_label",
    "header_empty_area",
    "shaped_frame",
]

SIMPLE_CONTROLS = dict(
    none=mod.SubControl.SC_None,
    scrollbar_add_line=mod.SubControl.SC_ScrollBarAddLine,
    scrollbar_sub_line=mod.SubControl.SC_ScrollBarSubLine,
    scrollbar_add_page=mod.SubControl.SC_ScrollBarAddPage,
    scrollbar_sub_page=mod.SubControl.SC_ScrollBarSubPage,
    scrollbar_first=mod.SubControl.SC_ScrollBarFirst,
    scrollbar_last=mod.SubControl.SC_ScrollBarLast,
    scrollbar_slider=mod.SubControl.SC_ScrollBarSlider,
    scrollbar_groove=mod.SubControl.SC_ScrollBarGroove,
    spinbox_up=mod.SubControl.SC_SpinBoxUp,
    spinbox_down=mod.SubControl.SC_SpinBoxDown,
    spinbox_frame=mod.SubControl.SC_SpinBoxFrame,
    spinbox_edit_field=mod.SubControl.SC_SpinBoxEditField,
    combobox_edit_field=mod.SubControl.SC_ComboBoxEditField,
    combobox_arrow=mod.SubControl.SC_ComboBoxArrow,
    combobox_frame=mod.SubControl.SC_ComboBoxFrame,
    combobox_list_box_popup=mod.SubControl.SC_ComboBoxListBoxPopup,
    slider_groove=mod.SubControl.SC_SliderGroove,
    slider_handle=mod.SubControl.SC_SliderHandle,
    slider_tickmarks=mod.SubControl.SC_SliderTickmarks,
    toolbutton=mod.SubControl.SC_ToolButton,
    toolbutton_menu=mod.SubControl.SC_ToolButtonMenu,
    titlebar_sys_menu=mod.SubControl.SC_TitleBarSysMenu,
    titlebar_min_button=mod.SubControl.SC_TitleBarMinButton,
    titlebar_max_button=mod.SubControl.SC_TitleBarMaxButton,
    titlebar_close_button=mod.SubControl.SC_TitleBarCloseButton,
    titlebar_label=mod.SubControl.SC_TitleBarLabel,
    titlebar_normal_button=mod.SubControl.SC_TitleBarNormalButton,
    titlebar_shade_button=mod.SubControl.SC_TitleBarShadeButton,
    titlebar_unshade_button=mod.SubControl.SC_TitleBarUnshadeButton,
    titlebar_context_help_button=mod.SubControl.SC_TitleBarContextHelpButton,
    dial_handle=mod.SubControl.SC_DialHandle,
    dial_groove=mod.SubControl.SC_DialGroove,
    dial_tickmarks=mod.SubControl.SC_DialTickmarks,
    groupbox_frame=mod.SubControl.SC_GroupBoxFrame,
    groupbox_label=mod.SubControl.SC_GroupBoxLabel,
    groupbox_checkbox=mod.SubControl.SC_GroupBoxCheckBox,
    groupbox_contents=mod.SubControl.SC_GroupBoxContents,
    mdi_normal_button=mod.SubControl.SC_MdiNormalButton,
    mdi_min_button=mod.SubControl.SC_MdiMinButton,
    mdi_close_button=mod.SubControl.SC_MdiCloseButton,
    all=mod.SubControl.SC_All,
)

pe = mod.PrimitiveElement

PRIMITIVE_ELEMENT = bidict(
    panel_button_command=pe.PE_PanelButtonCommand,
    frame_default_button=pe.PE_FrameDefaultButton,
    panel_button_bevel=pe.PE_PanelButtonBevel,
    panel_button_tool=pe.PE_PanelButtonTool,
    panel_line_edit=pe.PE_PanelLineEdit,
    indicator_button_drop_down=pe.PE_IndicatorButtonDropDown,
    frame_focus_rect=pe.PE_FrameFocusRect,
    indicator_arrow_up=pe.PE_IndicatorArrowUp,
    indicator_arrow_down=pe.PE_IndicatorArrowDown,
    indicator_arrow_right=pe.PE_IndicatorArrowRight,
    indicator_arrow_left=pe.PE_IndicatorArrowLeft,
    indicator_spin_up=pe.PE_IndicatorSpinUp,
    indicator_spin_down=pe.PE_IndicatorSpinDown,
    indicator_spin_plus=pe.PE_IndicatorSpinPlus,
    indicator_spin_minus=pe.PE_IndicatorSpinMinus,
    indicator_item_view_item_check=pe.PE_IndicatorItemViewItemCheck,
    indicator_check_box=pe.PE_IndicatorCheckBox,
    indicator_radio_button=pe.PE_IndicatorRadioButton,
    indicator_dock_widget_resize_handle=pe.PE_IndicatorDockWidgetResizeHandle,
    frame=pe.PE_Frame,
    frame_menu=pe.PE_FrameMenu,
    panel_menu_bar=pe.PE_PanelMenuBar,
    panel_scroll_area_corner=pe.PE_PanelScrollAreaCorner,
    frame_dock_widget=pe.PE_FrameDockWidget,
    frame_tab_widget=pe.PE_FrameTabWidget,
    frame_line_edit=pe.PE_FrameLineEdit,
    frame_group_box=pe.PE_FrameGroupBox,
    frame_button_bevel=pe.PE_FrameButtonBevel,
    frame_button_tool=pe.PE_FrameButtonTool,
    indicator_header_arrow=pe.PE_IndicatorHeaderArrow,
    frame_status_bar_item=pe.PE_FrameStatusBarItem,
    frame_window=pe.PE_FrameWindow,
    indicator_menu_check_mark=pe.PE_IndicatorMenuCheckMark,
    indicator_progress_chunk=pe.PE_IndicatorProgressChunk,
    indicator_branch=pe.PE_IndicatorBranch,
    indicator_tool_bar_handle=pe.PE_IndicatorToolBarHandle,
    indicator_tool_bar_separator=pe.PE_IndicatorToolBarSeparator,
    panel_tool_bar=pe.PE_PanelToolBar,
    panel_tip_label=pe.PE_PanelTipLabel,
    frame_tab_bar_base=pe.PE_FrameTabBarBase,
    indicator_tab_tear_left=pe.PE_IndicatorTabTearLeft,
    indicator_tab_tear_right=pe.PE_IndicatorTabTearRight,
    indicator_column_view_arrow=pe.PE_IndicatorColumnViewArrow,
    widget=pe.PE_Widget,
    custom_base=pe.PE_CustomBase,
    indicator_item_view_item_drop=pe.PE_IndicatorItemViewItemDrop,
    panel_item_view_item=pe.PE_PanelItemViewItem,
    panel_item_view_row=pe.PE_PanelItemViewRow,
    panel_status_bar=pe.PE_PanelStatusBar,
    indicator_tab_close=pe.PE_IndicatorTabClose,
    panel_menu=pe.PE_PanelMenu,
)

SimpleControlStr = Literal[
    "panel_button_command",
    "frame_default_button",
    "panel_button_bevel",
    "panel_button_tool",
    "panel_line_edit",
    "indicator_button_drop_down",
    "frame_focus_rect",
    "indicator_arrow_up",
    "indicator_arrow_down",
    "indicator_arrow_right",
    "indicator_arrow_left",
    "indicator_spin_up",
    "indicator_spin_down",
    "indicator_spin_plus",
    "indicator_spin_minus",
    "indicator_item_view_item_check",
    "indicator_check_box",
    "indicator_radio_button",
    "indicator_dock_widget_resize_handle",
    "frame",
    "frame_menu",
    "panel_menu_bar",
    "panel_scroll_area_corner",
    "frame_dock_widget",
    "frame_tab_widget",
    "frame_line_edit",
    "frame_group_box",
    "frame_button_bevel",
    "frame_button_tool",
    "indicator_header_arrow",
    "frame_status_bar_item",
    "frame_window",
    "indicator_menu_check_mark",
    "indicator_progress_chunk",
    "indicator_branch",
    "indicator_tool_bar_handle",
    "indicator_tool_bar_separator",
    "panel_tool_bar",
    "panel_tip_label",
    "frame_tab_bar_base",
    "indicator_tab_tear_left",
    "indicator_tab_tear_right",
    "indicator_column_view_arrow",
    "widget",
    "custom_base",
    "indicator_item_view_item_drop",
    "panel_item_view_item",
    "panel_item_view_row",
    "panel_status_bar",
    "indicator_tab_close",
    "panel_menu",
]


class Style(QtWidgets.QStyle):
    def draw_primitive(
        self,
        element: SimpleControlStr,
        option: QtWidgets.QStyleOption,
        painter: QtGui.QPainter,
        widget: QtWidgets.QWidget | None = None,
    ):
        if element not in PRIMITIVE_ELEMENT:
            raise InvalidParamError(element, PRIMITIVE_ELEMENT)
        self.drawPrimitive(PRIMITIVE_ELEMENT[element], option, painter, widget)

    def draw_control(
        self,
        control: ControlElementStr,
        option: QtWidgets.QStyleOption,
        painter: QtGui.QPainter,
        widget: QtWidgets.QWidget | None = None,
    ):
        if control not in CONTROL_ELEMENT:
            raise InvalidParamError(control, CONTROL_ELEMENT)
        self.drawPrimitive(CONTROL_ELEMENT[control], option, painter, widget)
