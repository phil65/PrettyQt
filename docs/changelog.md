## v1.53.0 (2023-07-07)

### Feat

- **AbstractItemModel**: add to_mermaid_tree method
- **AbstractTableModel**: add to_markdown method
- **Stalker**: add show method
- **MetaObject**: add has_property and copy_properties_to methods
- **AbstractItemView**: support Sequence as column/row kwarg for set_delegate
- **Widget**: add get/set_layout_direction
- `get_css` method for Gradient subclasses
- **Gradient**: add set_color_at method
- **StandardItemModel**: allow negative indexes for \__getitem__
- **GridLayout**: allow negative indexes for (int, int) and int indexer
- **Widget**: add set_width / set_height methods
- add GridSplitter
- **ProxyComparerWidget**: add link_selections kwarg
- **AbstractItemView**: allow None for set_delegate
- **ProxyComparerWiget**: allow custom delegate for ItemViews
- **TabWidget**: add `add` method
- **ProxyComparerWidget**: add itemview kwarg
- **ProxyComparerWidget**: add is_tree kwarg
- **AbstractItemModel**: add is_descendent_of helper

### Fix

- **LogRecordModel**: correct time formatting
- **Cursor**: fix typo
- **MeltProxyModel**: emit signals when props change

## v1.52.0 (2023-07-05)

### Feat

- **SliceChangeIconSizeProxyModel**: also support QColors and QPixmaps for DecorationRole
- Slicing support for Image
- add VerticalLabel
- **WebEnginePage**: add insert stylesheet method
- add TwoListsSelectionWidget
- add mkdocs gen-pages plugin
- **SliceIdentityProxymodel**: also support tuples for indexer_contains
- add SliceMapRoleProxymodel
- **AbstractItemModel**: allow setting parent for index_from_key / get_index_key
- **FileDevice**: add some permission getters
- **AbstractItemModel**: fetch_more kwarg for iter_tree (no need for prefetch_tree anymore)
- **LinkedSelectionModel**: also map selection
- add SliceDisplayTextProxyModel
- add BrushEdit
- **IconProvider**: for_color supports QBrush
- **ItemSelectionModel**: add __contains__ method
- **Proxifer**: add map_from / map_to methods
- add LinkedSelectionModel
- **ProxyMapper**: allow more than 2 models for mapping

### Fix

- **SliceChangeIconSizeProxyModel**: use proper val for caching
- **TableToListProxyModel**: fix Verticalheader labelling
- Allow icons from all charmaps
- **SliceEdit**: fix step=None

## v1.51.0 (2023-07-01)

### Feat

- **WidgetsDetailsModel**: use checkstate role for bool values
- add PolarsTableModel
- add GitPythonTreeModel
- **ImportLibTreeModel**: add DistributionRole
- add spatialaudio module
- **SubClassTreeModel**: support UnionTypes
- **proxifier**: add highlight_current method
- **AnnotatedScrollBar**: support horizontal
- **StandardItem**: add is_checked / toggle_checkstate methods
- Properties for IntegerValidator / TextLengthValidator
- **ClassTreeModel**: add caching
- add ChangeHeadersProxyModel

### Fix

- **MetaObject**: fix offsets for MetaProps etc
- **SliceIdentityProxyModel**: row, column indexing instead of column, row
- use checkstate enum instead of True/False

## v1.50.0 (2023-06-27)

### Feat

- **TreeView**: add expand_all method
- **FilterHeader**: use NumFilterWidget for numerical columns
- **MultiColumnFilterProxyModel**: add support for callables
- add NumFilterWidget
- add ColumnOrderProxyModel
- **Proxifier**: add melt method
- add ProxyMapper
- add MeltProxyModel
- **PandasIndexFilterProxyModel**: add endswith filter mode
- **DateTimeAxis**: add some datetime-related methods
- **Object**: add bind_property classmethod
- add FunctionValidator
- **VariantDelegate**: add validator kwarg
- add StringListLineEdit
- **LineEdit**: add append kwarg
- **ProgressBarDelegate**: support choosing a custom role
- add RangeEdit and SliceEdit
- **Proxifier**: add change_icon_size
- **StandardItemModel**: set ItemPrototype to our own subclass
- **StandardItemModel**: add from_dict method
- **XmlModel**: also support lxml.etree
- slicing support for Grid/GraphicsGridlayout
- **Object**: types.UnionType support for Object.find_child
- **PathValidator**: add mode setting (any, file, folder)
- **LineEdit**: allow explicitely overriding empty handling for validators
- **Proxifier**: change set_read_only to a more general change_flags method

### Fix

- **Widget**: fix map_to/from("window", ...)
- **EnumFlagWidget**: fix behaviour for non-power-of-2 flags
- **EventLoop**: typo in execute()
- **TableToListProxyModel**: emit headerDataChanged signal on header change
- **EnumFlagWidget**: filter None to workaround Qt flag bug
- **DoubleValidator**: correct default for set_range decimals kwarg

## v1.49.0 (2023-06-21)

### Feat

