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
