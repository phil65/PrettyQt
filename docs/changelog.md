## v0.186.0 (2021-11-11)

### Feat

- **WebEnginePage**: add some more methods
- **Color**: add get_name method
- **iconprovider**: add __dir__ and __getattr__ methods to iconsets
- **TextDocument**: add some more methods
- **TextBlock**: add __str__ method
- **Process**: add get_process_environment method
- **qml**: add clear_type_registrations method
- **FileIconProvider**: support os.PathLike for get_icon
- **custom_widgets**: add SubsequenceCompleter class
- **Completer**: add set/is_case_sensitive methods
- **custom_models**: add SubsequenceSortFilterProxyModel class
- **SortFilterProxyModel**: add set_sort_role method

## v0.185.0 (2021-11-04)

### Feat

- add QT_VERSION var to qt module

### Fix

- **core**: dont shadow builtin libraries

## v0.184.0 (2021-10-30)

### Feat

- **qt**: add flag_to_int method
- **debugging**: add is_deleted fn
- **TextEdit**: add get_text_cursor method
- **PlainTextEdit**: add get_text_cursor method
- better package support by using importlib.resources for resource files
- add qt.set_env_vars
- fallback to installed qt package in case environment var QT_API is invalid / empty
- **TextBlock**: add some methods related to syntax highlighting
- **HeaderView**: add section_resized_by_user signal
- **Widget**: add resized signal
- add StandardIconsWidget class
- **TextCursor**: add get_cursor_position method
- **SyntaxHighlighter**: add get_current_block / get_format
- **Process**: add edit_environment method
- **Widget**: rename get/set_context_menu_policy methods
- **TextLayout**: add get_text_option method
- **TextDocument**: add some more methods
- **TextCursor**: add __str__ method
- **StandardItemModel**: add create_single_item_model classmethod
- **ProcessEnvironment**: add update() / items() methods
- **Color**: add drift_color classmethod
- **PlaintextEdit**: TextDocument by default
- **PlainTextEdit**: add show_whitespace_and_tabs method
- add mimetype_icon fn for FileIconProvider
- Add MenuRecentFiles class
- update iconsets

### Fix

- **TextCursor**: correctly convert EOL in __str__
- qt6 flag fix
- typo in AwesomeFileIconProvider

## v0.183.6 (2021-10-26)

### Fix

- more qt compat stuff
- generate docs on py3.9

## v0.183.5 (2021-10-12)

### Fix

- only test on 3.9 / macos10

## v0.183.4 (2021-10-12)

### Fix

- dont use poetry pre version

## v0.183.3 (2021-10-12)

### Fix

- qt6 compat
- some flag fixes

## v0.183.2 (2021-02-05)

### Fix

- another try to fix docs generation

## v0.183.1 (2021-02-05)

### Fix

- fix docs generation

## v0.183.0 (2021-02-05)

### Feat

- **JSEngine**: add eval method
- **Pixmap**: add rotated method
- **ColorDialog**: add replace_qcolorshowlabel
- **JSValue**: add __call__ method
- **PlainTextEdit**: add some more methods
- **core**: add Slot method
- **core**: add Mutex/Semaphore classes
- **LineEdit**: add some signals
- **svg**: add SvgWidget class

### Fix

- correctly keep state when using block_signals / updates_off context managers

## v0.182.1 (2021-01-26)

### Fix

- colors fix

## v0.182.0 (2021-01-26)

### Feat

- **Image**: add invert_pixels method
- **Color**: invert_alpha param for inverted method
- **MetaObject**: type_filter kwarg for get_methods
- **core**: add MetaProperty class
- **MetaObject**: include_super param for get_ methods
- **ItemEditorFactory**: add property_name kwarg to register_editor method
- **TabWidget**: add update_tab_bar_visibility method
- **Pixmap**: add from_image method
- **MessageBox**: add some constants
- **MessageBox**: add set_escape/default_button methods
- **MessageBox**: add get_icon_pixmap method
- **svg**: add SvgRenderer class
- **Image**: add from_ndarray method

## v0.181.0 (2021-01-23)

### Feat

- **Color**: add is_dark and inverted methods
- **Dir**: add set_search_paths method
- **Palette**: add inverted method
- **Dir**: add add_search_path method
- **core**: add AbstractNativeEventFilter

## v0.180.0 (2021-01-20)

### Feat

- **TextDocument**: add some methods related to default stylesheet editing
- **PygmentsHighlighter**: add repr method
- **PygmentsHighlighter**: add style kwarg
- **QtCore**: add QClassInfo for PyQt5/6
- **colors**: add interpolate_text_colors fn
- **Color**: add from_hsv method
- **gui**: add Drag class
- **DataWidgetMapper**: add get_mapped_property_name method
- **DataWidgetMapper**: add add_mapping method

## v0.179.0 (2021-01-18)

### Fix

- RegexInput flags fix
- **ModelTester**: correctly disconnect model

### Feat

- **Painter**: more kwargs for set_pen method
- **Pen**: allow custom dash pattern for set_style
- **ItemEditorFactory**: add register_default_editor method
- **GraphicsItem**: add set_scale method
- **Pixmap**: add create_checkerboard_pattern method
- **ColorDialog**: add get_qcolorshower/get_qcolorshowlabel methods
- **TableWidgetItem**: add set_tooltip method

## v0.178.0 (2021-01-14)

### Feat

- **IODevice**: add __len__ method
- **EventLoop**: throw exception when running twice
- **Color**: add to_qsscolor method
- **Color**: add interpolate_color method
- **Locale**: add get_system_locale / get_system_language methods
- use subclassed ItemEditorFactory as default factory

## v0.177.1 (2021-01-13)

### Fix

- test fix

## v0.177.0 (2021-01-13)

### Feat

- allow args for app() methods

## v0.176.0 (2021-01-13)

### Feat