- **ParentClassTreeModel**: add mro mode
- add SliceCheckableTreeProxyModel
- **ScrollAreaTocWidget**: show windowIcon
- **ScrollAreaTocWidget**: make header property user-settable
- **Proxifier**: add to_list method
- **PandasTableWithHeaderModel**: make multiindex_separator a property
- new fast PandasProxyModels
- **BaseIPythonWidget**: make completion_mode a property
- add some multimedia classes
- add SliceChangeIconSizeProxyModel
- **SortFilterProxyModel**: allow re.Pattern for setFilterRegularExpression
- search box for settings
- **MultiColumnFilterProxyModel**: support fuzzy and normal (startswith) mode.
- **MultilineLayout**: support different layout types
- add MultiColumnFilterProxyModel
- add FilterHeader (replaces FilterContainer)
- **TableToListProxyModel**: map headerData and allow setting custom header
- **debugging**: add proxy_comparer helper
- allow negative indexes for Layout.__getitem__
- **ScrollAreaTocWidget**: make highlight_font a property
- **qml**: add a helper to quickly expose all widgets to qml
- **PropertyAnimation**: add get_property_value method
- **Widget**: add map_to/from("window")
- **AbstractAnimation**: add toggle_direction method
- **ColorValuesProxyModel**: allow setting low/high color
- **helpers**: get_color_percentage works with arbitrary number of tuple elements now
- **Layout**: allow LayoutItems for add()
- add SliceFilterProxyModel
- add HighlightMouseProxyModel
- **TabWidget**: allow slicing
- **HeaderView**: allow indexing by section name
- slicing support for TabBar
- **Layout**: add get_items method
- **Proxifier**: add add_column method
- Slicing support for StackedWidget
- **HeaderView**: add HeaderWrapper
- **PushButton**: add set_action method
- add AutoresizingTextEdit
- add ConfigWidget
- Slice proxying
- add include_column kwarg to get_index_key
- add ColorValuesProxyModel
- add ModelIndexModel
- add DisplayMode setting to FlattenedTreeProxyModel
- **Proxifier**: add flatten method
- **Object**: add properties_set_to context manager
- **AbstractItemModel**: add get_breadcrumbs_path
- **ImportlibTreeModel**: show markers
- **TreeModel**: support TreeItem subclasses
- **AbstractItemModel**: depth kwarg for prefetch_tree
- **Treeview**: add set_expanded method (which also takes Iterables)
- **AbstractItemModel**: depth kwarg for search/iter_tree
- **Object**: add signal_blocked method
- **AbstractItemModel**: add get_child_indexes method
- **VariantDelegate**: make setting EditRole optional
- **ToolBox**: add slicing support
- **GraphicsLayout**: add slicing support
- **AnimationGroup**: add targetObject method
- **ListWidget**: add slice support
- **ToolBar**: add __getitem__ including slicing
- **BaseListDelegator**: support slicing
- support slicing for layouts
- **Splitter**: allow slicing
- add listdelegators module
- **TextCursor**: add join_previous kwarg for edit_block
- **TextCursor**: add __contains__ method
- add FrameInfoModel class
- add show method
- add TextAnimation class
- **PygmentsHighlighter**: make style a property
- add EmojiIconEngine class
- **Locale**: add get_flag_unicode method
- **Locale**: add get_country method
- **Fx**: infer type for transition methods
- **Font**: add as_qt kwarg for mono()
- **ListMixin**: support slices for __getitem__
- add SubClassTreeModel / ParentClassTreeModel
- add PydanticFieldsModel
- add PydanticModel
- **Settings**: allow nesting settings objects
- add AstViewer
- add two models for attrs
- **fx**: add transition_to/from methods
- add OptionsValidator
- **RegularExpression**: add to_py_pattern method
- **VariantAnimation**: add append_reversed method
- add MultiComboBox
- **AbstractItemModel**: add get_index_key / key_from_index methods
- **Layout**: groupbox for ContextLayouts
- **MetaObject**: also accept snake case for get_property etc
- **MetaProperty**: add get_python_type method
- **SequentialAnimationGroup**: add reverse / reversed / append_reversed methods
- **Stalker**: work with non-prettyqt widgets
- **QObjectDialog**: widget click sets focus on HierarchyView
- add ZoomAnimation
- **VariantAnimation**: add reverse/reversed methods
- fx delegate for widgets
- **Widget**: add data kwarg to add_action
- add delay kwarg to play_animation
- **ScrollBar**: add can_scroll method
- add some ScXml classes
- **HighlightCurrentProxyModel**: make highlight color configurable
- **HighlightCurrentProxyModel**: add "row" as mode option
- add XmlModel
- **ScrollArea**: make get_visible_widgets work with base QWidgets
- add AstModel class
- **TextCursor**: allow tuples for select_text
- **TextCursor**: allow tuples for set_position
- **TabWidget**: add create_tab_preview method
- add two models for displaying dataclasses
- **WidgetPropertiesModel**: add Stored column
- **Locale**: add get_c_locale method
- **Object**: only_nonempty kwarg for get_properties
- **MetaObject**: extended get_properties filter functionality
- **MetaObject**: added get_all_super_classes method
- **Object**: allow predicates for find_children property selector
- **RegularExpression**: allow re.Pattern in ctor

### Fix

- **ColumnItemModel**: prevent namespace issues
- **TextDocument**: method somehow landed in wrong class
- **MultiColumnFilterProxyModel**: fix non-fuzzy str search
- **AstModel**: correct has_children check
- **Object**: fix check in get_properties
- **ScrollbarTocWidget**: highlight rows when shown
- **RenderLinkDelegate**: correctly clip text
- **ClassTreeModel**: catch another exception
- **KeySequenceEdit**: return correct type
- **AnimationGroup**: fix slicing support
- **DebugMode**: hide frame when menu closed
- **CycleWidget**: fixed scroll issue
- **FilterContainer**: editor width fix
- **FilterContainer**: pass object_name to parent in __init__
- **AbstractItemView**: fix incorrect type in size_hint_for_column
- **Spanslider**: qt6 related stuff

## v1.48.0 (2023-06-08)

### Feat

- make ProcessEnvironment a MutableMapping
- **TableView**: add margin kwarg to get_visible_section_span / resize_visible_columns_to_contents
- **AbstractItemView**: add get_visible_section_span
- **AbstractTableModel**: add to_dataframe method
- **AbstractItemModel**: add prefetch_tree method
- checks module
- Windows contextmenu stuff

### Fix

- **show_root**: properly reset before hiding

## v1.47.0 (2023-06-07)

