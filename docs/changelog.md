## v1.56.2 (2023-07-25)

### Fix

- longer timeout when building docs

## v1.56.1 (2023-07-25)

### Fix

- use pypi mknodes version

## v1.56.0 (2023-07-25)

### Feat

- use Property info for docs
- Globber for ItemModels
- add TupleTreeModel
- **ProgressBarDelegate**: make total and role a Property

### Fix

- **FilterHeader**: prevent name clash
- **Widget**: add missing Mixin

## v1.55.0 (2023-07-13)

### Feat

- first quick shot for GitPythonCommitTreeModel
- **OptionalWidget**: add value_changed signal
- **MetaEnum**: add get_scope_object and list_options methods
- **Object**: add get_qt_base_class method

### Fix

- fix link creation

## v1.54.0 (2023-07-11)

### Feat

- add SliceToMarkdownProxyModel
- **HtmlItemDelegate**: also support some markdown flavors
- custom LinkReplacer plugin for mkdocs
- add SliceColorCategoriesProxyModel
- **Palette**: add yield_colors method
- **markdownhelpers**: add get_dependency_table method
- add ModuleInfoModel
- **ColumnOrderProxyModel**: allow str for indexes
- **Widget**: add grab_example_pixmap classmethod

### Fix

- **SliceMapRoleProxyModel**: avoid recursive loop
- **SliceChangeFlagsProxyModel**: emit ChangeLayout when props change
- **spatialaudio**: fix some c&p errors
- **DesktopServices**: wrong module for QUrl
- **Stalker**: disconnect on destroyed signal
- **docs**: fix table headers

## v1.53.2 (2023-07-07)

### Fix

- **docs**: rem duplicate lines

## v1.53.1 (2023-07-07)

### Fix

- **build**: install addons for docs build

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
