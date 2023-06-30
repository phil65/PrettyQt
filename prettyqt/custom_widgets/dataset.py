from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass
import functools
import pathlib

from typing import Any

from prettyqt import custom_validators, custom_widgets, gui, widgets
from prettyqt.utils import datatypes


@dataclass
class DataItem:
    label: str
    value: Any = None
    optional: str | None = None
    include: bool = True
    enabled_on: str | None = None
    disabled_on: str | None = None
    name: str | None = None
    colspan: int = 1
    label_col: int = 0
    is_enabled: bool = True

    def __post_init__(self):
        self.enabled_on = [self.enabled_on] if self.enabled_on else []
        self.disabled_on = [self.disabled_on] if self.disabled_on else []

    def __get__(self, instance, owner):
        return self.value

    def set_pos(self, col: int = 0, colspan=None):
        """Set data item's position on a GUI layout."""
        self.label_col = col
        self.colspan = colspan
        return self

    def set_value(self, value):
        self.value = value

    def store(self, prop):
        # self.set_prop("display", store=prop)
        return self

    def is_valid(self) -> bool:
        return True

    def create_widget(self) -> widgets.Widget:
        widget = self._create_widget()
        if self.optional:
            return custom_widgets.OptionalWidget(widget, self.optional)
        return widget

    def _create_widget(self):
        return NotImplemented


@dataclass
class Fixed(DataItem):
    pass


@dataclass
class Float(DataItem):
    min_val: float | None = None
    max_val: float | None = None
    unit: str = ""
    step: float = 0.1
    slider: bool = False

    def _create_widget(self) -> widgets.DoubleSpinBox:
        widget = widgets.DoubleSpinBox()
        widget.set_range(self.min_val, self.max_val)
        widget.setSingleStep(self.step)
        widget.setSuffix(self.unit)
        if self.value is not None:
            widget.set_value(self.value)
        return widget


@dataclass
class Int(DataItem):
    min_val: int | None = 0
    max_val: int | None = None
    unit: str = ""
    step: int = 1
    slider: bool = False

    def _create_widget(self) -> custom_widgets.InputAndSlider | widgets.SpinBox:
        use_spinbox = self.min_val is None or self.max_val is None
        widget = widgets.SpinBox() if use_spinbox else custom_widgets.InputAndSlider()
        widget.setSuffix(self.unit)
        widget.set_range(self.min_val, self.max_val)
        widget.set_step_size(self.step)
        if self.value is not None:
            widget.set_value(self.value)
        return widget


@dataclass
class Range(DataItem):
    min_val: int = 0
    max_val: int = 1

    def _create_widget(self) -> custom_widgets.SpanSlider:
        widget = custom_widgets.SpanSlider()
        # widget.setSuffix(self.unit)
        widget.set_range(self.min_val, self.max_val)
        # widget.set_step_size(self.step)
        if self.value is not None:
            widget.set_value(self.value)
        return widget


@dataclass
class String(DataItem):
    notempty: bool = False
    regex: str | None = None

    def _create_widget(self) -> widgets.LineEdit:
        widget = widgets.LineEdit()
        if self.notempty:
            val = custom_validators.NotEmptyValidator()
            widget.set_validator(val)
        if self.regex is not None:
            val = gui.RegularExpressionValidator()
            val.set_regex(self.regex)
            widget.set_validator(val)
        if self.value is not None:
            widget.set_value(self.value)
        return widget


@dataclass
class RegexPattern(DataItem):
    notempty: bool = False

    def _create_widget(self) -> custom_widgets.SingleLineTextEdit:
        widget = custom_widgets.SingleLineTextEdit()
        if self.notempty:
            val = custom_validators.NotEmptyValidator()
            widget.set_validator(val)
        widget.set_syntaxhighlighter("regex")
        if self.value is not None:
            widget.set_value(self.value)
        return widget


@dataclass
class Code(DataItem):
    language: str = "python"

    def _create_widget(self) -> custom_widgets.CodeEditor:
        widget = custom_widgets.CodeEditor()
        if self.value is not None:
            widget.set_value(self.value)
        return widget


@dataclass
class Regex(DataItem):
    show_flags: bool = True
    show_error: bool = False

    def _create_widget(self) -> custom_widgets.RegexInput:
        widget = custom_widgets.RegexInput(
            show_flags=self.show_flags, show_error=self.show_error
        )
        if self.value is not None:
            widget.set_value(self.value)
        return widget


