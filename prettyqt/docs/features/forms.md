## Forms from pydantic models

`custom_widgets.PydanticForm` builds an editor widget per field of a pydantic v2 model
and validates the input with the model. Install the `pydantic` extra
(`pip install prettyqt[pydantic]`, also part of `addons`).

```py
import enum
import pathlib
from typing import Literal

import pydantic

from prettyqt import custom_widgets, widgets


class Method(enum.Enum):
    LINEAR = "linear"
    NEAREST = "nearest"


class FillParams(pydantic.BaseModel):
    column: str = pydantic.Field(title="Column", description="Column to fill")
    method: Method = Method.LINEAR
    limit: int | None = pydantic.Field(None, ge=1)
    factor: float = pydantic.Field(1.0, gt=0, json_schema_extra={"step": 0.1, "suffix": " x"})
    direction: Literal["forward", "backward"] = "forward"
    output: pathlib.Path | None = None


app = widgets.app()
form = custom_widgets.PydanticForm(FillParams, debounce_ms=200)
form.value_changed.connect(print)  # validated FillParams instance (GUI thread)
form.errors_changed.connect(print)  # {"field": "message"}, empty when valid
form.show()
app.exec()
```

Field types and their editors:

| Type | Editor |
| --- | --- |
| `str` | line edit (`multiline` hint: plain text edit) |
| `int`, `float` | spin box; range from `ge` / `gt` / `le` / `lt`, step from `multiple_of` |
| `bool` | check box |
| `Literal[...]`, `Enum` | combo box |
| `list[str]` (also `int` / `float` items) | comma-separated line edit (`multiline`: one item per line) |
| `list[Literal]`, `list[Enum]` | checkable list |
| `pathlib.Path` | file chooser button |
| `Optional[X]` | check box enabling the editor (`None` when unchecked) |
| nested `BaseModel` | group box with a sub-form (checkable when optional) |
| anything else | JSON line edit |

UI hints go into `json_schema_extra`: `widget`, `placeholder`, `multiline`, `step`,
`decimals`, `prefix`, `suffix`, `mapping` (`{value: label}` combo box), `choices`,
`editable`, `file_mode`, `mode`, `extensions`, `readonly`, `hidden`. App-specific
editors (e.g. a column chooser) are passed as `widget_factories={"column": factory}`
and selected with `json_schema_extra={"widget": "column"}`; a factory gets
`(field_name, field_info, hints)` and returns a widget with `get_value()`,
`set_value()` and a `value_changed` signal.

Labels come from `title` (fallback: the field name), tooltips from `description`.
To translate them, pass a translation function: titles, descriptions and `mapping`
labels go through it, so they can be gettext msgids (marked with `N_()`).
After a language change, `retranslate()` updates the texts in place (values and
errors are kept, nested forms included):

```py
form = custom_widgets.PydanticForm(FillParams, translate=i18n.gettext)
...
i18n.set_language("de")
form.retranslate()
```

Validation errors are shown below the field, model-level errors below the form.
`get_value()` validates and returns the model (or `None`), `set_value()` takes a
model instance or a dict.

`custom_widgets.PydanticDialog(model)` wraps the form with OK / Cancel; OK is
enabled only while the input is valid.
`PydanticDialog.get_model_instance(FillParams)` runs it modally.
It takes `translate` as well (also applied to the window title) and has
`retranslate()`.

## Code editor

`custom_widgets.CodeEditor` is a plain text editor with line numbers and Pygments
syntax highlighting (`language="python"` by default):

```py
editor = custom_widgets.CodeEditor()
editor.set_text(code)  # keeps cursor / scroll position, undoable
editor.add_line_marker(3, "SyntaxError: invalid syntax")  # kind: error / warning / info
editor.set_line_markers({1: "unused import"}, kind="warning")  # replace all markers
editor.clear_line_markers()
editor.set_read_only()
```

Marked lines are tinted; hovering them (or their line number) shows the messages.

## Command palette

`custom_widgets.CommandPalette` is a frameless popup with a fuzzy-filtered list of
`QAction`s (Enter triggers the selected one, Escape closes it):

```py
palette = custom_widgets.CommandPalette()
palette.install_to(window)
window.add_shortcut("Ctrl+Shift+P", palette.show)
palette.add_actions(actions)  # append
palette.set_actions(other_actions)  # replace all (e.g. after the registry changed)
palette.clear()
palette.get_actions()
```

Action texts are read when the list is shown; after re-texting actions (language
change), call `set_actions(palette.get_actions())` to refresh the list.
