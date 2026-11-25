"""Forms generated from pydantic v2 models.

`PydanticForm` builds one editor widget per field of a pydantic `BaseModel`,
validates the edited values with the model and shows validation errors inline.
`PydanticDialog` wraps a form in a dialog with OK / Cancel buttons.

Widget selection and UI hints come from the field's `json_schema_extra`:

- `widget`: editor override: `"line_edit"`, `"text_edit"`, `"spin_box"`,
  `"check_box"`, `"combo_box"`, `"file"`, `"directory"`, `"list"`, `"json"`, or the
  name of a factory passed via `widget_factories` (e.g. a column chooser)
- `placeholder`: placeholder text for text / list editors
- `multiline`: multi-line editor for `str`, one item per line for `list[str]`
- `step`: single step of spin boxes
- `decimals`: decimals of float spin boxes (default 4)
- `prefix` / `suffix`: prefix / suffix text of spin boxes (e.g. a unit)
- `mapping`: `{value: label}`: combo box with these values and labels
- `choices`: list of allowed values: combo box
- `editable`: combo box (from `mapping` / `choices`) also accepts free text
- `file_mode` / `mode` / `extensions`: passed to `FileChooserButton` (`Path` fields)
- `readonly`: editor is disabled
- `hidden`: no editor; the value is kept from `set_value()` or the default

Hint values end up in the model's JSON schema, so keep them JSON-serializable.

All widget code runs on the GUI thread; `value_changed` is emitted on the GUI thread.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
import dataclasses
import enum
import json
import logging
import pathlib
import types
from typing import TYPE_CHECKING, Annotated, Any, Literal, Union, get_args, get_origin

import annotated_types
import pydantic
from pydantic.fields import FieldInfo
import pydantic_core

from prettyqt import core, custom_widgets, widgets


if TYPE_CHECKING:
    from pydantic_core import ErrorDetails


logger = logging.getLogger(__name__)

ROOT_KEY = "__root__"
DEFAULT_DECIMALS = 4
ERROR_COLOR = "#d32f2f"
STRING_LIST_ORIGINS = (list, tuple, set, frozenset, Sequence)

# Factory for custom editors: `(field_name, field_info, hints) -> widget`.
#
# The widget must provide `get_value()`, `set_value(value)` and a `value_changed` signal.
WidgetFactory = Callable[[str, FieldInfo, Mapping[str, Any]], widgets.QWidget]


@dataclasses.dataclass(frozen=True)
class FieldSpec:
    """Resolved type information of a model field."""

    name: str
    info: FieldInfo
    annotation: Any
    optional: bool
    metadata: tuple[Any, ...]
    hints: Mapping[str, Any]


def _get_hints(info: FieldInfo) -> dict[str, Any]:
    extra = info.json_schema_extra
    return dict(extra) if isinstance(extra, Mapping) else {}


def _unwrap_annotated(annotation: Any) -> tuple[Any, tuple[Any, ...]]:
    metadata: list[Any] = []
    while get_origin(annotation) is Annotated:
        annotation, *meta = get_args(annotation)
        for m in meta:
            if isinstance(m, FieldInfo):
                metadata.extend(m.metadata)
            else:
                metadata.append(m)
    return annotation, tuple(metadata)


def _is_union(annotation: Any) -> bool:
    return get_origin(annotation) in (Union, types.UnionType)


def resolve_field(name: str, info: FieldInfo) -> FieldSpec:
    """Resolve the editable type of a field (strips `Optional` and `Annotated`)."""
    annotation, metadata = _unwrap_annotated(info.annotation)
    optional = False
    if _is_union(annotation):
        args = [a for a in get_args(annotation) if a is not types.NoneType]
        optional = len(args) < len(get_args(annotation))
        if len(args) == 1:
            annotation, inner_meta = _unwrap_annotated(args[0])
            metadata += inner_meta
        else:
            annotation = Union[tuple(args)]  # noqa: UP007
    return FieldSpec(
        name=name,
        info=info,
        annotation=annotation,
        optional=optional,
        metadata=(*info.metadata, *metadata),
        hints=_get_hints(info),
    )


def _is_model(annotation: Any) -> bool:
    return isinstance(annotation, type) and issubclass(annotation, pydantic.BaseModel)


def _choices_for(annotation: Any) -> list[tuple[str, Any]] | None:
    if get_origin(annotation) is Literal:
        return [(str(v), v) for v in get_args(annotation)]
    if isinstance(annotation, type) and issubclass(annotation, enum.Enum):
        return [(m.name, m) for m in annotation]
    return None


def _bounds(metadata: Sequence[Any], is_int: bool, decimals: int):
    """Return (minimum, maximum, multiple_of) from annotated_types constraints."""
    tiny = 1 if is_int else 10**-decimals
    minimum = maximum = multiple = None
    for m in metadata:
        match m:
            case annotated_types.Ge(ge=v):
                minimum = v
            case annotated_types.Gt(gt=v):
                minimum = v + tiny  # type: ignore[operator]
            case annotated_types.Le(le=v):
                maximum = v
            case annotated_types.Lt(lt=v):
                maximum = v - tiny  # type: ignore[operator]
            case annotated_types.MultipleOf(multiple_of=v):
                multiple = v
            case annotated_types.Interval():
                sub = [
                    annotated_types.Ge(m.ge) if m.ge is not None else None,
                    annotated_types.Gt(m.gt) if m.gt is not None else None,
                    annotated_types.Le(m.le) if m.le is not None else None,
                    annotated_types.Lt(m.lt) if m.lt is not None else None,
                ]
                lo, hi, _ = _bounds([s for s in sub if s], is_int, decimals)
                minimum = lo if lo is not None else minimum
                maximum = hi if hi is not None else maximum
    return minimum, maximum, multiple


def _max_length(metadata: Sequence[Any]) -> int | None:
    for m in metadata:
        if isinstance(m, annotated_types.MaxLen):
            return m.max_length
    return None


# ---------------------------------------------------------------------------
# Editors. Each provides get_value(), set_value() and a value_changed signal.
# ---------------------------------------------------------------------------


class ChoiceEditor(widgets.ComboBox):
    """Combo box over a fixed list of Python values (Literal / Enum / mapping)."""

    value_changed = core.Signal(object)

    def __init__(self, choices: Sequence[tuple[str, Any]], editable: bool = False):
        super().__init__()
        self._values: list[Any] = []
        for label, value in choices:
            self._values.append(value)
            self.addItem(label)
        if editable:
            self.set_editable(True)
            self.editTextChanged.connect(
                lambda _: self.value_changed.emit(self.get_value())
            )

    def _index_changed(self, index: int):
        self.value_changed.emit(self.get_value())

    def get_value(self) -> Any:
        idx = self.currentIndex()
        if self.isEditable() and (idx < 0 or self.currentText() != self.itemText(idx)):
            return self.currentText()
        return self._values[idx] if 0 <= idx < len(self._values) else None

    def set_value(self, value: Any):
        for i, v in enumerate(self._values):
            if v == value:
                self.setCurrentIndex(i)
                return
        if self.isEditable() and value is not None:
            self.setCurrentText(str(value))
        else:
            self.setCurrentIndex(-1)


class MultiChoiceEditor(widgets.ListWidget):
    """Checkable list for `list[Literal[...]]` / `list[Enum]` fields."""

    value_changed = core.Signal(object)

    def __init__(self, choices: Sequence[tuple[str, Any]]):
        super().__init__()
        self._values = [v for _, v in choices]
        for label, _ in choices:
            item = widgets.ListWidgetItem(label)
            item.setFlags(item.flags() | core.Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(core.Qt.CheckState.Unchecked)
            self.addItem(item)
        rows = min(len(self._values), 6)
        self.setMaximumHeight(self.sizeHintForRow(0) * rows + 2 * self.frameWidth() + 4)
        self.itemChanged.connect(lambda _: self.value_changed.emit(self.get_value()))

    def get_value(self) -> list[Any]:
        return [
            v
            for i, v in enumerate(self._values)
            if self.item(i).checkState() == core.Qt.CheckState.Checked
        ]

    def set_value(self, value: Sequence[Any] | None):
        value = list(value or [])
        with self.signals_blocked():
            for i, v in enumerate(self._values):
                state = (
                    core.Qt.CheckState.Checked
                    if v in value
                    else core.Qt.CheckState.Unchecked
                )
                self.item(i).setCheckState(state)
        self.value_changed.emit(self.get_value())


class StringListEditor(widgets.Widget):
    """Editor for `list[str]`: comma-separated line edit, or one item per line."""

    value_changed = core.Signal(object)

    def __init__(self, multiline: bool = False, placeholder: str = ""):
        super().__init__()
        layout = self.set_layout("horizontal", margin=0)
        self._multiline = multiline
        self.editor = widgets.PlainTextEdit() if multiline else widgets.LineEdit()
        self.editor.setPlaceholderText(placeholder)
        self.editor.value_changed.connect(
            lambda _: self.value_changed.emit(self.get_value())
        )
        layout.add(self.editor)

    def get_value(self) -> list[str]:
        text = self.editor.get_value()
        parts = text.splitlines() if self._multiline else text.split(",")
        return [p.strip() for p in parts if p.strip()]

    def set_value(self, value: Sequence[Any] | None):
        sep = "\n" if self._multiline else ", "
        self.editor.set_value(sep.join(str(v) for v in value or []))


class JsonEditor(widgets.Widget):
    """Fallback editor: value as JSON (plain text is passed through as string)."""

    value_changed = core.Signal(object)

    def __init__(self, placeholder: str = ""):
        super().__init__()
        layout = self.set_layout("horizontal", margin=0)
        self.lineedit = widgets.LineEdit()
        self.lineedit.setPlaceholderText(placeholder)
        self.lineedit.textChanged.connect(
            lambda _: self.value_changed.emit(self.get_value())
        )
        layout.add(self.lineedit)

    def get_value(self) -> Any:
        text = self.lineedit.text()
        try:
            return json.loads(text)
        except ValueError:
            return text

    def set_value(self, value: Any):
        if isinstance(value, str):
            self.lineedit.set_text(value)
        else:
            self.lineedit.set_text(json.dumps(pydantic_core.to_jsonable_python(value)))


class OptionalEditor(widgets.Widget):
    """Check box which enables / disables an inner editor; `None` when unchecked."""

    value_changed = core.Signal(object)

    def __init__(self, editor: widgets.QWidget):
        super().__init__()
        layout = self.set_layout("horizontal", margin=0)
        self.checkbox = widgets.CheckBox()
        self.checkbox.setToolTip("Set a value")
        self.editor = editor
        layout.add(self.checkbox)
        layout.addWidget(editor, 1)
        editor.setEnabled(False)
        self.checkbox.toggled.connect(self._on_toggled)
        editor.value_changed.connect(self._on_inner_change)

    def _on_toggled(self, checked: bool):
        self.editor.setEnabled(checked)
        self.value_changed.emit(self.get_value())

    def _on_inner_change(self, *_):
        if self.checkbox.isChecked():
            self.value_changed.emit(self.get_value())

    def get_value(self) -> Any:
        return self.editor.get_value() if self.checkbox.isChecked() else None

    def set_value(self, value: Any):
        if value is not None:
            self.editor.set_value(value)
        self.checkbox.setChecked(value is not None)


class ModelEditor(widgets.GroupBox):
    """Group box holding a sub-form for a nested model field."""

    value_changed = core.Signal(object)

    def __init__(
        self,
        model: type[pydantic.BaseModel],
        title: str = "",
        optional: bool = False,
        widget_factories: Mapping[str, WidgetFactory] | None = None,
    ):
        super().__init__(title=title)
        self.setCheckable(optional)
        if optional:
            self.setChecked(False)
        layout = self.set_layout("vertical")
        self.form = PydanticForm(model, debounce_ms=0, widget_factories=widget_factories)
        self.form._auto_validate = False
        self.form.set_margin(0)
        self.form.edited.connect(self._on_change)
        self.toggled.connect(self._on_change)
        layout.add(self.form)

    def _on_change(self, *_):
        self.value_changed.emit(self.get_value())

    def get_value(self) -> dict[str, Any] | None:
        if self.isCheckable() and not self.isChecked():
            return None
        return self.form.get_raw_value()

    def set_value(self, value: pydantic.BaseModel | Mapping[str, Any] | None):
        if self.isCheckable():
            self.setChecked(value is not None)
        if value is not None:
            self.form.set_raw_value(value)


# ---------------------------------------------------------------------------


class PydanticForm(widgets.Widget):
    """Form with an editor per field of a pydantic v2 model.

    Supported field types: `str`, `int`, `float` (spin boxes respecting `ge` / `gt` /
    `le` / `lt` / `multiple_of`), `bool`, `Literal` / `Enum` (combo box),
    `list[str]` (and other scalar lists), `list[Literal]` / `list[Enum]` (checkable
    list), `pathlib.Path` (file chooser), `X | None` (check box enabling the editor),
    nested models (group box with a sub-form). Anything else gets a JSON line edit.
    See the module docstring for the `json_schema_extra` UI hints.

    Labels come from the field's `title` (fallback: the field name), tooltips from
    `description`; both are used as given (pass translated strings).

    Signals (all emitted on the GUI thread; the widget must only be used from it):

    - `value_changed(model)`: validated model instance, debounced by `debounce_ms`;
      only emitted when the input is valid.
    - `errors_changed(dict)`: `{field_path: message}` after each validation
      (empty dict: valid).
    - `edited()`: emitted immediately on every user edit (not debounced).
    """

    value_changed = core.Signal(object)
    errors_changed = core.Signal(object)
    edited = core.Signal()

    def __init__(
        self,
        model: type[pydantic.BaseModel] | pydantic.BaseModel,
        *,
        debounce_ms: int = 200,
        widget_factories: Mapping[str, WidgetFactory] | None = None,
        parent: widgets.QWidget | None = None,
        **kwargs: Any,
    ):
        """Create the form.

        Args:
            model: model class, or an instance whose values are loaded
            debounce_ms: delay between the last edit and validation / `value_changed`.
                         0 validates synchronously on every edit.
            widget_factories: named editor factories, selected with the
                              `widget` hint (e.g. a column chooser)
            parent: parent widget
            kwargs: passed to `widgets.Widget`
        """
        super().__init__(parent=parent, **kwargs)
        instance = model if isinstance(model, pydantic.BaseModel) else None
        self._model_cls: type[pydantic.BaseModel] = (
            type(instance) if instance is not None else model  # type: ignore[assignment]
        )
        self._factories: dict[str, WidgetFactory] = dict(widget_factories or {})
        self._editors: dict[str, widgets.QWidget] = {}
        self._error_labels: dict[str, widgets.Label] = {}
        self._kept_values: dict[str, Any] = {}
        self._errors: dict[str, str] = {}
        self._loading = False
        self._auto_validate = True  # False for nested forms: the parent validates
        self._debounce_ms = debounce_ms
        self._timer = core.QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.setInterval(debounce_ms)
        self._timer.timeout.connect(self.validate)

        self._layout = widgets.FormLayout()
        self.setLayout(self._layout)
        self._root_error = self._make_error_label()
        for name, info in self._model_cls.model_fields.items():
            self._add_field(resolve_field(name, info))
        self._layout.addRow(self._root_error)
        self._load_defaults()
        if instance is not None:
            self.set_raw_value(instance)
        self._update_error_labels()

    def __repr__(self):
        return f"{type(self).__name__}({self._model_cls.__name__})"

    # --- building ---------------------------------------------------------

    @staticmethod
    def _make_error_label() -> widgets.Label:
        label = widgets.Label()
        label.set_color(ERROR_COLOR)
        label.setWordWrap(True)
        label.hide()
        return label

    def _add_field(self, spec: FieldSpec):
        hints = spec.hints
        if hints.get("hidden"):
            return
        title = spec.info.title or spec.name.replace("_", " ").capitalize()
        editor = self.create_editor(spec)
        if hints.get("readonly") or spec.info.frozen:
            editor.setEnabled(False)
        if spec.info.description:
            editor.setToolTip(spec.info.description)
        editor.setObjectName(spec.name)
        editor.value_changed.connect(self._on_edit)
        self._editors[spec.name] = editor
        error_label = self._make_error_label()
        self._error_labels[spec.name] = error_label
        if isinstance(editor, ModelEditor):
            self._layout.addRow(editor)
            self._layout.addRow(error_label)
            return
        container = widgets.Widget()
        box = container.set_layout("vertical", margin=0, spacing=2)
        box.add(editor)
        box.add(error_label)
        label = widgets.Label(title)
        if spec.info.description:
            label.setToolTip(spec.info.description)
        label.setBuddy(editor)
        self._layout.addRow(label, container)

    def create_editor(self, spec: FieldSpec) -> widgets.QWidget:
        """Create the editor widget for a field (override to customize)."""
        hints = spec.hints
        widget_name = hints.get("widget")
        if widget_name in self._factories:
            editor = self._factories[widget_name](spec.name, spec.info, hints)
            return OptionalEditor(editor) if spec.optional else editor
        if _is_model(spec.annotation) and widget_name is None:
            title = spec.info.title or spec.name.replace("_", " ").capitalize()
            editor = ModelEditor(
                spec.annotation,
                title=title,
                optional=spec.optional,
                widget_factories=self._factories,
            )
            if spec.info.description:
                editor.setToolTip(spec.info.description)
            return editor
        editor = self._create_plain_editor(spec, widget_name)
        return OptionalEditor(editor) if spec.optional else editor

    def _create_plain_editor(  # noqa: PLR0911
        self, spec: FieldSpec, widget_name: str | None
    ) -> widgets.QWidget:
        ann = spec.annotation
        hints = spec.hints
        origin = get_origin(ann)
        if "mapping" in hints:
            choices = [(str(label), value) for value, label in hints["mapping"].items()]
            return ChoiceEditor(choices, editable=hints.get("editable", False))
        if "choices" in hints:
            choices = [(str(v), v) for v in hints["choices"]]
            return ChoiceEditor(choices, editable=hints.get("editable", False))
        match widget_name:
            case "line_edit":
                return self._text_editor(spec, multiline=False)
            case "text_edit":
                return self._text_editor(spec, multiline=True)
            case "json":
                return JsonEditor(hints.get("placeholder", ""))
            case "file" | "directory":
                return self._path_editor(spec, directory=widget_name == "directory")
            case "list":
                return StringListEditor(
                    hints.get("multiline", False), hints.get("placeholder", "")
                )
            case "check_box":
                return widgets.CheckBox()
            case "spin_box" | "combo_box" | None:
                pass
            case _:
                logger.warning(
                    "No widget %r for field %r, using the default editor",
                    widget_name,
                    spec.name,
                )
        if (choices := _choices_for(ann)) is not None:
            return ChoiceEditor(choices)
        if ann is bool:
            return widgets.CheckBox()
        if ann is int or ann is float:
            return self._number_editor(spec, is_int=ann is int)
        if isinstance(ann, type) and issubclass(ann, pathlib.PurePath):
            return self._path_editor(spec, directory=False)
        if ann is str:
            return self._text_editor(spec, multiline=hints.get("multiline", False))
        if origin in STRING_LIST_ORIGINS:
            (item_type, *_) = get_args(ann) or (str,)
            item_type, _ = _unwrap_annotated(item_type)
            if (choices := _choices_for(item_type)) is not None:
                return MultiChoiceEditor(choices)
            if item_type in (str, int, float):
                return StringListEditor(
                    hints.get("multiline", False), hints.get("placeholder", "")
                )
        return JsonEditor(hints.get("placeholder", ""))

    @staticmethod
    def _text_editor(spec: FieldSpec, multiline: bool) -> widgets.QWidget:
        placeholder = spec.hints.get("placeholder", "")
        if multiline:
            text_edit = widgets.PlainTextEdit()
            text_edit.setPlaceholderText(placeholder)
            return text_edit
        editor = widgets.LineEdit()
        editor.setPlaceholderText(placeholder)
        if (max_len := _max_length(spec.metadata)) is not None:
            editor.setMaxLength(max_len)
        return editor

    @staticmethod
    def _number_editor(spec: FieldSpec, is_int: bool) -> widgets.QWidget:
        hints = spec.hints
        decimals = hints.get("decimals", DEFAULT_DECIMALS)
        minimum, maximum, multiple = _bounds(spec.metadata, is_int, decimals)
        if is_int:
            editor = widgets.SpinBox()
            editor.set_range(
                None if minimum is None else int(minimum),
                None if maximum is None else int(maximum),
            )
        else:
            editor = widgets.DoubleSpinBox()
            editor.setDecimals(decimals)
            editor.set_range(minimum, maximum)
        step = hints.get("step", multiple)
        if step is not None:
            editor.setSingleStep(step)
        if prefix := hints.get("prefix"):
            editor.setPrefix(prefix)
        if suffix := hints.get("suffix"):
            editor.setSuffix(suffix)
        return editor

    @staticmethod
    def _path_editor(spec: FieldSpec, directory: bool) -> widgets.QWidget:
        hints = spec.hints
        file_mode: Any = (
            "directory" if directory else hints.get("file_mode", "existing_file")
        )
        return custom_widgets.FileChooserButton(
            extensions=hints.get("extensions"),
            mode=hints.get("mode", "open"),
            file_mode=file_mode,
        )

    def _load_defaults(self):
        values: dict[str, Any] = {}
        for name, info in self._model_cls.model_fields.items():
            if not info.is_required():
                values[name] = info.get_default(call_default_factory=True)
        self.set_raw_value(values)

    # --- values -----------------------------------------------------------

    def get_model(self) -> type[pydantic.BaseModel]:
        """Return the model class of this form."""
        return self._model_cls

    def get_editor(self, name: str) -> widgets.QWidget:
        """Return the editor widget of a field."""
        return self._editors[name]

    def get_raw_value(self) -> dict[str, Any]:
        """Return the unvalidated editor values (plus hidden / kept values)."""
        values = dict(self._kept_values)
        for name, editor in self._editors.items():
            values[name] = editor.get_value()
        return values

    def set_raw_value(self, value: pydantic.BaseModel | Mapping[str, Any]):
        """Load values into the editors without validating / emitting."""
        if isinstance(value, pydantic.BaseModel):
            data = {name: getattr(value, name) for name in type(value).model_fields}
        else:
            data = dict(value)
        self._loading = True
        try:
            for name, val in data.items():
                if (editor := self._editors.get(name)) is None:
                    self._kept_values[name] = val
                else:
                    editor.set_value(val)
        finally:
            self._loading = False

    def set_value(self, value: pydantic.BaseModel | Mapping[str, Any]):
        """Load a model instance (or a dict of field values), then validate.

        Emits `value_changed` (debounced) if the values are valid.
        """
        self.set_raw_value(value)
        self._schedule()

    def get_value(self) -> pydantic.BaseModel | None:
        """Validate now and return the model instance, or None if invalid."""
        self._timer.stop()
        return self._validate()

    def is_valid(self) -> bool:
        return self.get_value() is not None

    def get_errors(self) -> dict[str, str]:
        """Return the errors of the last validation: `{"field.sub": message}`."""
        return dict(self._errors)

    # --- validation -------------------------------------------------------

    def _on_edit(self, *_):
        if self._loading:
            return
        self.edited.emit()
        self._schedule()

    def _schedule(self):
        if not self._auto_validate:
            return
        if self._debounce_ms <= 0:
            self.validate()
        else:
            self._timer.start()

    @core.Slot()
    def validate(self) -> pydantic.BaseModel | None:
        """Validate the current input, update inline errors, emit signals."""
        instance = self._validate()
        if instance is not None:
            self.value_changed.emit(instance)
        return instance

    def _validate(self) -> pydantic.BaseModel | None:
        try:
            instance = self._model_cls.model_validate(self.get_raw_value(), by_name=True)
        except pydantic.ValidationError as e:
            self._set_errors(e.errors(include_url=False))
            return None
        self._set_errors([])
        return instance

    def _set_errors(self, errors: Sequence[ErrorDetails]):
        new: dict[str, str] = {}
        for err in errors:
            path = ".".join(str(p) for p in err["loc"]) or ROOT_KEY
            new[path] = f"{new[path]}\n{err['msg']}" if path in new else err["msg"]
        self._show_errors(new)
        if new != self._errors:
            self._errors = new
            self._update_error_labels()
            self.errors_changed.emit(dict(new))

    def _show_errors(self, errors: Mapping[str, str]):
        """Distribute errors to nested forms (they only display them)."""
        for name, editor in self._editors.items():
            if isinstance(editor, ModelEditor):
                prefix = f"{name}."
                sub = {
                    k.removeprefix(prefix): v
                    for k, v in errors.items()
                    if k.startswith(prefix)
                }
                editor.form._show_errors(sub)
                editor.form._errors = sub
                editor.form._update_error_labels()

    def _update_error_labels(self):
        handled: set[str] = set()
        for name, label in self._error_labels.items():
            msg = self._errors.get(name)
            if isinstance(self._editors[name], ModelEditor):
                handled |= {k for k in self._errors if k.startswith(f"{name}.")}
            label.setText(msg or "")
            label.setVisible(bool(msg))
            handled.add(name)
        rest = [msg for path, msg in self._errors.items() if path not in handled]
        self._root_error.setText("\n".join(rest))
        self._root_error.setVisible(bool(rest))


class PydanticDialog(widgets.Dialog):
    """Dialog with a `PydanticForm` and OK / Cancel; OK is enabled only if valid."""

    def __init__(
        self,
        model: type[pydantic.BaseModel] | pydantic.BaseModel,
        *,
        title: str | None = None,
        widget_factories: Mapping[str, WidgetFactory] | None = None,
        parent: widgets.QWidget | None = None,
        **kwargs: Any,
    ):
        super().__init__(parent=parent, **kwargs)
        model_cls = type(model) if isinstance(model, pydantic.BaseModel) else model
        self.setWindowTitle(
            title or model_cls.model_config.get("title") or model_cls.__name__
        )
        layout = self.set_layout("vertical")
        self.form = PydanticForm(model, debounce_ms=0, widget_factories=widget_factories)
        layout.add(self.form)
        self.button_box = widgets.DialogButtonBox.create(
            ok=self.accept, cancel=self.reject
        )
        layout.add(self.button_box)
        self.form.errors_changed.connect(self._on_errors_changed)
        self.form.get_value()
        self._on_errors_changed(self.form.get_errors())

    def _on_errors_changed(self, errors: Mapping[str, str]):
        self.button_box["ok"].setEnabled(not errors)

    def accept(self):
        if self.form.is_valid():
            super().accept()

    def get_value(self) -> pydantic.BaseModel | None:
        return self.form.get_value()

    def set_value(self, value: pydantic.BaseModel | Mapping[str, Any]):
        self.form.set_value(value)

    @classmethod
    def get_model_instance(
        cls,
        model: type[pydantic.BaseModel] | pydantic.BaseModel,
        parent: widgets.QWidget | None = None,
        **kwargs: Any,
    ) -> pydantic.BaseModel | None:
        """Show the dialog modally; return the model instance, or None if cancelled."""
        dialog = cls(model, parent=parent, **kwargs)
        return dialog.get_value() if dialog.exec() else None


if __name__ == "__main__":
    from typing import Annotated as A  # noqa: N817

    class Inner(pydantic.BaseModel):
        x: int = 1
        label: str = "inner"

    class Color(enum.Enum):
        RED = "red"
        GREEN = "green"

    class Params(pydantic.BaseModel):
        name: str = pydantic.Field("abc", title="Name", description="A name")
        count: A[int, pydantic.Field(ge=0, le=10)] = 3
        factor: float = pydantic.Field(0.5, gt=0, lt=1, json_schema_extra={"step": 0.1})
        flag: bool = True
        how: Literal["left", "right"] = "left"
        color: Color = Color.RED
        columns: list[str] = []
        path: pathlib.Path | None = None
        limit: int | None = None
        inner: Inner = Inner()
        notes: str = pydantic.Field("", json_schema_extra={"multiline": True})

    app = widgets.app()
    form = PydanticForm(Params)
    form.value_changed.connect(print)
    form.show()
    app.exec()
