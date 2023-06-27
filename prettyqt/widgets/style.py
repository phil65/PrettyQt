from __future__ import annotations

from typing import Literal

from prettyqt import constants, core, widgets
from prettyqt.qt import QtGui, QtWidgets
from prettyqt.utils import bidict


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
    "dialog_yes_to_all",
    "dialog_no_to_all",
    "dialog_save_all",
    "dialog_abort",
    "dialog_retry",
    "dialog_ignore",
    "restore_defaults",
    "tab_close",
]

mod = QtWidgets.QStyle

STANDARD_PIXMAP: bidict[StandardPixmapStr, mod.StandardPixmap] = bidict(
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
    dialog_yes_to_all=mod.StandardPixmap.SP_DialogYesToAllButton,
    dialog_no_to_all=mod.StandardPixmap.SP_DialogNoToAllButton,
    dialog_save_all=mod.StandardPixmap.SP_DialogSaveAllButton,
    dialog_abort=mod.StandardPixmap.SP_DialogAbortButton,
    dialog_retry=mod.StandardPixmap.SP_DialogRetryButton,
    dialog_ignore=mod.StandardPixmap.SP_DialogIgnoreButton,
    restore_defaults=mod.StandardPixmap.SP_RestoreDefaultsButton,
    tab_close=mod.StandardPixmap.SP_TabCloseButton,
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


COMPLEX_CONTROL: bidict[ComplexControlStr, mod.ComplexControl] = bidict(
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

CONTROL_ELEMENT: bidict[ControlElementStr, mod.ControlElement] = bidict(
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

SubControlStr = Literal[
    "none",
    "scrollbar_add_line",
    "scrollbar_sub_line",
    "scrollbar_add_page",
    "scrollbar_sub_page",
    "scrollbar_first",
    "scrollbar_last",
    "scrollbar_slider",
    "scrollbar_groove",
    "spinbox_up",
    "spinbox_down",
    "spinbox_frame",
    "spinbox_edit_field",
    "combobox_edit_field",
    "combobox_arrow",
    "combobox_frame",
    "combobox_list_box_popup",
    "slider_groove",
    "slider_handle",
    "slider_tickmarks",
    "toolbutton",
    "toolbutton_menu",
    "titlebar_sys_menu",
    "titlebar_min_button",
    "titlebar_max_button",
    "titlebar_close_button",
    "titlebar_label",
    "titlebar_normal_button",
    "titlebar_shade_button",
    "titlebar_unshade_button",
    "titlebar_context_help_button",
    "dial_handle",
    "dial_groove",
    "dial_tickmarks",
    "groupbox_frame",
    "groupbox_label",
    "groupbox_checkbox",
    "groupbox_contents",
    "mdi_normal_button",
    "mdi_min_button",
    "mdi_close_button",
    "all",
]

SUB_CONTROL: dict[SubControlStr, mod.SubControl] = dict(
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

PrimitiveElementStr = Literal[
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

pe = mod.PrimitiveElement

PRIMITIVE_ELEMENT: bidict[PrimitiveElementStr, pe] = bidict(
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

PixelMetricStr = Literal[
    "button_margin",
    "dock_widget_title_bar_button_margin",
    "button_default_indicator",
    "menu_button_indicator",
    "button_shift_horizontal",
    "button_shift_vertical",
    "default_frame_width",
    "spinbox_frame_width",
    "combobox_frame_width",
    "mdi_subwindow_frame_width",
    "mdi_subwindow_minimized_width",
    "layout_left_margin",
    "layout_top_margin",
    "layout_right_margin",
    "layout_bottom_margin",
    "layout_horizontal_spacing",
    "layout_vertical_spacing",
    "maximum_drag_distance",
    "scrollbar_extent",
    "scrollbar_slider_min",
    "slider_thickness",
    "slider_control_thickness",
    "slider_length",
    "slider_tickmark_offset",
    "slider_space_available",
    "dock_widget_separator_extent",
    "dock_widget_handle_extent",
    "dock_widget_frame_width",
    "dock_widget_title_margin",
    "menu_bar_panel_width",
    "menu_bar_item_spacing",
    "menu_bar_h_margin",
    "menu_bar_v_margin",
    "tool_bar_frame_width",
    "tool_bar_handle_extent",
    "tool_bar_item_margin",
    "tool_bar_item_spacing",
    "tool_bar_separator_extent",
    "tool_bar_extension_extent",
    "tab_bar_tab_overlap",
    "tab_bar_tab_h_space",
    "tab_bar_tab_v_space",
    "tab_bar_base_height",
    "tab_bar_base_overlap",
    "tab_bar_scroll_button_width",
    "tab_bar_tab_shift_horizontal",
    "tab_bar_tab_shift_vertical",
    "progress_bar_chunk_width",
    "splitter_width",
    "title_bar_height",
    "indicator_width",
    "indicator_height",
    "exclusive_indicator_width",
    "exclusive_indicator_height",
    "menu_panel_width",
    "menu_h_margin",
    "menu_v_margin",
    "menu_scroller_height",
    "menu_tearoff_height",
    "menu_desktop_frame_width",
    "header_mark_size",
    "header_grip_margin",
    "header_margin",
    "spin_box_slider_height",
    "tool_bar_icon_size",
    "small_icon_size",
    "large_icon_size",
    "focus_frame_h_margin",
    "focus_frame_v_margin",
    "icon_view_icon_size",
    "list_view_icon_size",
    "tool_tip_label_frame_width",
    "check_box_label_spacing",
    "radio_button_label_spacing",
    "tab_bar_icon_size",
    "size_grip_size",
    "message_box_icon_size",
    "button_icon_size",
    "text_cursor_width",
    "tabbar_scrollbuttonoverlap",
    "tab_close_indicator_width",
    "tab_close_indicator_height",
    "scroll_view_scroll_bar_spacing",
    "scroll_view_scroll_bar_overlap",
    "sub_menu_overlap",
    "tree_view_indentation",
    "header_default_section_size_horizontal",
    "header_default_section_size_vertical",
    "title_bar_button_icon_size",
    "title_bar_button_size",
    "line_edit_icon_size",
    "line_edit_icon_margin",
]

pm = mod.PixelMetric

PIXEL_METRIC: bidict[PixelMetricStr, pm] = bidict(
    button_margin=pm.PM_ButtonMargin,
    dock_widget_title_bar_button_margin=pm.PM_DockWidgetTitleBarButtonMargin,
    button_default_indicator=pm.PM_ButtonDefaultIndicator,
    menu_button_indicator=pm.PM_MenuButtonIndicator,
    button_shift_horizontal=pm.PM_ButtonShiftHorizontal,
    button_shift_vertical=pm.PM_ButtonShiftVertical,
    default_frame_width=pm.PM_DefaultFrameWidth,
    spinbox_frame_width=pm.PM_SpinBoxFrameWidth,
    combobox_frame_width=pm.PM_ComboBoxFrameWidth,
    mdi_subwindow_frame_width=pm.PM_MdiSubWindowFrameWidth,
    mdi_subwindow_minimized_width=pm.PM_MdiSubWindowMinimizedWidth,
    layout_left_margin=pm.PM_LayoutLeftMargin,
    layout_top_margin=pm.PM_LayoutTopMargin,
    layout_right_margin=pm.PM_LayoutRightMargin,
    layout_bottom_margin=pm.PM_LayoutBottomMargin,
    layout_horizontal_spacing=pm.PM_LayoutHorizontalSpacing,
    layout_vertical_spacing=pm.PM_LayoutVerticalSpacing,
    maximum_drag_distance=pm.PM_MaximumDragDistance,
    scrollbar_extent=pm.PM_ScrollBarExtent,
    scrollbar_slider_min=pm.PM_ScrollBarSliderMin,
    slider_thickness=pm.PM_SliderThickness,
    slider_control_thickness=pm.PM_SliderControlThickness,
    slider_length=pm.PM_SliderLength,
    slider_tickmark_offset=pm.PM_SliderTickmarkOffset,
    slider_space_available=pm.PM_SliderSpaceAvailable,
    dock_widget_separator_extent=pm.PM_DockWidgetSeparatorExtent,
    dock_widget_handle_extent=pm.PM_DockWidgetHandleExtent,
    dock_widget_frame_width=pm.PM_DockWidgetFrameWidth,
    dock_widget_title_margin=pm.PM_DockWidgetTitleMargin,
    menu_bar_panel_width=pm.PM_MenuBarPanelWidth,
    menu_bar_item_spacing=pm.PM_MenuBarItemSpacing,
    menu_bar_h_margin=pm.PM_MenuBarHMargin,
    menu_bar_v_margin=pm.PM_MenuBarVMargin,
    tool_bar_frame_width=pm.PM_ToolBarFrameWidth,
    tool_bar_handle_extent=pm.PM_ToolBarHandleExtent,
    tool_bar_item_margin=pm.PM_ToolBarItemMargin,
    tool_bar_item_spacing=pm.PM_ToolBarItemSpacing,
    tool_bar_separator_extent=pm.PM_ToolBarSeparatorExtent,
    tool_bar_extension_extent=pm.PM_ToolBarExtensionExtent,
    tab_bar_tab_overlap=pm.PM_TabBarTabOverlap,
    tab_bar_tab_h_space=pm.PM_TabBarTabHSpace,
    tab_bar_tab_v_space=pm.PM_TabBarTabVSpace,
    tab_bar_base_height=pm.PM_TabBarBaseHeight,
    tab_bar_base_overlap=pm.PM_TabBarBaseOverlap,
    tab_bar_scroll_button_width=pm.PM_TabBarScrollButtonWidth,
    tab_bar_tab_shift_horizontal=pm.PM_TabBarTabShiftHorizontal,
    tab_bar_tab_shift_vertical=pm.PM_TabBarTabShiftVertical,
    progress_bar_chunk_width=pm.PM_ProgressBarChunkWidth,
    splitter_width=pm.PM_SplitterWidth,
    title_bar_height=pm.PM_TitleBarHeight,
    indicator_width=pm.PM_IndicatorWidth,
    indicator_height=pm.PM_IndicatorHeight,
    exclusive_indicator_width=pm.PM_ExclusiveIndicatorWidth,
    exclusive_indicator_height=pm.PM_ExclusiveIndicatorHeight,
    menu_panel_width=pm.PM_MenuPanelWidth,
    menu_h_margin=pm.PM_MenuHMargin,
    menu_v_margin=pm.PM_MenuVMargin,
    menu_scroller_height=pm.PM_MenuScrollerHeight,
    menu_tearoff_height=pm.PM_MenuTearoffHeight,
    menu_desktop_frame_width=pm.PM_MenuDesktopFrameWidth,
    header_mark_size=pm.PM_HeaderMarkSize,
    header_grip_margin=pm.PM_HeaderGripMargin,
    header_margin=pm.PM_HeaderMargin,
    spin_box_slider_height=pm.PM_SpinBoxSliderHeight,
    tool_bar_icon_size=pm.PM_ToolBarIconSize,
    small_icon_size=pm.PM_SmallIconSize,
    large_icon_size=pm.PM_LargeIconSize,
    focus_frame_h_margin=pm.PM_FocusFrameHMargin,
    focus_frame_v_margin=pm.PM_FocusFrameVMargin,
    icon_view_icon_size=pm.PM_IconViewIconSize,
    list_view_icon_size=pm.PM_ListViewIconSize,
    tool_tip_label_frame_width=pm.PM_ToolTipLabelFrameWidth,
    check_box_label_spacing=pm.PM_CheckBoxLabelSpacing,
    radio_button_label_spacing=pm.PM_RadioButtonLabelSpacing,
    tab_bar_icon_size=pm.PM_TabBarIconSize,
    size_grip_size=pm.PM_SizeGripSize,
    message_box_icon_size=pm.PM_MessageBoxIconSize,
    button_icon_size=pm.PM_ButtonIconSize,
    text_cursor_width=pm.PM_TextCursorWidth,
    tabbar_scrollbuttonoverlap=pm.PM_TabBar_ScrollButtonOverlap,
    tab_close_indicator_width=pm.PM_TabCloseIndicatorWidth,
    tab_close_indicator_height=pm.PM_TabCloseIndicatorHeight,
    scroll_view_scroll_bar_spacing=pm.PM_ScrollView_ScrollBarSpacing,
    scroll_view_scroll_bar_overlap=pm.PM_ScrollView_ScrollBarOverlap,
    sub_menu_overlap=pm.PM_SubMenuOverlap,
    tree_view_indentation=pm.PM_TreeViewIndentation,
    header_default_section_size_horizontal=pm.PM_HeaderDefaultSectionSizeHorizontal,
    header_default_section_size_vertical=pm.PM_HeaderDefaultSectionSizeVertical,
    title_bar_button_icon_size=pm.PM_TitleBarButtonIconSize,
    title_bar_button_size=pm.PM_TitleBarButtonSize,
    line_edit_icon_size=pm.PM_LineEditIconSize,
    line_edit_icon_margin=pm.PM_LineEditIconMargin,
)

StateStr = Literal[
    "none",
    "active",
    "auto_raise",
    "children",
    "down_arrow",
    "editing",
    "enabled",
    "has_edit_focus",
    "has_focus",
    "horizontal",
    "keyboard_focus_change",
    "mouse_over",
    "no_change",
    "off",
    "on",
    "raised",
    "read_only",
    "selected",
    "item",
    "open",
    "sibling",
    "sunken",
    "up_arrow",
    "mini",
    "small",
]

st = mod.StateFlag

State: bidict[StateStr, st] = bidict(
    none=st.State_None,
    active=st.State_Active,
    auto_raise=st.State_AutoRaise,
    children=st.State_Children,
    down_arrow=st.State_DownArrow,
    editing=st.State_Editing,
    enabled=st.State_Enabled,
    # has_edit_focus=st.State_HasEditFocus,
    has_focus=st.State_HasFocus,
    horizontal=st.State_Horizontal,
    keyboard_focus_change=st.State_KeyboardFocusChange,
    mouse_over=st.State_MouseOver,
    no_change=st.State_NoChange,
    off=st.State_Off,
    on=st.State_On,
    raised=st.State_Raised,
    read_only=st.State_ReadOnly,
    selected=st.State_Selected,
    item=st.State_Item,
    open=st.State_Open,
    sibling=st.State_Sibling,
    sunken=st.State_Sunken,
    up_arrow=st.State_UpArrow,
    mini=st.State_Mini,
    small=st.State_Small,
)


class StyleMixin(core.ObjectMixin):
    def draw_primitive(
        self,
        element: SubControlStr | mod.SubControl,
        option: QtWidgets.QStyleOption,
        painter: QtGui.QPainter,
        widget: QtWidgets.QWidget | None = None,
    ):
        self.drawPrimitive(
            PRIMITIVE_ELEMENT.get_enum_value(element), option, painter, widget
        )

    def draw_control(
        self,
        control: ControlElementStr | mod.ControlElement,
        option: QtWidgets.QStyleOption,
        painter: QtGui.QPainter,
        widget: QtWidgets.QWidget | None = None,
    ):
        self.drawPrimitive(
            CONTROL_ELEMENT.get_enum_value(control), option, painter, widget
        )

    def get_layout_spacing(
        self,
        control_1: widgets.sizepolicy.ControlTypeStr | widgets.QSizePolicy.ControlType,
        control_2: widgets.sizepolicy.ControlTypeStr | widgets.QSizePolicy.ControlType,
        orientation: constants.OrientationStr | constants.Orientation,
        option_or_widget: QtWidgets.QStyleOption | QtWidgets.QWidget | None = None,
    ):
        c1 = widgets.sizepolicy.CONTROL_TYPE.get_enum_value(control_1)
        c2 = widgets.sizepolicy.CONTROL_TYPE.get_enum_value(control_2)
        o = constants.ORIENTATION.get_enum_value(orientation)
        match option_or_widget:
            case QtWidgets.QWidget():
                return self.layoutSpacing(c1, c2, o, None, option_or_widget)
            case QtWidgets.QStyleOption() | None:
                return self.layoutSpacing(c1, c2, o, option_or_widget)
            case _:
                raise ValueError(option_or_widget)


class Style(StyleMixin, QtWidgets.QStyle):
    pass