- **Timer**: add start_timer method
- **Timer**: add set_interval method
- allow os.PathLike for using images in set_tooltip methods
- **Movie**: add get_supported_formats method
- **iconprovider**: add AwesomeQuickImageProvider class
- **iconprovider**: add AwesomeFileIconProvider class

## v0.175.0 (2021-01-12)

### Feat

- add prettyqtest
- **qml**: add register_qml_type method
- **AbstractSlider**: add set_auto_scroll_to_end method
- **GuiApplication**: add edit_palette context manager
- **Dir**: add get_entry_list method

## v0.174.0 (2021-01-11)

### Feat

- **core**: add FileSelector class
- **Dir**: add get_entry_info_list method
- **Resource**: add set/get_file_name and register_resource methods
- **Application**: add get_available_themes method

## v0.173.0 (2021-01-10)

### Fix

- correct icon color for dark mode

### Feat

- **custom_models**: add StorageInfoModel class
- **DataStream**: add get/set_status methods
- **custom_widgets**: add ElidedLabel class
- **Painter**: add get_font_metrics method
- **gui**: add TextLayout class
- add SyncedProperty class
- **Widget**: add get/set_window_file_path methods
- **widgets**: add SplitterHandle class

## v0.172.0 (2021-01-09)

### Feat

- **Application**: add set_theme method
- **gui**: add TextObjectInterface class
- **PyQt5**: import QEnum and QFlag classes
- **core**: add MetaMethod/MetaObject classes
- **widgets**: add FocusFrame class
- **quick**: add Quick(Async)ImageProvider classes
- **QmlEngine**: add some more methods
- **QmlApplicationEngine**: add load_file method

## v0.171.1 (2021-01-07)

### Fix

- comment out some event constants

## v0.171.0 (2021-01-07)

### Feat

- **GraphicsItem**: add get/set_cache_mode methods
- **GraphicsPixmapItem**: some additional methods
- **custom_widgets**: add BorderLayout class
- **widgets**: add WidgetItem class
- **LayoutItem**: add get_item method
- **LayoutItem**: add get/set_alignment methods
- **Style**: add draw_primitive method
- **StyleOption**: add based_on method

### Fix

- **AutoSlot**: use typing.get_type_hints

## v0.170.0 (2021-01-05)

### Feat

- **Validators**: also allow Pattern for set_regex
- add tile rule constant
- add SingleApplication class
- **custom_widgets**: add Notification class
- **TreeWidget**: add __contains__ method
- **HelpContentWidget**: add index_of method
- add __contains__ method to some widgets
- **ItemEditorFactory**: add register_editor method
- **widgets**: add ItemEditorCreatorBase / ItemEditorFactory
- **types**: add Variant(Type)
- **VariantAnimation**: add set_range method
- **TextStream**: add read_lines method
- **TextStream**: add set_codec method

## v0.169.0 (2021-01-04)

### Feat

- **RegularExpressionMatch**: add get_match_type method
- **CoreApplication**: allow more types for version metadata
- **Windows**: add workaround for raising window
- **network**: add LocalSocket class

### Fix

- **CoreApplication**: fix setting metadata

## v0.168.0 (2021-01-03)

### Feat

- **eventfilters**: add AnimatedToolTipEventFilter class
- **Widget**: tooltip kwarg for set_flags method
- **AbstractAnimation**: add restart_animation method
- add custom_animations module
- **AbstractAnimation**: implement __and__ and __or__
- **Dir**: some additional methods

## v0.167.0 (2021-01-02)

### Feat

- **FileSystemModel**: add get_file_info and get_file_path methods
- add __fspath__ to Dir and FileInfo classes

## v0.166.1 (2021-01-01)

### Fix

- localization fixups

## v0.166.0 (2020-12-31)

### Feat

- **CoreApplication**: add get_available_languages and load_language methods

## v0.165.0 (2020-12-31)

### Feat

- **WebEngineView**: add register_as_browser method
- **WebEngineView**: ass some settings-related methods
- **Translator**: add load_file method
- add FramelessWindow class
- add webchannel module
- **qt**: add QtWebchannel module
- **widgets**: add FileIconProvider class
- add prettyqt.qt.QtUiTools module

## v0.164.0 (2020-12-29)

### Feat

- **CoreApplication**: add restart method

### Fix

- **FontDatabase**: make get_system_font a classmethod
- ObjectBrowser signal fix for Qt6
- **PdfWriter**: correctly inherit from Object and PagedPaintDevice

## v0.163.0 (2020-12-27)

### Feat

- **OperatingsystemVersion**: add __eq__ and __hash__ methods
- **VersionNumber**: add __hash__ method
- **FontDatabase**: add optional md5 check for add_font

### Fix

- revert CharIconPainter paint method for now

## v0.162.0 (2020-12-27)

### Feat

- **FontDatabase**: add additional check in add_font
- **Painter**: add offset_by and apply_transform context managers

### Fix

- **IconWidget**: update when setting size

## v0.161.0 (2020-12-26)

### Feat

- **LineEdit**: add add_action method
- **ListView/TableView**: add some more setters / getters
- **Painter**: add edit_pen context manager
- **PolygonF**: alternative ctors for diamond / star creation

### Fix

- **LabeledSlider**: call adjust_margins on correct object
- correct IconProvider init

## v0.160.0 (2020-12-25)

### Feat

- **gui**: add TextLine module
- **Doublevalidator**: add set_range method
- **IntValidator**: add set_range method
- **Pixmap**: add __eq__ method

## v0.159.0 (2020-12-24)

### Feat

- **LineEdit**: add set/get_cursor_move_style methods

## v0.158.0 (2020-12-22)

### Feat

- **iconprovider**: add reset_cache method
- **Widget**: add set/get_foreground/background_role methods
- **Application/Widget**: add set/get_stylesheet methods
- **Application**: add edit_stylesheet context manager

## v0.157.1 (2020-12-22)

