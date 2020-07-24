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