### Feat

- **AbstractScrollArea**: add add_scrollbar_widget method
- add AnnotatedScrollBar
- **TextEditSelecter**: add __getitem__
- **PlainTextEdit**: add get_visible_line_span
- add MonotonicListValidator
- add some pandas widgets
- add PrintSupport classes
- **PlainTextEdit**: add get_pixel_height method
- quick shot for a PreviewScrollBar
- Add ScrollAreaTableOfContentsWidget
- **AbstractItemModel**: add max_results kwarg for search_tree
- **Object**: property selector kwarg for find_children
- **Widget**: add map_to and child_at methods
- **ScrollArea**: always use Widget for viewport, add get_visible_widgets
- return handles for AbstractItemView.sync_with
- **AbstractItemView**: always use our subclassed ItemSelectionModel
- make settings a proper MutableMapping
- **Layout**: add item_at method
- add SectionAutoSpanEventFilter
- **AbstractItemView**: add sync_with method
- add OrientedTableView
- add AutoSizeColumnsEventFilter
- allow setting eventfilters by name
- **TextDocument**: add get_pixel_height method
- **TableView**: add resize_visible_columns_to_contents method
- getattr for core, gui, widgets modules
- **AbstractProxyModel**: add get_source_model method
- **TableView**: add get_visible_section_span
- **Pixmap**: add save_to_file method
- **VariantDelegate**: support numpy integers
- add DataFrameEvalFilterProxyModel
- **TableView**: add auto_span method
- max colcount by default for resizeColumnsToContents
- **DataFrameViewer**: use numpy for span detection
- **MetaObject**: add forward_signals kwarg to copy
- **MetaObject**: also allow copy for widgets which need orientation
- bit NumPy support for VariantDelegate
- add HighlightCurrentProxyModel
- **GuiApplication**: add find_window method
- add UrlLineEdit
- allow str for RegularExpressionValidator ctor
- **TreeView**: add show_root method
- start with pandas stuff
- **AbstractItemView**: add get_size_hint_for_column
- **AbstractProxyModel**: add remove method
- add ReadOnlyProxyModel
- **MessageBox**: add get_button method
- **LineEdit**: allow QRegularExpressions for set_validator
- **Validator**: add strict mode
- **AbstractItemModel**: add iter_tree / search_tree methods
- **AbstractItemView**: add iter_tree method
- **Stalker**: add some event signals
- add TextLength/AlphaNumericValidator
- add Hex/QssValidator
- allow showing different content for show_tooltips
- add Int/Float LineEdits
- allow setting validator by str
- **TextEditSelecter**: add highlight_matches method
- MenuBar for QObjectDetailsDialog
- **SidebarWidget**: allow Actions for add_action
- prep some Actions for Mainwindow
- **FilterContainer**: add set_filter_mode method
- **Stalker**: make log_level a prop
- add ColumnJoinerProxyModel
- fuzzy filter support in "regular" SortFilterProxyModel
- add AppearanceProxyModel class
- add SpanTableView
- add BackingStore
- add RectFEdit
- **AbstractItemView**: add get_proxies method
- **TableView**: add is_cell_visible method
- **HeaderView**: add is_in_visual_range method
- show widget borders in debug mode
- **KeyCombination**: add __add__ method
- **AbstractItemModel**: add is_checkstate_column method
- add some proxy models
- ensure_visible kwarg for (Plain)TextEdit
- **colors**: quick access to setting color roles
- **TextEditSelecter**: end_pos kwarg for goto_line
- add qobjectsdetailsdialog
- **AbstractItemView**: extend set_model
- **MetaObject**: add connect_signals method
- **MetaObject**: add only_notifiers kwarg for get_signals
- **TextBrowser**: add get_source_type method
- **CommandPalette**: add for_path method
- automatic registration for delegates
- **Widget**: add "border" as set_layout option
- move all proxy stuff to Proxifier delegate
- **Widget**: allow setting margin in ctor
- **AbstractItemView**: make role a kwarg for current_data/selected_data
- add FlattenedTreeProxyModel
- add StretchButtonToolBar
- add CrossFadeWidget
- add AdjustingBoxLayoutDockWidget

### Fix

- **Settings**: raise KeyError for non-existing keys
- fix create_char
- add missing import
- typo
- **DataFrameEvalFilterProxyModel**: always get the root sourcemodel
- **ColorDialog**: fix replacing QColorShower stuff
- **SidebarWidget**: correct signature for add_action
- **WidgetHierarchyModel**: only return direct children
- **HeaderView**: fix toggle-vis context menu
- add workaround for missing parent() methods when using PyQt
- QAbstractProxyModel is part of QtCore
- dont mask QObject.parent()
- **StackedWidget**: fix fade animation
- **WidgetHierarchyModel**: missed to adjust columnCount for extra column

## v1.46.0 (2023-05-24)

### Feat

- add ActionGrid
- **StandardItem**: add get/set_text_alignment
- **HeaderView**: add get_section_for_label method
- add DefaultDropdownAction
- add PredicateFilterProxyModel
- **MetaObject**: only_writable kwarg for get_properties
- add ValueTransformationProxyModel
- add SubsetFilterProxyModel
- **AbstractItemView**: add get/set_state
- add LineEditFilterContainer
- add TableToListProxyModel
- **AbstractItemModel**: add get_model method
- add WidgetHierarchyModel
- add MultiLineLayout
- **AbstractItemView**: add get_drop_indicator_position
- **Layout**: add clear method
- **Font**: add scaled method
- **SignalMapper**: add __delitem__ method
- add ListViewGridResizeEventFilter

### Fix

- **GraphicsScene**: fix _get_viewer_zoom without viewer
- **WaitingSpinner**: correctly position on parent

## v1.45.0 (2023-05-23)

### Feat

- **ShortcutsModel**: parent widget column