@dataclass
class IntList(DataItem):
    allow_single: bool = False

    def _create_widget(self) -> custom_widgets.ListInput:
        widget = custom_widgets.ListInput(allow_single=self.allow_single)
        if self.value is not None:
            widget.set_value(self.value)
        return widget


@dataclass
class FloatList(DataItem):
    allow_single: bool = False

    def _create_widget(self) -> custom_widgets.ListInput:
        widget = custom_widgets.ListInput(allow_single=self.allow_single, typ=float)
        if self.value is not None:
            widget.set_value(self.value)
        return widget


@dataclass
class Bool(DataItem):
    true_value: Any = True
    false_value: Any = False
    value: bool = True

    def _create_widget(self) -> custom_widgets.MappedCheckBox:
        widget = custom_widgets.MappedCheckBox(
            true_value=self.true_value, false_value=self.false_value
        )
        widget.set_value(self.value)
        return widget


@dataclass
class Color(DataItem):
    def _create_widget(self) -> custom_widgets.ColorChooserButton:
        widget = custom_widgets.ColorChooserButton()
        if self.value is not None:
            widget.set_value(self.value)
        return widget


@dataclass
class Enum(DataItem):
    choices: Iterable | Mapping | None = None
    radio: bool = False

    def _create_widget(
        self,
    ) -> custom_widgets.ColorChooserButton | widgets.ComboBox:
        if self.radio:
            widget = custom_widgets.SelectionWidget(layout="vertical")
        else:
            widget = widgets.ComboBox()
        if isinstance(self.choices, Mapping):
            widget.add_items(self.choices)
        else:
            for item in self.choices:
                if isinstance(item, tuple):
                    if len(item) == 2:
                        widget.add(item[1], item[0])
                    elif len(item) == 3:
                        widget.add(item[1], item[0], item[2])
                else:
                    widget.add(item)
        if self.value is not None:
            widget.set_value(self.value)
        return widget


@dataclass
class MultipleChoice(DataItem):
    choices: Iterable | Mapping | None = None

    def _create_widget(self) -> widgets.ListWidget:
        widget = widgets.ListWidget()
        widget.set_selection_mode("multi")
        if isinstance(self.choices, Mapping):
            widget.add_items(self.choices)
        else:
            for item in self.choices:
                if isinstance(item, tuple):
                    if len(item) == 2:
                        widget.add(item[1], item[0])
                    elif len(item) == 3:
                        widget.add(item[1], item[0], item[2])
                else:
                    widget.add(item)
        if self.value is not None:
            widget.set_value(self.value)
        return widget


@dataclass
class File(DataItem):
    formats: str = "*"
    save: bool = True
    root: None | str | pathlib.Path = None

    def _create_widget(self) -> custom_widgets.FileChooserButton:
        widget = custom_widgets.FileChooserButton(
            file_mode="any_file" if self.save else "existing_file",
            mode="save" if self.save else "open",
            root=self.root,
        )
        if self.value is not None:
            widget.set_value(self.value)
        return widget


@dataclass
class Folder(DataItem):
    root: None | str | pathlib.Path = None
    mode: widgets.filedialog.AcceptModeStr = "open"

    def _create_widget(self) -> custom_widgets.FileChooserButton:
        widget = custom_widgets.FileChooserButton(
            file_mode="directory", mode=self.mode, root=self.root
        )
        if self.value is not None:
            widget.set_value(self.value)
        return widget


@dataclass
class StringOrNumber(DataItem):
    def _create_widget(self) -> custom_widgets.StringOrNumberWidget:
        widget = custom_widgets.StringOrNumberWidget(self.label)
        if self.value is not None:
            widget.set_value(self.value)
        return widget


@dataclass
class Button(DataItem):
    callback: Callable | None = None
    icon: datatypes.IconType | None = None

    def _create_widget(self) -> widgets.PushButton:
        widget = widgets.PushButton(self.label)
        widget.set_icon(self.icon)
        callback = functools.partial(self.callback, parent=widget.window())
        widget.clicked.connect(callback)
        return widget


class DataSetMeta(type):
    def __new__(cls, name, bases, dct):
        filtered = [b for b in bases if getattr(b, "__metaclass__", None) is DataSetMeta]
        items = {item._name: item for b in filtered for item in b._items}
        # items should contain DataItems of parent classes
        for attrname, value in list(dct.items()):
            if isinstance(value, DataItem):
                value.name = attrname
                items[attrname] = value
        dct["_items"] = items
        return type.__new__(cls, name, bases, dct)