### Fix

- SpanSlider fix

## v0.157.0 (2020-12-22)

### Feat

- **Painter**: add native_mode context manager
- **FontDatabase**: add add_font method
- **gui**: add IconEngine class
- **TabWidget**: add set_icon_size method
- **Icon**: allow more types for size param

## v0.156.0 (2020-12-21)

### Feat

- **RegularExpressionMatch**: add __bool__ method
- **custom_widgets**: add ObjectBrowser class
- **Timer**: add restart method
- **ListView**: add set_grid_size method
- **SortFilterProxyModel**: add is/set_filter_case_sensitive methods
- **AbstractItemView**: add set_icon_size method

## v0.155.0 (2020-12-20)

### Feat

- **Label**: add get_horizontal/vertical_alignment methods
- **GraphicsWidget**: add window_frame_section_at method

## v0.154.0 (2020-12-18)

### Feat

- add QtLocation and QtHelp to qt submodule
- **Dir/FileDialog**: add get/set_filter methods
- **InputDialog**: add get/set_input_mode and get/set_text_echo_mode methods

### Fix

- correct StarDelegate setModelData call

## v0.153.0 (2020-12-17)

### Feat

- **MediaPlayer**: add get_error method

## v0.152.1 (2020-12-17)

### Fix

- PySide2 workaround for non-recursive Object.findChild(ren)

## v0.152.0 (2020-12-16)

### Feat

- **Standarditem/StandardItemModel**: add enabled and editable kwarg to add_item methods
- **AbstractItemView**: add get/set_drag_drop_mode methods

## v0.151.0 (2020-12-16)

### Feat

- **ToolBar**: add add method
- **Icon**: add get_actual_size method
- **winextras**: add WinThumbnailToolButton class
- **ToolButton**: add set_menu method
- **Uuid**: add str method

### Fix

- PySide2 find_child(ren) fix

## v0.150.0 (2020-12-15)

### Feat

- **Movie**: add get_state method

## v0.149.0 (2020-12-15)

### Feat

- add HoverIconEventFilter class
- **positioning**: add GeoPositionInfo class
- **Icon**: add mode and state kwarg for add/get_pixmap
- **widget**: add set_mask method
- **core**: add FileSystemWatcher class
- **Palette**: add get/set_color_group methods
- **Brush**: add some addtional methods
- **Region**: add some additional methods
- **custom_delegates**: add RenderLinkDelegate class
- **TableWidgetItem**: add set_text_alignment method
- **Gradients**: add repr and some helper methods to gradient classes

### Fix

- PySide2 workaround for missing recursive param in findChild(ren)
- WebEngineHistory len fix for PySide2
- CategoryAxis len fix for PySide2
- correctly inherit LCDNumber

## v0.148.0 (2020-12-14)

### Feat

- **Widget**: add get/set_window_state methods
- **AbstractTextDocumentLayout**: add tuple support for hit_test point arg
- **TimeZone**: add get_display_name method
- **GuiApplication**: add get/set_high_dpi_scale_factor_rounding_policy methods
- **StandardItem**: add some new methods
- **AbstractButton**: add get_icon method
- **StandardItemModel**: add add_item method
- **StandardItem**: add get/set_checkstate methods
- **Window**: add start_system_resize method

## v0.147.2 (2020-12-14)

### Fix

- MacOs test fix

## v0.147.1 (2020-12-14)

### Fix

- MacOs test fix

## v0.147.0 (2020-12-13)

### Feat

- **ToolBar**: add get_allowed_areas method
- **WebEnginePage**: add some additional methods
- **WebEngineSettings**: add __delitem__ method
- **Application**: add send/post_event methods

## v0.146.0 (2020-12-13)

### Fix

- correctly serialize AbstractGraphicsShapeItem

### Feat

- **GuiApplication**: add get_icon method
- **PlainTextEdit**: add get(_line)_wrap_mode methods
- **GuiApplication**: add get_application_state method

## v0.145.0 (2020-12-11)

### Fix

- **GraphicsGridLayout**: serialize correctly
- **MediaRecorder**: use correct module in set_video/audio_settings
- correct constant naming
- install_exceptionhook fix

### Feat

- **GridLayout**: add get/set_origin_corner methods
- **BoxLayout**: add get/set_direction methods
- **NetworkCookieJar**: add __add__ and set_cookies_from_url methods
- **NetworkCookie**: add set_expiration_date method
- **Translator**: add __bool__ method
- **custom_widgets**: add RoundProgressBar class
- **DateTimeEdit**: add some more methods related to sections
- get/set_icon_size work for some widgets
- **CalendarWidget**: add set_range method
- **HeaderView**: add generate_header_id method
- **Widget**: add edit_palette contextmanager and get_font method
- **Palette**: add brush methods
- **custom_models**: add ImportlibDistributionModel class

## v0.144.0 (2020-12-09)

### Fix

- **Settings**: iter through key-value pairs
- correct inheritance for QuickItem
- **ColumnItemModel**: correct get_width signature

### Feat

- **qml**: add QmlImageProviderbase class
- **widgets**: add TreeWidgetItemIterator class
- **quick**: add some more classes
- **qml**: add QmlParserStatus class
- **Widget**: add get_title method
- **Painter**: add get_text_rect method
- **ListWidget**: add add_item method

## v0.143.0 (2020-12-08)

### Fix

- ObjectBrowser fix

### Feat

- implement __eq__ method for some more validator classes

## v0.142.1 (2020-12-07)

### Fix

- use our own SizeF class

## v0.142.0 (2020-12-07)

### Feat

- **SizeF**: add some methods to be on par with Size
- **Size**: add expanded_to method
- **CompositeValidator**: add some additional methods
- **custom_validators**: add __eq__ method to validator classes
- **TreeWidgetItem**: add some more methods
- **widgets**: add TableWidgetSelectionRange class
- **core**: add Calendar class
- **core**: add SignalMapper class
- **core**: add StateMachine class
- **core**: add LockFile class
- **core**: add JsonDocument/JsonValue classes
- **GeoCircle**: allow tuple in ctor
- **core**: add SocketNotifier class
- **widgets**: add Shortcut class

