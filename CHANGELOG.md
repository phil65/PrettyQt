## v0.77.1 (2020-07-07)

### Feat

- allow custom icons for Messagebox
- add Icon.get_pixmap
- add Object.set_unique_id / Object.get_id
- allow None for set_max_height/width widget setters
- add checkboxdelegate
- add regexinput
- add pre-commit-hook for commit messages

### Fix

- return correct types for re.groupdict / re.groups
- Fixed an issue which prevented saving an image from chartview
- fix Messagebox.message call

### Refactor

- also allow qt flag for Splitter ctor
- dont use property setter widget.id
- dont use property setter widget.title
- add child classes in re module
- radiodelegate stuff
- no props for abstractscrollarea scrollbars