### Fix

- **AbstractItemModel**: fix transpose for PySide6
- **MetaType**: correctly cast in get_name

## v1.44.0 (2023-05-23)

### Feat

- **Widget**: add highlight_widget method
- add FocusWidget
- add MappingModel
- **DateTime**: add from_seconds method
- add LogRecordModel
- **MetaMethod**: add get_parameter_types method
- **MetaObject**: add filter_shit kwarg for get_methods
- animation option for Cursor.set_pos
- add CursorMoveAnimation
- **Cursor**: add click method
- add SliderMoveToMouseClickEventFilter
- add test module
- **PopupInfo**: add icon support
- **EventCatcher**: allow str for eventtselection
- **Object**: add copy method
- for_palette method for Gradient
- **RubberBand**: add track widget method
- add WidgetDelegate
- **Object**: add copy method
- proper LocaleEdit
- **Locale**: add get_all_locales method
- add PainterPath.add
- **Widget**: support tuples for position_on
- **Cursor**: add set_pos method
- **Object**: add start_callback_timer
- add OrientedScrollArea
- add OverlayBorder
- add ScientificValidators
- rich_text param for set_tooltip
- **DateTimeEdit**: add set_to_today method
- add FuzzyCompleter
- List interface for ListMixin
- **AbstractItemModel**: two more context managers
- ShortcutsModel
- set ObjectNames in debugmode
- add OpenGLwidget
- **WidgetsDetailsModel**: automatically populate table based on most common ancestor.
- add WidgetsDetailsModel
- **AbstractItemModel**: make proxies easily available
- **ToolBar**: add show_tooltips method
- first shot for a WidgetPropertiesModel
- **Date**: add from_string method
- add EnumFlagWidget
- **Application**: add process_events method
- **MetaProperty**: add get_enumerator_type
- add debugmode eventFilter (WIP)
- **EventCatcher**: allow callable for do_filter
- **Object**: add connect_events method
- EventCatcher eventfilter
- Elision functionality for Label
- add JsonValidator / PythonCodeValidator / ColorValidator classes

### Fix

- **Cursor**: correct subclass check in set_pos
- **EnumComboBox/EnumFlagWidget**: only declare one user prop
- correctly init Url when arg is PathLike

## v1.43.0 (2023-05-18)

### Feat

- **Widget**: x/y_offset kwargs for position_on
- add FlashEffect
- auto kwarg suppport for Slot decorator
- **MetaMethod**: add get_normalized_signature method
- **Widget**: add show_tooltip method
- **Widget**: tool_tip kwarg for add_action
- **ToolBar**: add get_widgets method
- allow str in PropertyAnimation ctor

### Fix

- missed some testing shit
- correctly map in map_to_global

## v1.42.0 (2023-05-17)

### Feat

- **coreApplication**: add in_main_thread method
- **MetaObject**: add get_user_property method
- **MetaType**: add get_meta_object / get_meta_object_for_type
- add SignalList
- **MetaProperty**: add get_notify_signal / get_enumerator
- **Object**: keep track of eventfilters
- **GuiApplication**: add get_keyboard_modifiers / query_keyboard_modifiers
- **Application**: add widgets_at method
- first quick shot for a WidgetEditor
- allow initializing SizePolicy with strings
- NativeEventFilter for windows global hotkeys
- **KeySequence**: add get_key_bindings
- **KeySequence**: cast in __getitem__
- **KeySequenceEdit**: add get_key_combinations / get_finishing_key_combinations
- add some more prop-edit widgets
- **Drag**: return DropActionStr for main_loop
- animation feature for StackedWidget
- **Frame**: add set_frame_rect
- **MetaType**: get_type -> get_type_name and new get_type
- **JsonDocument**: add __format__ method
- embed quickref in RegexEditorWidget
- **IconBrowser**: use FuzzyFilter proxy
- **GroupBox**: add get_alignment method
- **FormLayout**: add get/set_label_alignment, get/set_form_alignment
- **Widget**: scale_ratio param for center_on
- context manager stuff for layouts
- **widgets**: add HBoxLayout / VBoxLayout classes
- **ActionsModel**: Usage count column
- add AsyncRunner
- add IPython stuff
- some helper stuff for ThreadPool
- **Dir**: add get_temp_path method
- merge widget center methods + rect support for mapToGlobal (map_to_global)
- **FileIconProvider**: custom_directory_icons methods
- prep some QtDesigner stuff
- **Widget**: add center_on_parent method
- some methods for StyleOptionViewItem
- **Action**: add usage counter and get_type
- **SortFilterProxyModel**: add invalidated signal

### Fix

- proper mono font for all platforms
- **ElidedLabel**: qt6 fix
- set_data for StandardItem / ListWidgetItem with wrong arg order
- **CommandPalette**: widgets from other sources can have parent as an attribute
- **QtWidgets**: fix binding of old methods
- **ButtonDelegate**: pass parent via kwarg
- **HtmlItemDelegate**: properly draw with icon
- **AbstractItemView**: fix some setfocus stuff
- **FuzzyFilterModel**: do not check html string for filtering

## v1.41.0 (2023-05-10)

### Feat

- **ColumnItemModel**: add set_columns method
- add FuzzyFilterModel
- add commandpalette
- **SortFilterProxyModel**: add setFixedFilterList method
- **SortFilterProxyModel**: override lessThan to allow sorting for more types
- **AbstractItemView**: add some methods to deal with ItemSelectionModel
- **Widget**: add set_focus method
- add ActionsModel class
- **StandardItem**: add set_data method
- **IconDelegate**: make item role configurable
- **Completer**: added path_updated signal
- **Completer**: add set_completion_role method
- **SortFilterProxyModel**: add set_filter_role method

### Fix