### Fix

- Correctly inherit StyleItemDelegate

## v0.141.0 (2020-12-03)

### Feat

- **core**: add Collator(SortKey) classes

### Fix

- github actions fix

## v0.140.4 (2020-12-02)

### Fix

- docs build fix

## v0.140.3 (2020-12-02)

### Fix

- docs deployment

## v0.140.2 (2020-12-02)

### Fix

- deploy check for github actions

## v0.140.1 (2020-12-02)

### Fix

- github actions: conditional deploy step

## v0.140.0 (2020-12-02)

### Feat

- **gui**: add ColorSpace class

## v0.139.0 (2020-12-02)

### Feat

- **FileInfo/Dir**: fallback to pathlib.Path methods
- **widgets**: add Proxy/CommonStyle classes
- **widgets**: add Gesture classes
- **core**: add TemporaryDir class
- **widgets**: add WhatsThis class
- **core**: add ItemSelectionRange class
- **FormLayout**: add some more methods
- **core**: add ProcessEnvironment class
- **gui**: add StaticText class
- **core**: add PauseAnimation class

## v0.138.0 (2020-12-01)

### Feat

- **core**: add ChildEvent / TimerEvent classes
- **core**: add IdentityProxyModel class
- **gui**: add SessionManager class
- **gui**: add InputMethod class
- **core**: add AbstractEventDispatcher class
- **widgets**: add StackedWidget class
- **widgets**: add some events
- **FileInfo**: add some additional methods
- **gui**: add Vector3D class
- **core**: add MimeType / MimeDatabase classes
- **core**: add SaveFile class
- **core**: add SignalBlocker class
- **core**: add TimeLine class
- **gui**: add Bitmap class
- **core**: add RandomGenerator class
- **FileDevice**: add get_error method
- **widgets**: add Dial class
- **widgets**: add RubberBand class
- **Wizard/WizardPage**: add some more methods
- **widgets**: add GraphicsRotation / GraphicsScale classes
- **widgets**: add GraphicsTransform class
- **widgets**: add LCDNumber class
- **widgets**: add Scroller(Properties) classes
- **core**: add CommandLineParser/Option classes
- **Pixmap**: add some more methods
- **gui**: add Screen class
- **Transform**: add some more methods
- add Abstract/PlainTextTextDocumentLayout classes
- **core**: add BasicTimer class
- **core**: add Resource class
- **core**: add StorageInfo class
- **core**: add ElapsedTimer class
- **core**: add CryptographicHash class

## v0.137.1 (2020-11-27)

### Fix

- doc build fix

## v0.137.0 (2020-11-27)

### Feat

- **core**: add OperatingSystemVersion class
- **PdfWriter**: add set_page_margins method
- **core**: add MarginsF class
- **core**: Add TextStream class
- **core**: add ByteArrayMatcher
- **AbstractItemModel**: add check_index method
- **PlaceManager**: add search_place method
- **core**: add app method
- add __bytes__ method to some classes
- **utils**: add Singleton metaclass
- **icon**: add add_pixmap method
- **gui**: Add PixmapCache
- **Font**: add some more methods

## v0.136.0 (2020-11-26)

### Feat

- **location**: add PlaceResult class
- **location**: add PlaceProposedSearchResult class
- **location**: add clone_from method to reply classes
- **Object**: add has_id method

### Fix

- emit inputandslider signal correctly on value change
- correct flag for constants.NO_CHILDREN

## v0.135.0 (2020-11-26)

### Feat

- **WebEngineHistoryItem**: add get_icon_url method
- **location**: add PlaceMatchReply / PlaceIdReply classes
- **PlaceContentReply/PlaceSearchReply**: add request methods
- **gui**: add TextListFormat class
- **gui**: add TextImageFormat class
- **location**: add some reply/result classes
- **gui**: add TextTableCellFormat class
- **gui**: add app method
- **gui**: add TextFrameFormat class
- **Application**: add get_font method
- add qthelp module
- **quick**: add QuickPaintedItem class
- **gui**: add TextBlockGroup class
- **TextCharFormat**: add get/set_vertical_alignment methods
- **TextBlock**: add __contains__ method
- **PaintDevice**: add get_metric method
- **GuiApplication**: add get/set_layout_direction methods
- **gui**: add TextObject / TextLength / TextFrame / TextFormat classes
- **core**: add ItemSelection class
- **GraphicsLayout**: add set_margin method

### Fix

- correctly add items for GraphicsGridLayout

## v0.134.0 (2020-11-23)

### Feat

- **core**: add PersistentModelIndex class
- **core**: add PluginLoader class
- **core**: add Library class
- **gui**: add PainterPathStroker class
- **gui**: add ImageWriter / ImageReader / ImageIOHandler classes
- **quick**: add QuickItem / QuickWindow classes
- **core**: add install_message_handler method
- **gui**: add RasterWindow / PaintDeviceWindow / OpenGLWindow classes
- **svg**: add SvgGenerator class
- **SplashScreen**: allow pixmap for ctor
- **icon**: add get_available_sizes method
- **widget**: add set_attributes method
- **gui**: add Vector4D / Matrix4x4 classes
- **custom_widgets**: add StarDelegate class
- **custom_delegates**: add ProgressBarDelegate class
- **widgets**: add missing StyleOption classes
- **WidgetItems**: some more methods
- **Painter**: add backup_state contextmanager

### Fix

- **KeySequenceEdit**: correct repr
- correct coloring for WaitingSpinner

## v0.133.1 (2020-11-16)

### Fix

- test fix

## v0.133.0 (2020-11-16)

### Feat

