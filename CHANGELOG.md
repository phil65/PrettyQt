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