- **ColumnItemModel**: fix get_sort_value
- **ListWidgetItem**: fix set_data method
- **IconDelegate**: qt6 porting issue
- **HtmlItemDelegate**: qt6 porting bug
- **RenderLinkDelegate**: Qt6 fixes

## v1.40.0 (2023-05-09)

### Feat

- **Painter**: add draw_star, draw_diamond methods
- **PolygonF**: scale kwarg for create_star_diamond
- Constraints column for ImportLib model
- __format__ for different classes
- **Widget**: add set_graphics_effect method
- **core**: add LoggingCategory class
- **network**: add NetworkReply class
- add MaterialIconStyle class
- **InputMethod**: add query_focus_object method
- add GoogleCompleter
- add HTMLItemDelegate

### Fix

- **NestedItem**: set parent in append_child

## v1.39.1 (2023-05-08)

### Fix

- model cleanup

## v1.39.0 (2023-05-08)

### Feat

- re-work JsonModel
- add update_check
- some MessageBox work
- **SlideAnimation**: add start/end_value kwargs for ctor
- **Widget**: add play_animation method
- **PlainTextEdit**: extend set_syntaxhighlighter
- add CycleWidget
- add SelectedWordHighlighter class
- **PlainTextEdit**: better way to color focused line
- **bluetooth**: cover some more classes
- **ItemSelectionModel**: add set_current_index method
- scroll_to_item for Table/TreeWidget
- **AbstractScrollArea**: add set_viewport_margins method
- set_size for SvgGenerator and QuickItem

### Fix

- **Scintilla**: fix highlight_current_line
- **Color**: also inherit transparency when QColor for ctor
- typed signals seem to cast to Qt types

## v1.38.1 (2023-05-07)

### Fix

- **Chart**: used wrong call for setting style

## v1.38.0 (2023-05-07)

### Feat

- **TreeWidget**: add find_items method
- recursive and case_sensitive kwarg for ListWidget/StandardItemModel.find_items
- **HeaderView**: add set_sort_indicator method
- **VersionNumber**: add from_string method
- auto adjust Chart and PygmentsHighlighter colors to Palette
- **Palette**: allow disabling highlight_inactive

### Fix

- **HierarchicalHeaderView**: oops

## v1.37.1 (2023-05-06)

### Fix

- check for None-model in set_sorting_enabled

## v1.37.0 (2023-05-06)

### Feat

- **HeaderView**: some kwargs for set_resize_mode, add set_sections_movable method
- **TreeView/TableView**: add set_sorting_enabled method
- add HierarchicalHeaderView class
- **SortFilterProxyModel**: add get_sort_order method
- **Wizard**: add set_custom_button method
- make some basic types pattern matching compatible
- **SortFilterProxyModel**: more pythonic sort() kwargs

## v1.36.0 (2023-05-05)

### Feat

- **MimeDatabase**: add some new methods
- **SizePolicy**: add get_transposed method
- enable dark mode detection on linux
- **DataWidgetMapper**: add __setitem__, __getitem__, __delitem__
- **GuiApplication**: add set_progress_value method
- **quick**: add SGNode class
- **Window**: add some more methods
- **qml**: add QmlError / QmlExpression classes
- **qml**: add QmlProperty class
- **TreeWidgetItem**: add recursive option for get_children
- **TreeWidget**: add get_items method

### Fix

- **Completer**: fixed is_case_sensitive method
- correctly inherit for QuickView

## v1.35.0 (2023-05-05)

### Feat

- **Shortcut**: allow str for ctor
- **Shortcut**: add set_key(s) methods
- add add_shortcut methods for Window and Widget classes
- **gui**: add SurfaceFormat class
- **Locale**: add some methods
- **Locale**: add get_formatted_data_size

## v1.34.0 (2023-05-04)

### Feat

- **qml**: add QmlPropertyMap class
- **FsSpecModel**: filter columns depending on protocol
- **GraphicsView**: add zooming option
- add AccordionWidget

## v1.33.1 (2023-05-04)

### Fix

- test fixes

## v1.33.0 (2023-05-04)

### Feat

- **GraphicsScene**: add grid functionality
- add DebouncedSignal class
- **TabWidget**: allow QWidget for remove_tab
- **AbstractNativeEventFilter**: add install method
- add taskbaritem module
- **HoverIconEventFilter**: add pressed state
- **VariantDelegate**: deal with enums
- add EnumComboBox
- **Completer**: add set_strings method
- add FsSpecCompleter
- **Widget**: add get_win_id() method
- **TtextTableCell**: add get_first/last_cursor_position methods
- **LineEdit**: add set_completer method
- **Completer**: add get_completions() method
- **FsSpecModel**: add get_file_content method
- **KeySequence**: overload for to_shortcut_str
- **LineEdit**: add tab_pressed signal
- **qthelp**: add HelpFilterSettingsWidget class
- **Shortcut**: add get_keys method
- **TreeWidgetItem**: add collapse / expand / get_text_alignment methods
- **TableWidget**: allow QModelIndex for closePersistentEditor / isPersistentEditorOpen
- **TableWidgetItem**: add set_editable method
- **TreeWidget**: add some more methods
- **gui**: add TextBlockFormat class
- **TreeWidgetItem**: add some methods
- **GraphicsView**: add get_view_rect / get_pixel_size
- **GraphicsView**: add add_item / remove_item methods
- **GraphicsView**: set our own scene subclass by default
- **MimeData**: add to_dict and clone methods
- add VariantDelegate class

### Fix

- **TabBar**: qt6 regression (PointF instead of Point)
- **ColumnItemModel**: reset model in set_root_item
- **AwesomeFileIconProvider**: missed a case for icon()
- **AudioDevice**: fix get_channel_config
- **Charts**: dont use axisX / axisY (missing in qt6)
- **ButtonDelegate**: only apply to correct column
- **RegexInput**: catch exception when regex invalid