- **ComboBox**: default param for add_items
- **AbstractItemModel**: add force_reset/force_layoutchange methods
- add location module
- **gui**: add FontMetricsF class
- **GeoCoordinate**: add __bool__ method
- **FontMetrics**: add get_(tight_)bounding_rect methods
- **Url**: add to_string method
- **network**: add LocalServer / TcpServer classes
- **multimediawidgets**: add GraphicsVideoItem class
- **mediaobject**: add get_availability method
- add qt module

## v0.132.1 (2020-11-07)

### Fix

- import fix

## v0.132.0 (2020-11-07)

### Feat

- **NetworkAccessManager**: allow str for request
- **network**: add UdpSocket
- **network**: add NetworkAddressEntry / NetworkInterface classes
- add texttospeech module
- **network**: add NetworkDatagram class
- **core**: add DeadlineTimer class
- **network**: add HostAddress/AbstractSocket/TcpSocket classes
- **network**: add NetworkProxy class
- **network**: add HttpMultiPart class
- **network**: add HttpPart class
- **NetworkRequest**: add set/get_header methods

## v0.131.0 (2020-11-04)

### Feat

- **webenginecore**: add WebEngineHttpRequest class
- **webenginewidgets**: add WebEngineContextMenuData class
- **webenginewidgets**: add WebEngineScriptCollection class
- **multimedia**: add CameraExposure/CameraImageProcessing classes
- **multimedia**: add CameraFocus(Zone) classes
- **webenginecore**: add WebEngineUrlSchemeHandler

## v0.130.0 (2020-11-04)

### Feat

- **WebEnginePage**: add some settings methods
- **webenginewidgets**: add WebEngineSettings class
- add bluetooth module
- **core**: add Uuid class
- add quick module
- **gui**: add Surface and Window class
- **multimedia**: add ImageEncoderSettings
- **multimedia**: add MediaTimeRange and MediaTimeInterval classes

## v0.129.1 (2020-10-29)

### Fix

- fix tests
- fix multimedia tests for Travis

### Feat

- **charts**: add Legend class
- **WebEnginePage**: add get_history method
- **qml**: add JSValue(Iterator) class
- **VideoWidget**: option for fullscreen toggling via double click
- **multimedia**: add CameraViewFinderSettings
- **multimedia**: add VideoFrame class
- **multimedia**: add AbstractPlanarVideoBuffer class
- **multimedia**: add AbstractVideoBuffer class
- **multimedia**: add Camera class
- **multimedia**: add CameraInfo class
- **gui**: add Clipboard class
- **multimedia**: add AudioFormat class
- **multimedia**: add SoundEffect class
- **charts**: add PieSlice class
- **charts**: add BoxSet and CandlestickSet classes
- **charts**: add Axis-related classes
- **charts**: add BarSeries-related classes

## v0.128.1 (2020-10-25)

### Fix

- import fix

## v0.128.0 (2020-10-25)

### Feat

- **custom_widgets**: add ExpandableLine class
- **ParallelAnimationGroup**: add set_duration method
- **charts**: add Abstract/ValueAxis and PolarChart classes
- **core**: add SequentialAnimationGroup class
- **AnimationGroup**: allow slicing for indexing
- **AnimationGroup**: add add_property_animation method
- **ChartView**: add get/set_rubber_band methods
- **Chart**: add some more methods
- **core**: add Locale class
- **core**: add Margins class
- **webenginewidgets**: add some more modules

### Fix

- **Chart**: properly inherit from GraphicsWidget

## v0.127.1 (2020-10-20)

### Fix

- fix tests

## v0.127.0 (2020-10-20)

### Fix

- always import correct bindings for winextras module
- **Url**: allow initializing without arg

### Feat

- **PainterPath**: add set_fill_rule method
- **PainterPath**: add get_bounding_rect method
- **GraphicsItem**: add get_shape method
- **MediaPlaylist**: add get_media_url method
- start with webenginecore module
- **core**: add EventLoop class
- **Widget**: add get_font_info method
- **custom_models**: add PlaylistModel
- **Translator**: add get_file_path method
- add positioning module
- add some first QtQml classes
- **core**: add LibraryInfo class
- **Application**: add __iter__ method
- **Application**: add get/set_navigation_mode methods
- **Application**: add get/is_effect_enabled methods
- **custom_widgets**: add Player class

## v0.126.0 (2020-10-08)

### Feat

- **core**: add Process class
- **DateTime**: add get/set_time_spec and get_date/time methods
- **core**: add Time class
- **DateTime**: add timezone methods
- **core**: add TimeZone class
- **Pixmap**: add create_dot classmethod

## v0.125.1 (2020-10-07)

### Fix

- import fix

## v0.125.0 (2020-10-07)

### Feat

- **widgets**: add Transition classes
- **core**: add Transition classes

### Fix

- fix Action.get_shortcut for NoneValue

## v0.124.0 (2020-10-05)

### Feat

- **IODevice**: add get_open_mode method
- Improve repr and add str method for Date and DateTime
- **core**: add TemporaryFile class
- **FileDevice**: add set/get_file_time methods
- **MainWindow**: allow setting central widget to None
- **AbstractButton**: add get_shortcut method
- **Url**: add from_user_input method
- **WebEngineView**: add get_url method
- **FileInfo**: support pathlib + add proper repr
- **KeySequence**: allow initializing with standard keys

## v0.123.1 (2020-09-29)

### Fix

- add missing State import in core module

## v0.123.0 (2020-09-29)

### Feat

- **core**: add State classes
- **core**: add TextBoundaryFinder class
- **ProgressBar**: add get/set_orientation methods + serialize work
- **Action**: allow setting callback with ctor
- **WebEngineView**: set subclassed WebEnginePage by default
- **WebEnginePage**: add some more methods and constants
- **AbstractSlider**: add get/set_orientation methods
- **core**: add FileInfo class
- **webenginewidgets**: add WebEngineProfile class

