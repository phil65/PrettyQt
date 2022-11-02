from __future__ import annotations

from collections.abc import Iterable, Mapping
import functools
import pathlib
from typing import Any, Callable

from prettyqt import custom_validators, custom_widgets, gui, widgets
from prettyqt.utils import types


class DataItem:
    def __init__(
        self,
        label: str,
        value=None,
        optional: str | None = None,
        include: bool = True,
        enabled_on=None,
        disabled_on=None,
    ):
        self.set_value(value)
        self.enabled_on = [enabled_on] if enabled_on else list()
        self.disabled_on = [disabled_on] if disabled_on else list()
        self.name = None
        self.label = label
        self.optional = optional
        self.include = include
        self.colspan = 1
        self.label_col = 0
        self.is_enabled = True

    def __get__(self, instance, owner):
        return self.value

    def set_pos(self, col=0, colspan=None):
        """Set data item's position on a GUI layout."""
        self.label_col = col
        self.colspan = colspan
        return self

    def set_value(self, value):
        self.value = value

    def store(self, prop):
        # self.set_prop("display", store=prop)
        return self

    def is_valid(self):
        return True

    def create_widget(self):
        widget = self._create_widget()
        if self.optional:
            return custom_widgets.OptionalWidget(widget, self.optional)
        return widget

    def _create_widget(self):
        return None


class Fixed(DataItem):
    pass


class Float(DataItem):
    def __init__(
        self,
        label: str,
        value: float | None = None,
        min_val: float | None = None,
        max_val: float | None = None,
        unit: str = "",
        step: float = 0.1,
        slider: bool = False,
        **kwargs,
    ):
        super().__init__(label, value=value, **kwargs)
        self.range = (min_val, max_val)
        self.step = step
        self.unit = unit

    def _create_widget(self) -> widgets.DoubleSpinBox:
        widget = widgets.DoubleSpinBox()
        widget.set_range(*self.range)
        widget.setSingleStep(self.step)
        widget.setSuffix(self.unit)
        if self.value is not None:
            widget.set_value(self.value)
        return widget


class Int(DataItem):
    def __init__(
        self,
        label: str,
        value: int | None = None,
        min_val: int | None = 0,
        max_val: int | None = None,
        unit: str = "",
        step: int = 1,
        slider: bool = False,
        **kwargs,
    ):
        super().__init__(label, value=value, **kwargs)
        self.range = (min_val, max_val)
        self.step = step
        self.unit = unit
        self.slider = slider

    def _create_widget(self) -> custom_widgets.InputAndSlider | widgets.SpinBox:
        min_val = self.range[0]
        max_val = self.range[1]
        if min_val is not None and max_val is not None:
            widget = custom_widgets.InputAndSlider()
            widget.set_range(min_val, max_val)
        else:
            widget = widgets.SpinBox()
            widget.set_range(min_val, max_val)
            widget.setSuffix(self.unit)
        widget.set_step_size(self.step)
        if self.value is not None:
            widget.set_value(self.value)
        return widget


class Range(DataItem):
    def __init__(
        self, label: str, value=None, min_val: int = 0, max_val: int = 1, **kwargs
    ):
        super().__init__(label, value=value, **kwargs)
        self.range = (min_val, max_val)
        # self.step = step
        # self.unit = unit

    def _create_widget(self) -> custom_widgets.SpanSlider:
        widget = custom_widgets.SpanSlider()
        # widget.setSuffix(self.unit)
        widget.set_range(*self.range)
        # widget.set_step_size(self.step)
        if self.value is not None:
            widget.set_value(self.value)
        return widget


class String(DataItem):
    def __init__(
        self,
        label: str,
        value: str | None = None,
        notempty: bool = False,
        regex: str | None = None,
        **kwargs,
    ):
        super().__init__(label, value=value, **kwargs)
        self.notempty = notempty
        self.regex = regex

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