class DataSet(metaclass=DataSetMeta):
    _items: dict[str, DataItem]

    def __init__(self, title: str = "", comment: str | None = None, icon=""):
        # self.widget = custom_widgets.SettingsWidget()
        self.dialog_title = title
        self.dialog_comment = comment
        self.dialog_icon = icon

    def create_dialog(self):
        dialog = widgets.Dialog(
            window_modality="application",
            minimum_width=400,
            window_title=self.dialog_title,
            window_icon=self.dialog_icon,
        )
        dialog.set_layout("grid")
        dialog.box.set_spacing(10)
        dialog.box.set_margin(20)

        button_box = widgets.DialogButtonBox()
        ok_btn = button_box.add_default_button("ok", callback=dialog.accept)
        button_box.add_default_button("cancel", callback=dialog.reject)
        widget_dict = {k: v.create_widget() for k, v in self._items.items()}
        widget_dict = {k: v for k, v in widget_dict.items() if v is not None}

        def on_update():
            is_valid = all(
                i.is_valid() if hasattr(i, "is_valid") else True
                for i in widget_dict.values()
            )
            ok_btn.setEnabled(is_valid)

        for i, (k, item) in enumerate(self._items.items()):
            if k not in widget_dict:
                continue
            dialog.box[i, item.label_col] = widgets.Label(item.label)
            dialog.box[i, item.label_col + 1 : item.label_col + 3] = widget_dict[k]
            widget = widget_dict[k]
            widget.setObjectName(k)
            widget.value_changed.connect(on_update)
            for active in item.enabled_on:
                widget.setEnabled(widget_dict[active].get_value())
                widget_dict[active].value_changed.connect(widget.setEnabled)
            for active in item.disabled_on:
                widget.setDisabled(widget_dict[active].get_value())
                widget_dict[active].value_changed.connect(widget.setDisabled)
        if self.dialog_comment:
            label = widgets.Label(self.dialog_comment)
            label.setWordWrap(True)
            dialog.box[len(self._items) + 1, 0:3] = label
        dialog.box.append(button_box)
        on_update()
        return dialog

    def edit(self, preset: dict | None = None) -> bool:
        dialog = self.create_dialog()
        if preset:
            for item in dialog.layout():
                item_id = item.objectName()
                if item_id in preset and preset[item_id] is not None:
                    item.set_value(preset[item_id])

        if not dialog.show_blocking():
            return False
        new_values = {
            item.objectName(): item.get_value()
            for item in dialog.layout()
            if item.objectName()
        }
        enabled = {
            item.objectName(): item.isEnabled()
            for item in dialog.layout()
            if item.objectName()
        }
        # new_values = {a: (str(b) if isinstance(b, pathlib.Path) else b)
        #               for a, b in dct.items()}
        for k, item in self._items.items():
            if k in new_values:
                item.set_value(new_values[k])
                item.is_enabled = enabled[k]
        return True

    def to_dict(self) -> dict:
        return {
            k: (str(v.value) if isinstance(v.value, pathlib.Path) else v.value)
            for k, v in self._items.items()
            if v.include and v.is_enabled
        }


if __name__ == "__main__":
    app = widgets.app()

    class Test(DataSet):
        int1 = Int(label="Int", unit="ts")
        int2 = Int(label="Int", min_val=0, max_val=100, unit="ts")
        boolitem = Bool(label="Bool")
        string1 = String(label="String Regex 0-9")
        string2 = String(label="String Notempty")
        enum = Enum(label="Enum", choices=["A", "B"], disabled_on="boolitem")
        floatitem = Float(label="Float", enabled_on="boolitem")
        fileitem = File(label="File", optional="Activate")
        rangeitem = Range(label="Range", max_val=10)
        folderitem = Folder(label="Folder", include=False)
        stringornumber = StringOrNumber(label="StringOrNumber", value=2.4)
        code = Code(label="Test", value="class Test")
        regexpattern = RegexPattern("RegexPattern")
        # regex = Regex(label="Test", value="", show_error=False)

    # class Test2(Test):
    #     boolitem = None
    with app.debug_mode():
        dlg = Test(icon="mdi.timer", comment="hallo")
        if dlg.edit():
            pass