## v1.32.0 (2023-04-30)

### Feat

- **custom_widgets**: add RegexLineEdit class
- **PlainTextEdit**: emit text with value_changed signal
- **gui**: add TextTable, TextTableCell and TextTableFormat classes
- **ItemEditorFactor**: add create_extended method
- **QuickItem**: add __getitem__ and __contains__ methods
- **custom_widgets**: add ColorComboBox
- **ColorDialog**: add get/set_custom_colors methods
- **printsupport**: add Printer class
- **GuiApplication**: add palette_changed signal
- add QtPrintSupport to qt module
- **Splitter**: override createHandle so that our own subclass is used.
- **SplitterHandle**: add clicked signal
- **Palette**: add is_dark method
- add quickwidgets module

### Fix

- **FontChooserButton**: add missing button icon

## v1.31.0 (2023-04-29)

### Feat

- **FsSpecModel**: allow None for setRootPath
- **core**: add SharedMemory class
- **multimedia**: add AudioDevice class
- add __delitem__ for UrlQuery, Timeline and StackedWidget
- **QuickRenderControl**: add edit_frame context manager
- **PdfWriter**: add get/set_version methods
- **PagedPaintDevice**: add get_page_ranges and get_page_layout methods
- **Date**: add replace method
- **FileDevice**: add get_permissions method
- **gui**: add PageRanges class
- **PainterPath**: add get_simplified and to_reversed methods
- **Layout**: allow None for set_margin
- **GridLayout**: add alignment kwarg to add method
- add KeyCombinationEdit class
- **KeySequenceEdit**: allow QKeySequence for set_value
- **ToolBox**: add some kwargs to add_widget
- **Splitter**: some kwargs for add_widget method
- **Slider**: better mouseclick behaviour
- **Date**: add add_days, add_months, add_years and get_current_date methods
- **Time**: add add_msecs, add_secs and get_current_time methods
- **Label**: add clicked signal

### Fix

- **FsSpecModel**: fix root glob call
- **StarDelegate**: qt6 fix
- **Timeline**: Qt6 fixes
- **PlainTextEdit**: wheelEvent fix

## v1.30.0 (2023-04-28)

### Feat

- **AbstractScrollArea**: add set_scrollbar_smooth method
- add SmoothScrollBar class
- **AbstractScrollArea**: add scroll_by_pixels method
- **Cursor**: add fake_mouse_move classmethod
- **Widget**: add set_style method

### Fix

- **PlainTextEdit**: correctly propagate wheelEvent

## v1.29.0 (2023-04-27)

### Feat

- **CameraDevice**: add get_video_formats method
- re-introduce multimedia module
- **FsSpecModel**: add get_protocol_path method
- **Widget**: allow int index for insertAction
- **HeaderView**: add get_default_alignment and get_orientation methods
- **HeaderView**: add get_resize_mode method
- **ColorDialog**: some new methods
- **pdf**: add PdfSearchModel class

### Fix

- **Widget**: support several QOpenGlWidgets for get_image

## v1.28.1 (2023-04-26)

### Fix

- weird PySide6 issue with Enum val as default kwarg (PyQt works fine..)

## v1.28.0 (2023-04-26)

### Feat

- **Drag**: add set_drag_cursor and main_loop methods

## v1.27.0 (2023-04-26)

### Feat

- filesystemmodel mixin for FsSpecModel

### Fix

- **FsSpecModel**: always return correct type for permissions()

## v1.26.0 (2023-04-26)

### Feat

- **MimeData**: add get_urls method
- **MimeData**: add set_urls method
- **pdf**: add PdfBookmarkModel class
- **AbstractItemModel**: add get_role_names method

### Fix

- change SORT_ROLE and NAME_ROLE values to not conflict with FileSystemModel enums
- **MimeData**: __getitem__ and __setitem__ seem to cause issues?

## v1.25.0 (2023-04-26)

### Feat

- **custom_models**: add fsspec model
- **FileSystemModel**: add get_permissions method

## v1.24.0 (2023-04-26)

### Feat

- **Layout**: add add_widget method
- **Widget**: allow None values for set_min/max_size
- **TextStream**: add get/set_number_flags methods

## v1.23.0 (2023-04-25)

### Feat

- **core**: Add ModelRoleData class
- add ImportlibTreeModel

### Fix

- correctly behaving listmixin

## v1.22.2 (2023-04-25)

### Fix

- **NestedModel**: add default value for index kwargs
- correctly behaving RegexMatchesModel

## v1.22.1 (2023-04-25)

### Fix

- **NestedModel**: rowCount fix

## v1.22.0 (2023-04-25)

### Feat

- **LayoutItem**: add get_expanding_directions method
- **LayoutItem**: add get_control_types method
- **GraphicsLayoutItem**: add get/set_size_policy and __bool__ methods

### Fix

- **Pixmap**: fix create_char method

## v1.21.0 (2023-04-23)

### Feat

- **NetworkRequest**: support some attributes from newer qt versions
- **NetworkRequest**: add set_attribute(s) method
- **Object**: add set_properties method
- **MimeData**: add for_file method
- **TextDocument**: add get_bytes method
- **MetaMethod**: add get_parameters/get_return_types methods
- **MetaObject**: add get_class_info method
- **MetaObject**: add get_super_class method
- **UrlQuery**: add __getitem__ and __setitem__ methods
- **TextDocumentWriter**: add serialize_document method
- **Widget**: add toggle_maximized method

### Fix

- correct isinstance check for to_json
- **TextDocumentWriter**: fix serialization
- **SingleApplication**: TextStream.setCodec gone in qt6

## v1.20.0 (2023-04-22)

### Feat