class RegexPattern(DataItem):
    def __init__(
        self, label: str, value: str | None = None, notempty: bool = False, **kwargs
    ):
        super().__init__(label, value=value, **kwargs)
        self.notempty = notempty

    def _create_widget(self) -> custom_widgets.SingleLineTextEdit:
        widget = custom_widgets.SingleLineTextEdit()
        if self.notempty:
            val = custom_validators.NotEmptyValidator()
            widget.set_validator(val)
        widget.set_syntaxhighlighter("regex")
        if self.value is not None:
            widget.set_value(self.value)
        return widget


class Code(DataItem):
    def __init__(
        self, label: str, value: str | None = None, language: str = "python", **kwargs
    ):
        super().__init__(label, value=value, **kwargs)
        self.language = language

    def _create_widget(self) -> custom_widgets.CodeEditor:
        widget = custom_widgets.CodeEditor()
        if self.value is not None:
            widget.set_value(self.value)
        return widget


class Regex(DataItem):
    def __init__(
        self,
        label: str,
        value: str | None = None,
        show_flags: bool = True,
        show_error: bool = False,
        **kwargs,
    ):
        super().__init__(label, value=value, **kwargs)
        self.show_flags = show_flags
        self.show_error = show_error

    def _create_widget(self) -> custom_widgets.RegexInput:
        widget = custom_widgets.RegexInput(
            show_flags=self.show_flags, show_error=self.show_error
        )
        if self.value is not None:
            widget.set_value(self.value)
        return widget


class IntList(DataItem):
    def __init__(
        self,
        label: str,
        value: list[int] | None = None,
        allow_single: bool = False,
        **kwargs,
    ):
        super().__init__(label, value=value, **kwargs)
        self.allow_single = allow_single

    def _create_widget(self) -> custom_widgets.ListInput:
        widget = custom_widgets.ListInput(allow_single=self.allow_single)
        if self.value is not None:
            widget.set_value(self.value)
        return widget


class FloatList(DataItem):
    def __init__(
        self,
        label: str,
        value: list[float] | None = None,
        allow_single: bool = False,
        **kwargs,
    ):
        super().__init__(label, value=value, **kwargs)
        self.allow_single = allow_single

    def _create_widget(self) -> custom_widgets.ListInput:
        widget = custom_widgets.ListInput(allow_single=self.allow_single, typ=float)
        if self.value is not None:
            widget.set_value(self.value)
        return widget


class Bool(DataItem):
    def __init__(
        self,
        label: str,
        value: bool = False,
        true_value: Any = True,
        false_value: Any = False,
        **kwargs,
    ):
        super().__init__(label, value=value, **kwargs)
        self.true_value = true_value
        self.false_value = false_value

    def _create_widget(self) -> custom_widgets.MappedCheckBox:
        widget = custom_widgets.MappedCheckBox(
            true_value=self.true_value, false_value=self.false_value
        )
        widget.set_value(self.value)
        return widget


class Color(DataItem):
    def __init__(self, label: str, value=None, **kwargs):
        super().__init__(label, value=value, **kwargs)

    def _create_widget(self) -> custom_widgets.ColorChooserButton:
        widget = custom_widgets.ColorChooserButton()
        if self.value is not None:
            widget.set_value(self.value)
        return widget


class Enum(DataItem):
    def __init__(
        self,
        label: str,
        choices: Iterable | Mapping,
        value: Any = None,
        radio: bool = False,
        **kwargs,
    ):
        super().__init__(label, value=value, **kwargs)
        self.radio = radio
        self.choices = choices

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


class MultipleChoice(DataItem):
    def __init__(
        self,
        label: str,
        choices: Iterable | Mapping,
        value: list | None = None,
        **kwargs,
    ):
        super().__init__(label, value=value, **kwargs)
        self.choices = choices

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


class File(DataItem):
    def __init__(
        self,
        label: str,
        formats: str = "*",
        value: None | str | pathlib.Path = None,
        save: bool = True,
        root: None | str | pathlib.Path = None,
        **kwargs,
    ):
        super().__init__(label, value=value, **kwargs)
        self.formats = formats.lstrip(".")
        self.root = root
        self.save = save

    def _create_widget(self) -> custom_widgets.FileChooserButton:
        widget = custom_widgets.FileChooserButton(
            file_mode="any_file" if self.save else "existing_file",
            mode="save" if self.save else "open",
            root=self.root,
        )
        if self.value is not None:
            widget.set_value(self.value)
        return widget