## v0.122.1 (2020-09-27)

### Fix

- use correct icon names

## v0.122.0 (2020-09-27)

### Feat

- **gui**: add PageLayout
- **gui**: add Movie class
- **gui**: add PageSize class
- **gui**: add FontInfo class
- **core**: add UrlQuery class
- add network module
- **PropertyAnimation**: add get/set_property_name methods
- **core**: add ParallelAnimationGroup
- **widgets**: add SizeGrip class
- **widgets**: add DataWidgetMapper class
- **core**: add StringListModel
- **VersionNumber**: add get_python_version
- **gui**: add Transform class
- **Painter**: add draw_polygon method
- add core.ByteArray

## v0.121.0 (2020-09-10)

### Feat

- **Image**: add __setitem__ / __getitem__ methods
- **Line/LineF**: add __reversed__ and __abs__ methods
- **GraphicsScene**: add get/set_item_index_method method

### Fix

- serialization fixes

## v0.120.0 (2020-08-27)

### Feat

- **GraphicsWidget**: add set_layout method
- **GraphicsLayout**: add some magic methods
- **GraphicsScene**: add add_item_group method
- **widgets**: add GraphicsAnchorLayout / GraphicsGridLayout / GraphicsLinearLayout
- **widgets**: add GraphicsItemGroup
- **Layout**: add __delitem__ method
- **Polygon/PolygonF**: add __repr__ and __iter__ methods
- **PainterPath**: some additional methods
- **GraphicsItems**: add repr methods
- **Line/LineF**: add __repr__ and __iter__
- **Application**: allow loading included language files via load_language_file
- **widgets**: add GraphicsView class

### Refactor

- PromptLineEdit rework

## v0.119.1 (2020-08-24)

### Fix

- add missing StyleOptionComplex class

## v0.119.0 (2020-08-24)

### Feat

- **GraphicsScene**: add some convenience methods
- **widgets**: add graphicsitem classes
- **StylePainter**: add draw_complex_control method
- **gui**: allow pickling some more classes
- **core**: add LineF class
- **Widget**: add get_palette() method
- **widgets**: add GraphicsPixmapItem / GraphicsScene
- **GraphicsItem**: add __getitem__ and __setitem__ methods
- **widgets**: add Blur/Colorize/DropShadowEffect

### Fix

- Graphicsitem collides methods fix
- **KeySequence**: pickling

## v0.118.2 (2020-08-17)

### Fix

- Fix tests

## v0.118.1 (2020-08-17)

### Fix

- **MenuBar**: fix add method

## v0.118.0 (2020-08-17)

### Refactor

- **MenuBar**: return subclassed types instead of qt classes

### Feat

- **gui**: add TextDocument / TextBlock / TextOption
- **gui**: add ConicalGradient / RadialGradient
- **custom_widgets**: add CollapsibleFrame
- **GraphicsItem**: add some more methods

## v0.117.0 (2020-08-16)

### Feat

- **MimeData**: add dict-like interface
- **Timer**: add get/set_type methods
- **File**: add __repr__ and __str__ methods
- **Dir**: add __repr__ and __truediv__ methods
- **Frame**: set/get_frame_shape, set/get_frame_shadow
- **Splitter**: add __setitem__ method, and some more typing
- **Polygon/PolygonF**: pythonize
- **core**: add Abstract/Variant/PropertyAnimation and AnimationGroup
- **core**: add EasingCurve
- **StyleOptionSlider**: add get_orientation method

### Refactor

- **SpanSlider**: clean up code

## v0.116.0 (2020-08-13)

### Feat

- **gui**: add LinearGradient
- **AbstractSlider**: add get/set_repeat_action and trigger_action methods
- **TabWidget**: add get/set_tab_position methods
- **Image/Pixmap**: add __bool__ method
- **MenuBar**: serialize stuff
- **MdiArea**: serialize stuff
- **Brush**: allow pickling + add get_texture_image method
- **custom_widgets**: add Timeline
- **Pen**: add methods for setting and getting style / join style / cap style

### Refactor

- **Painter**: rework set_pen / get_pen

## v0.115.0 (2020-08-12)

### Feat

- **Polygon**: add add_points method
- **Object**: add store_widget_states / restore_widget_states
- **Painter**: add paint_on, set_transparent_background, set_brush
- **PainterPath**: add add_rect method
- **Application**: add __class_getitem__

### Fix

- **RegexEditor**: correctly initialize dialog

## v0.114.1 (2020-08-12)

### Fix

- **HeaderView**: fix saving state

## v0.114.0 (2020-08-12)

### Refactor

- use AutoSlot decorator

### Feat

- add autoslot decorator
- add prettyqt.debug

## v0.113.0 (2020-08-10)

### Feat

- **gui**: add PainterPath class
- **gui**: add Polygon class
- **gui**: palette improvements
- **core**: add Line class
- **core**: add TransposeProxyModel / ConcatenateTablesProxyModel
- add ObjectBrowser
- **widgets**: add GraphicsEffect / GraphicsObject / GraphicsOpacityEffect
- **Action**: "checked" param for ctor
- **gui**: some magic methods + get_matches for KeySequence
- **core**: allow pickling VersionNumber / Size / Dir
- **gui**: add Gradient class
- add ColumnItemModel / ColumnItem
- **Settings**: add set_values method
- **Widget**: spacing kwarg for set_layout

### Refactor

- add serialization stuff
- improve some repr methods

## v0.112.0 (2020-08-04)

### Feat

- **utils**: add install_exceptionhook method
- **FileSystemModel**: add some more shortcuts for set_root_path
- **core**: add VersionNumber class
- **Application**: add get_icon method
- **MessageBox**: add show_exception method

### Refactor

- improve compat with older Qt Versions

### Fix

- another test fix

## v0.111.1 (2020-08-03)

### Fix

- fix tests for Linux