- add some methods for Thread/ThreadPool [81795](https://github.com/phil65/PrettyQt/commit/8179503530cd6290546b28edee6045b46d2d3237)
- **Pixmap**: get rid of flags param for from_image [8fbbf](https://github.com/phil65/PrettyQt/commit/8fbbfb35f6af5b37554f5a8944efa061dd8f9c1f)
- **bluetooth**: add BluetoothDeviceInfo class [80482](https://github.com/phil65/PrettyQt/commit/80482f0e31e72bc04e65813e61a670bf488b7221)

### Fix

- **BluetoothDeviceDiscoveryAgent**: correctly set flags for start_discovery [4f53b](https://github.com/phil65/PrettyQt/commit/4f53be680fcdaa2deec2cee1b941fb79ee7876a0)

## v1.19.0 (2023-04-22)

### Feat

- **MenuBar**: add get/set_corner_widget methods [a9fc0](https://github.com/phil65/PrettyQt/commit/a9fc04fca144beb7de5937a201422213e4fb53f8)
- **PdfView**: add set_file method [c5b79](https://github.com/phil65/PrettyQt/commit/c5b79c0791dcaf1114f436675cda9a6118b514e6)

## v1.18.0 (2023-04-21)

### Feat

- **ScrollerMetrics**: add get_scroll_metrics method + bit dict interface [838d6](https://github.com/phil65/PrettyQt/commit/838d650bb10de97ed32b4084d1e5a1d005b2c664)
- **WebEngineSettings**: more dict interface [903d7](https://github.com/phil65/PrettyQt/commit/903d78632c98b3b7812cfd82aacc0b86ab6fd5a9)
- **GuiApplication**: add set_badge_number method [57e9b](https://github.com/phil65/PrettyQt/commit/57e9b9e41687c969890c79d54f3bd7e59dd7c204)

### Fix

- make sure to correctly set parent for actions added to menus [8ea43](https://github.com/phil65/PrettyQt/commit/8ea4384d81e27a610604d441f14b765b5f333f80)
- **HeaderView**: context menu fix [c71c2](https://github.com/phil65/PrettyQt/commit/c71c2d744d842e39c011b88d203ff1b74c332ab5)

## v1.17.0 (2023-04-21)

### Feat

- **Image**: add to_ndarray method [ea556](https://github.com/phil65/PrettyQt/commit/ea556d1c6acc980930b5f6c17ae818451f9f9fd7)
- **Widget**: add get_cursor method [4dc77](https://github.com/phil65/PrettyQt/commit/4dc77ed75cf4fb61726a02d6d18563aa6dad890c)
- **Image**: add convert_to_format method [f36f1](https://github.com/phil65/PrettyQt/commit/f36f1355c73eed635f13cd833595b99527019909)

### Fix

- **ImportlibDistributionModel**: avoid duplicates in requirements [d27d2](https://github.com/phil65/PrettyQt/commit/d27d2642d4b320eaa9dccddd091eb4f3ff36f6c0)

## v1.16.0 (2023-04-21)

### Feat

- **AbstractItemView**: add get_horizontal/vertical/scroll_mode methods [bf664](https://github.com/phil65/PrettyQt/commit/bf664c4e9a4fcbe8830102f3272f19f620cc0d13)
- **AbstractItemView**: added model_changed signal [79b24](https://github.com/phil65/PrettyQt/commit/79b24d8ace40f8d473f04a5db674a8ceb62f7efc)
- **Scroller**: add grabbed_gesture method [c3041](https://github.com/phil65/PrettyQt/commit/c3041897be61300fd598ab2b0cb88ecd0395b5bd)
- add pdf and pdfwidgets modules [de15b](https://github.com/phil65/PrettyQt/commit/de15b89a950d5510b15606269683e32bbc4bd8ea)
- **MetaProperty**: add get_meta_type method [9242c](https://github.com/phil65/PrettyQt/commit/9242c01cc13f616fed257dda14f41eba4e214eb8)
- **GeoPolygon**: add get_hole_path / get_perimeter methods [8910a](https://github.com/phil65/PrettyQt/commit/8910a22fb995f1a931faae8b3971d65ec9fb49e7)

## v1.15.1 (2023-04-20)

### Fix

- **IconBrowser**: correctly build charmap dict [49e18](https://github.com/phil65/PrettyQt/commit/49e183410c79dcfcf65d667d284fbb2532065947)
- **GraphicsEllipseItem**: fix get_rect type issue (got broken with qt6) [69653](https://github.com/phil65/PrettyQt/commit/6965326cbfc22078dfeb2e0586a45c01ea0a957a)

## v1.15.0 (2023-04-20)

### Feat

- **Object**: add get_properties method [2fafb](https://github.com/phil65/PrettyQt/commit/2fafb5515fb1155409b503f5a400ff7a0f908773)
- **Image**: add from/to_pil methods [eb342](https://github.com/phil65/PrettyQt/commit/eb342e965c4bc5b7929b5d0baa6b0e7910516fba)
- **Object**: add get_dynamic_properties method [7c82b](https://github.com/phil65/PrettyQt/commit/7c82ba9191bb45197b2abae12fe717a3f401e01e)
- **PropertyAnimation**: allow passing the qt property method directly for apply_to [1ca12](https://github.com/phil65/PrettyQt/commit/1ca12880e3883d45704a22873db6c864befecaf4)

### Fix

- **MetaObject**: offsets were off by 1 [cecd7](https://github.com/phil65/PrettyQt/commit/cecd70330ca0a6ee78d064056e0bb525fd3fb250)

## v1.14.3 (2023-04-20)

### Fix

- another release fix :) [af959](https://github.com/phil65/PrettyQt/commit/af959d4063b8040299a790d65c31bcb644362034)

## v1.14.2 (2023-04-20)

### Fix

- another release fix [bdc10](https://github.com/phil65/PrettyQt/commit/bdc1085d98a6e03956dff0679674c704bc716151)

## v1.14.1 (2023-04-20)

### Fix

- release pipeline fix [bcfd8](https://github.com/phil65/PrettyQt/commit/bcfd8737e6cff2016def568c57953598eec0e8d6)

## v1.14.0 (2023-04-20)

### Feat

- **WaitingSpinner**: register some attributes as Qt Properties [d3b25](https://github.com/phil65/PrettyQt/commit/d3b2542d2011a23f5c2cf76683c88449a0da5e35)
- **TableWidget**: also support indexes for openPersistentEditor [d450d](https://github.com/phil65/PrettyQt/commit/d450d40d9713d0771861ec03f6bf1f130d56bdc2)

### Fix

- **RadioDelegate**: property doesnt accept bytes (anymore) [25a96](https://github.com/phil65/PrettyQt/commit/25a962c6cab32bf65234d3689dd417bb00333968)
- **Painter**: fix draw_rounded_rect method [bb883](https://github.com/phil65/PrettyQt/commit/bb88306049a42fc999dc050953569e7d7f7ec5df)

## v1.13.1 (2023-04-20)

### Fix

- fix tests... [58c78](https://github.com/phil65/PrettyQt/commit/58c78daf3d039bf08c04b02c1af21abead582f87)

## v1.13.0 (2023-04-20)

### Feat

- **ButtonDelegate**: no need anymore to open persistent editors [78984](https://github.com/phil65/PrettyQt/commit/789841de7811e5d0b0df3e47a5ce14559e2a182a)
- **AbstractTableModel**: add __getitem__ method to return indexes [0b9be](https://github.com/phil65/PrettyQt/commit/0b9be2ba8b24e51467a62d3cdccc7e7fc3ddf41f)

## v1.12.1 (2023-04-19)

### Fix

- **Widget**: missing string cast for set_stylesheet [e536b](https://github.com/phil65/PrettyQt/commit/e536beec652473b8c8f6d546a1781f1bc0b293a1)

## v1.12.0 (2023-04-19)

### Feat

- **ColumnItemModel**: inherit some stuff from ListMixin

## v1.11.0 (2023-04-18)

### Feat

- **LineEdit**: allow some special values for set_input_mask
- **Locale**: add get_measurement_system

### Fix

- **ColumntItemModel**: always return correct rowCount

## v1.10.0 (2023-04-18)

### Feat

- **ColumnItemModel**: methods for setting data
- **TreeItem**: add __iter__ method

### Fix

- **AttributeModel**: checkstate instead of text for is_attribute
- **UndoStack**: raise KeyError instead of returning it

## v1.9.2 (2023-04-17)

### Fix

- **StorageInfoModel**: move some stuff to baseclass

## v1.9.1 (2023-04-17)

### Fix

- **ColumnItemModel**: fix wrong value for non-listed roles in data()
- **ObjectBrowser**: re-add DEFAULT_ATTR_DETAILS and inspected_node_is_visible

## v1.9.0 (2023-04-17)

### Feat

- **custom_widgets**: add FileTree class
- **AbstractItemModel**: add update_all method

### Fix

- **IconDelegate**: fix exception when QIcon is passed

## v1.8.1 (2023-04-17)

### Fix

- user_data fix

## v1.8.0 (2023-04-17)

### Feat

- **ColumnItemModel**: add user_data to ColumnItems

## v1.7.1 (2023-04-17)

### Fix

- fix docs generation

## v1.7.0 (2023-04-17)

### Feat

- **ColumnItemModel**: add support for sort value and tooltips
- **Widget**: add grab_mouse_events / grab_keyboard_events context managers
- **Painter**: add some convenience methods

## v1.6.0 (2023-04-16)

### Feat

- **Widget**: add delete_children method
- **Url**: add is_special_url and _has_explicit_scheme methods
- **Application**: add set_style method
- **Scrollbar**: add scroll_to_next/previous_row methods
- **Uuid**: add to_string method

### Fix

- **Application**: correct icon colors for new Qt built in dark mode (when using Fusion theme)
- **ChartView**: correct cursor shape for dragging movements

## v1.5.0 (2023-04-13)

### Feat

- **TimeZone**: add get_time_spec method
- **TextDocument**: add get/set_meta_information methods
- **ListWidgetItem**: add set_text_alignment method
- **DirIterator**: add get_file_path / get_file_info methods

### Fix

- **FileSystemModel**: fix yield_child_indexes method

## v1.4.2 (2023-04-12)

### Fix

- only run tests on linux for now

## v1.4.1 (2023-04-12)

### Fix

- remove codecov from deps

## v1.4.0 (2023-04-12)

### Feat

- **Color**: add convert_to method
- **Color**: add get_spec method
- **core**: add KeyCombination class
- re-add qthelp module

### Fix

- fixed Color.as_qt error with Qt6.5

## v1.3.0 (2023-04-11)

### Feat

- add some set_origin methods
- add some set_transform methods
- **Brush**: add set_style method

## v1.2.0 (2023-04-11)

### Feat

- re-enable texttospeech module
- **gui**: add AbstractFileIconProvider class
- **core**: add MetaType class
- **gui**: add StyleHints class

### Fix

- correct filtering for Dir.get_entry_info_list
- **Dir**: explicitely use kwargs for entryList/entryInfoList calls
- prevent namespace collisions with builtin locale package

## v1.1.2 (2023-04-10)

### Fix

- always pass sys.argv to QCoreApplication etc

## v1.1.1 (2023-04-10)

### Fix

- Qt6 fixes for Dialog classes

## v1.1.0 (2023-04-10)

### Feat

- **Image**: add as_bytes method

## v1.0.0 (2023-04-07)

### Feat

- MultimediaWidgets for Qt6
- get rid of mro fuckery
- re-add location module

### Fix

- remove title property for widgets