class Folder(DataItem):
    def __init__(
        self,
        label: str,
        value: None | str | pathlib.Path = None,
        root: None | str | pathlib.Path = None,
        mode: widgets.filedialog.AcceptModeStr = "open",
        **kwargs,
    ):
        super().__init__(label, value=value, **kwargs)
        self.mode = mode
        self.root = root

    def _create_widget(self) -> custom_widgets.FileChooserButton:
        widget = custom_widgets.FileChooserButton(
            file_mode="directory", mode=self.mode, root=self.root
        )
        if self.value is not None:
            widget.set_value(self.value)
        return widget


class StringOrNumber(DataItem):
    def _create_widget(self) -> custom_widgets.StringOrNumberWidget:
        widget = custom_widgets.StringOrNumberWidget(self.label)
        if self.value is not None:
            widget.set_value(self.value)
        return widget


class Button(DataItem):
    def __init__(self, label: str, callback: Callable, icon: types.IconType = None):
        super().__init__("", value=None, include=False)
        self.button_label = label
        self.icon = icon
        self.callback = callback

    def _create_widget(self) -> widgets.PushButton:
        widget = widgets.PushButton(self.button_label)
        widget.set_icon(self.icon)
        callback = functools.partial(self.callback, parent=widget.window())
        widget.clicked.connect(callback)
        return widget


class DataSetMeta(type):
    def __new__(mcs, name, bases, dct):
        filtered = [b for b in bases if getattr(b, "__metaclass__", None) is DataSetMeta]
        items = {item._name: item for b in filtered for item in b._items}
        # items should contain DataItems of parent classes
        for attrname, value in list(dct.items()):
            if isinstance(value, DataItem):
                value.name = attrname
                items[attrname] = value
        dct["_items"] = items
        return type.__new__(mcs, name, bases, dct)


class DataSet(metaclass=DataSetMeta):
    _items: dict[str, DataItem]

    def __init__(self, title: str = "", comment: str | None = None, icon=""):
        # self.widget = custom_widgets.SettingsWidget()
        self.dialog_title = title
        self.dialog_comment = comment
        self.dialog_icon = icon

    def create_dialog(self):
        dialog = widgets.Dialog()
        dialog.set_modality("application")
        dialog.setMinimumWidth(400)
        dialog.set_title(self.dialog_title)
        dialog.set_icon(self.dialog_icon)
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
            widget.set_id(k)
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
                item_id = item.get_id()
                if item_id in preset and preset[item_id] is not None:
                    item.set_value(preset[item_id])

        if not dialog.show_blocking():
            return False
        new_values = {
            item.get_id(): item.get_value() for item in dialog.layout() if item.has_id()
        }
        enabled = {
            item.get_id(): item.isEnabled() for item in dialog.layout() if item.has_id()
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
        boolitem = Bool(label="Bool")
        string1 = String(label="String Regex 0-9")
        string2 = String(label="String Notempty")
        enum = Enum(label="Enum", choices=["A", "B"], disabled_on="boolitem")
        floatitem = Float(label="Float", enabled_on="boolitem")
        fileitem = File(label="File", optional="Activate")
        rangeitem = Range(label="Range", max_val=10)
        folderitem = Folder(label="Folder", include=False)
        buttonitem = Button(label="Folder", icon="mdi.folder", callback=print)
        stringornumber = StringOrNumber(label="StringOrNumber", value=2.4)
        code = Code(label="Test", value="class Test")
        regexpattern = RegexPattern("RegexPattern")
        regex = Regex(label="Test", value="[", show_error=False)

    # class Test2(Test):
    #     boolitem = None

    dlg = Test(icon="mdi.timer", comment="hallo")
    # dlg.widget.value_changed.connect(print)
    if dlg.edit(dict(boolitem=True)):
        from pprint import pprint

        pprint(dlg.to_dict())