## v0.111.0 (2020-08-03)

### Feat

- **widgets**: add FontComboBox
- **StandardPaths**: add __class_getitem__ method
- **Action**: some more ctor kwargs
- **Action**: add get/set_menu_role methods, some pickle work

### Refactor

- custom Exception for wrong params

### Fix

- **Menu**: disable separator widgetAction

## v0.110.2 (2020-08-03)

### Fix

- fix broken LogTextEdit

## v0.110.1 (2020-08-03)

### Fix

- **LogTextEdit**: improve exception handling
- **SidebarWidget**: some fixes related to set_marker

## v0.110.0 (2020-08-02)

### Refactor

- improve serialization for listitems
- Validator pickle work

### Feat

- **Image**: allow pickling
- **DataStream**: add create_bytearray / write_bytearray / copy_data methods
- **core**: add DataStream class

## v0.109.0 (2020-08-02)

### Feat

- **widget**: add __pretty__ method for devtools
- **GridLayout**: allow adding tuples/lists

### Refactor

- rework widget pickling
- move CheckboxDelegate to custom_delegates
- pickle stuff for undocommand

## v0.108.0 (2020-07-31)

### Feat

- **custom_delegates**: add IconDelegate and NoFocusDelegate
- **TableWidet**: add __getitem__ and __setitem__ methods
- **Icon**: add from_image method
- allow str for layout.__getitem__ (uses objectName)
- **SidebarWidget**: add set_marker method

### Refactor

- move delegates to separate module

## v0.107.0 (2020-07-29)

### Feat

- **GridLayout**: also allow adding LayoutItems via add method

## v0.106.1 (2020-07-29)

### Fix

- **TabWidget**: correctly close detached tabs on app close
- pickle fixes for toolbar and dockwidget
- **PygmentsHighlighter**: catch pygments KeyError

## v0.106.0 (2020-07-26)

### Feat

- **gui**: add DesktopServices class
- **multimedia**: add AudioRecorder class
- **core**: add StandardPaths class
- **widgets**: add Undo classes

## v0.105.0 (2020-07-24)

### Feat

- **MediaRecorder**: some new methods
- sort_by_column for tableview and treeview
- **multimedia**: dict-setter and getter for encodersettings

### Refactor

- improve Url-Pathlib interoperability

### Fix

- **PopupInfo**: use PrimaryScreen geometry instead of screens[0] for positioning

## v0.104.0 (2020-07-23)

### Feat

- **multimedia**: add MediaRecorder
- **AbstractItemModel**: add __getitem__ method
- **multimedia**: add VideoEncoderSettings / AudioEncoderSettings

### Refactor

- use subclassed core.Size

## v0.103.0 (2020-07-22)

### Feat

- **ActionGroup**: add __getitem__ method
- **MediaContent**: add get_url method
- add multimediawidgets module
- add multimedia module
- **PlainTextEdit**: add allow_wheel_zoom method
- **Object**: name kwarg for find_parent method

## v0.102.0 (2020-07-21)

### Refactor

- move raise_dock to from Widget to Object
- **SidebarWidget**: some code cleanup, make settings button size configurable
- **Widget**: default state to True for set_attribute
- **MainWindow**: add return value for load_window_state

### Feat

- **Object**: add find_parent method
- **PlainTextEdit**: add style kwarg to set_syntaxhighlighter

## v0.101.1 (2020-07-20)

### Fix

- **LogTextEdit**: better integrate with custom qstylesheets

## v0.101.0 (2020-07-20)

### Feat

- **MessageBox**: add detail_text keyword argument to message method

### Fix

- correct return type for gui.icon.get_icon

## v0.100.0 (2020-07-20)

### Feat

- **ToolTip**: add show_text method
- **GuiApplication**: add set_override_cursor / restore_override_cursor methods
- **GuiApplication**: add override_cursor context manager

## v0.99.0 (2020-07-18)

### Refactor

- **FileChooserButton**: typing and fixes
- **Dataset**: typing and fixes
- **SidebarWidget**: use button map instead of attaching button to widget

### Feat

- **AbstractItemView**: add scroll_to method

## v0.98.5 (2020-07-17)

### Perf

- add icon cache

### Refactor

- use core.Settings for windows dark mode detection

## v0.98.4 (2020-07-15)

### Fix

- use qta default icon color instead of black for default

## v0.98.3 (2020-07-15)

### Refactor

- properly set stylesheets by using contextmanager
- **FontDialog**: do not override current_font contextmanager
- move current_font context manager to Widget class

## v0.98.2 (2020-07-15)

### Fix

- package name

## v0.98.1 (2020-07-15)

### Fix

- correctly reset stylesheet for widget validation background

### Refactor

- use qstylizer for stylesheet editing

## v0.98.0 (2020-07-15)

### Feat

- **widgets**: add StyleFactory

### Refactor

- **FontDatabase**: make add_fonts_from_folder a classmethod

## v0.97.0 (2020-07-15)

### Feat

- **gui**: add FontDatabase
- **widgets**: add Completer
- **widgets**: add ActionGroup

## v0.96.0 (2020-07-14)

### Feat

- **SelectionWidget**: default keyword argument for add_custom

## v0.95.0 (2020-07-14)

### Feat

- **SelectionWidget**: different options for custom type
- add PagedPaintDevice
- **Widget**: add set_margin method

## v0.94.0 (2020-07-14)

### Feat

- **Widget**: add Widget.font_metrics()
- **SpacerItem**: allow strings for size policy in ctor
- allow Mapping for listwidget.add_items

### Refactor

- change to {value: label} dicts for FlagSelectionWidget.add_items

## v0.93.1 (2020-07-14)

### Refactor

- typecheck for Mapping instead of dict for combobox / selectionwidget add_items method

## v0.93.0 (2020-07-14)

### Feat

- add register_extensions function to settings module

### Refactor

- **Settings**: do not override value method

## v0.92.1 (2020-07-14)

### Fix

- winextras test fix

## v0.92.0 (2020-07-14)

### Feat

- add widgets.SystemTrayIcon
- add winextras module
- **Label**: set_indent method

## v0.91.0 (2020-07-13)

### Feat

- **SidebarWidget**: allow choosing layout
- **MainWindow**: add show_blocking method

## v0.90.0 (2020-07-13)

### Feat

- **Toolbar**: allow combinations of allowed areas for set_allowed_areas
- **SidebarWidget**: add optional settings menu

## v0.89.1 (2020-07-13)

### Refactor

- **SelectionWidget**: switch to {data: label} dicts for add_items to be in line with RadioButton

## v0.89.0 (2020-07-13)

### Feat

- **SidebarWidget**: make button width configurable

## v0.88.1 (2020-07-13)

### Refactor

- **ComboBox**: use set_data for set_value

### Fix

- **ComboBox**: fix add_items method

## v0.88.0 (2020-07-13)

### Feat

- **ComboBox**: set_data method

## v0.87.0 (2020-07-13)

### Feat

- **ComboBox**: allow dict for add_items

## v0.86.3 (2020-07-12)

### Refactor

- **RegexEditor**: code cleanup

## v0.86.2 (2020-07-12)

### Fix

- another deployment fix

## v0.86.1 (2020-07-12)

### Fix

- deployment fix

## v0.86.0 (2020-07-12)

### Feat

- add Scintilla CodeEditor
- **PlainTextEdit**: add color argument for highlight_current_line

## v0.85.1 (2020-07-10)

### Fix

- add missing pygments requirement

## v0.85.0 (2020-07-10)

### Feat

- **dataset**: add RegexPattern DataItem
- **RegexEditor**: use syntaxhighlighter for pattern
- **RegexInput**: use syntaxhighlighter for pattern
- **PlainTextEdit**: add set_syntaxhighlighter method
- **Label**: add set_color method

### Refactor

- **CodeEditor**: use pygments for syntax highlighting

## v0.84.0 (2020-07-10)

### Feat

- **sidebarwidget**: allow setting tab by object id
- **Object**: name kwarg for Object.find_children, add Object.find_child

## v0.83.1 (2020-07-09)

### Refactor

- move set_icon from window classes to widget class

## v0.83.0 (2020-07-09)

### Feat

- add Label.set_point_size
- add self for label methods to allow chaining
- Font.current_font context manager

## v0.82.0 (2020-07-09)

### Feat

- add Label.set_bold / set_italic / set_weight
- added Font.set_weight

## v0.81.0 (2020-07-08)

### Feat

- allow setting window icon color
- os dark mode detection

## v0.80.1 (2020-07-08)

### Fix

- Settings.value() returned wrong type

## v0.80.0 (2020-07-08)

### Feat

- add Widget.set_attribute
- add margin keyword argument to Widget.set_layout

## v0.79.1 (2020-07-08)

### Fix

- remove Qt logger on Application exit

## v0.79.0 (2020-07-08)

### Feat

- add widgets.Application.get_widget

## v0.78.0 (2020-07-08)

### Feat

- allow to save/load window state recursively. Saving needs to be done explicitely now.

### Fix

- some fixes for core.Settings dict interface
- properly preserve types in core.Settings

## v0.77.1 (2020-07-07)

### Refactor

- also allow qt flag for Splitter ctor

### Fix

- return correct types for re.groupdict / re.groups
- Fixed an issue which prevented saving an image from chartview

## 0.77.0 (2020-07-06)

### Feat

- allow custom icons for Messagebox
- add Icon.get_pixmap
- add Object.set_unique_id / Object.get_id
- allow None for set_max_height/width widget setters
- add checkboxdelegate
- add regexinput
- add pre-commit-hook for commit messages

### Fix

- fix Messagebox.message call

### Refactor

- dont use property setter widget.id
- dont use property setter widget.title
- add child classes in re module
- radiodelegate stuff
- no props for abstractscrollarea scrollbars

## v0.75.9 (2020-07-05)

## v0.75.8 (2020-07-05)

## v0.75.7 (2020-07-05)

## v0.75.6 (2020-07-05)

## v0.75.5 (2020-07-05)

## v0.75.4 (2020-07-05)

## v0.75.3 (2020-07-05)

## v0.75.2 (2020-07-05)

## v0.75.1 (2020-07-05)

## v0.75.0 (2020-07-05)

## v0.74.3 (2020-07-05)

## v0.74.2 (2020-07-05)

## v0.74.1 (2020-07-05)

## v0.74.0 (2020-07-05)

## v0.73.4 (2020-07-04)

## v0.73.3 (2020-07-04)

## v0.73.2 (2020-07-04)

## v0.73.1 (2020-07-04)

## v0.73.0 (2020-07-02)

## v0.72.3 (2020-07-01)

## v0.72.2 (2020-07-01)

## v0.72.1 (2020-07-01)

## v0.72.0 (2020-07-01)

## v0.71.0 (2020-06-30)

## v0.70.0 (2020-06-30)

## v0.69.0 (2020-06-29)

## v0.68.0 (2020-06-29)

## v0.67.1 (2020-06-28)

## v0.65.1 (2020-06-24)

## v0.65.0 (2020-06-24)

## v0.64.0 (2020-06-24)

## v0.63.0 (2020-06-22)

## v0.62.0 (2020-06-21)

## v0.61.0 (2020-06-21)

## v0.60.1 (2020-06-21)

## v0.60.0 (2020-06-20)

## v0.59.0 (2020-06-20)

## v0.58.1 (2020-06-19)

## v0.57.1 (2020-06-15)

## v0.57.0 (2020-06-14)

## v0.56.1 (2020-06-10)

## v0.56.0 (2020-06-10)

## v0.55.0 (2020-06-09)

## v0.54.0 (2020-06-08)
