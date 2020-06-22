# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

import functools
import pathlib
from typing import Optional

from prettyqt import custom_validators, custom_widgets, gui, widgets


class DataItem(object):
    def __init__(self, label, value=None, optional=False):
        self.set_value(value)
        self.label = label
        self.optional = optional
        self.colspan = 1
        self.label_col = 0
        self.active_on = list()
        self.not_active_on = list()

    def __get__(self, instance, owner):
        return self.value

    def set_pos(self, col=0, colspan=None):
        """
        Set data item's position on a GUI layout
        """
        self.label_col = col
        self.colspan = colspan
        return self

    def set_value(self, value):
        self.value = value

    def store(self, prop):
        # self.set_prop("display", store=prop)
        return self

    def set_active(self, prop):
        # self.set_prop("display", active=prop)
        self.active_on.append(prop)
        return self

    def set_not_active(self, prop):
        # self.set_prop("display", active=prop)
        self.not_active_on.append(prop)
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
    """
    Construct a float data item
        * label [string]: name
        * value [float]: default value (optional)
        * min [float]: minimum value (optional)
        * max [float]: maximum value (optional)
        * slider [bool]: if True, shows a slider widget right after the line
          edit widget (default is False)
        * step [float]: step between tick values with a slider widget (optional)
        * unit [string]: physical unit (optional)
        * check [bool]: if False, value is not checked (optional, value=True)
    """

    def __init__(self, label, value=None, min_val=None, max_val=None,
                 unit="", step=0.1, slider=False, optional=False):
        super().__init__(label, value=value, optional=optional)
        self.range = (min_val, max_val)
        self.step = step
        self.unit = unit

    def _create_widget(self):
        widget = widgets.DoubleSpinBox()
        widget.set_range(*self.range)
        widget.setSingleStep(self.step)
        widget.setSuffix(self.unit)
        if self.value is not None:
            widget.set_value(self.value)
        return widget


class Int(DataItem):
    """
    Construct an integer data item
        * label [string]: name
        * value [int]: default value (optional)
        * min [int]: minimum value (optional)
        * max [int]: maximum value (optional)
        * unit [string]: physical unit (optional)
        * slider [bool]: if True, shows a slider widget right after the line
          edit widget (default is False)
        * check [bool]: if False, value is not checked (optional, value=True)
    """

    def __init__(self, label, value=None, min_val=0, max_val=None,
                 unit="", step=1, slider=False, optional=False):
        super().__init__(label, value=value, optional=optional)
        self.range = (min_val, max_val)
        self.step = step
        self.unit = unit
        self.slider = slider

    def _create_widget(self):
        if self.slider:
            widget = custom_widgets.InputAndSlider()
        else:
            widget = widgets.SpinBox()
            widget.setSuffix(self.unit)
        widget.set_range(*self.range)
        widget.set_step_size(self.step)
        if self.value is not None:
            widget.set_value(self.value)
        return widget


class String(DataItem):
    """
    Construct a string data item
        * label [string]: name
        * value [string]: default value (optional)
        * notempty [bool]: if True, empty string is not a valid value (opt.)
    """

    def __init__(self, label, value=None, notempty=False, regex=None, optional=False):
        super().__init__(label, value=value, optional=optional)
        self.notempty = notempty
        self.regex = regex

    def _create_widget(self):
        widget = widgets.LineEdit()
        if self.notempty:
            val = custom_validators.NotEmptyValidator()
            widget.set_validator(val)
        if self.regex is not None:
            val = gui.RegExpValidator()
            val.set_regex(self.regex)
            widget.set_validator(val)
        if self.value is not None:
            widget.set_value(self.value)
        return widget


class IntList(DataItem):
    """
    Construct an IntList data item
        * label [string]: name
        * value [string]: default value (optional)
        * notempty [bool]: if True, empty string is not a valid value (opt.)
    """

    def __init__(self, label, value=None, allow_single=False, optional=False):
        super().__init__(label, value=value, optional=optional)
        self.allow_single = allow_single

    def _create_widget(self):
        widget = custom_widgets.ListInput(allow_single=self.allow_single)
        if self.value is not None:
            widget.set_value(self.value)
        return widget


class FloatList(DataItem):
    """
    Construct an FloatList data item
        * label [string]: name
        * value [string]: default value (optional)
        * notempty [bool]: if True, empty string is not a valid value (opt.)
    """

    def __init__(self, label, value=None, allow_single=False, optional=False):
        super().__init__(label, value=value, optional=optional)
        self.allow_single = allow_single

    def _create_widget(self):
        widget = custom_widgets.ListInput(allow_single=self.allow_single, typ=float)
        if self.value is not None:
            widget.set_value(self.value)
        return widget


class Bool(DataItem):
    """
    Construct a boolean data item
        * text [string]: form's field name (optional)
        * label [string]: name
        * value [string]: default value (optional)
        * check [bool]: if False, value is not checked (optional, value=True)
    """

    def __init__(self, label, value=False, optional=False,
                 true_value=True, false_value=False):
        super().__init__(label, value=value, optional=optional)
        self.true_value = true_value
        self.false_value = false_value

    def _create_widget(self):
        widget = custom_widgets.MappedCheckBox(true_value=self.true_value,
                                               false_value=self.false_value)
        if self.value is not None:
            widget.set_value(self.value)
        return widget


class Color(DataItem):
    """
    Construct a color data item
        * label [string]: name
        * value [string]: default value (optional)
        * check [bool]: if False, value is not checked (optional, value=True)

    Color values are encoded as hexadecimal strings or Qt color names
    """

    def __init__(self, label, value=None, optional=False):
        super().__init__(label, value=value, optional=optional)

    def _create_widget(self):
        widget = custom_widgets.ColorChooserButton()
        if self.value is not None:
            widget.set_value(self.value)
        return widget


class Enum(DataItem):
    """
    Construct a data item for a list of choices.
        * label [string]: name
        * choices [list, tuple or function]: string list or (key, label) list
          function of two arguments (item, value) returning a list of tuples
          (key, label, image) where image is an icon path, a QIcon instance
          or a function of one argument (key) returning a QIcon instance
        * value [-]: default label or default key (optional)
        * check [bool]: if False, value is not checked (optional, value=True)
        * radio [bool]: if True, shows radio buttons instead of a combo box
          (default is False)
    """

    def __init__(self, label, choices, value=None, optional=False, radio=False):
        super().__init__(label, value=value, optional=optional)
        self.radio = radio
        self.choices = choices

    def _create_widget(self):
        if self.radio:
            widget = custom_widgets.SelectionWidget(layout="vertical")
        else:
            widget = widgets.ComboBox()
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

    def __init__(self, label, choices, value=None, optional=False):
        super().__init__(label, value=value, optional=optional)
        self.choices = choices

    def _create_widget(self):
        widget = widgets.ListWidget()
        widget.set_selection_mode("multi")
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

    def __init__(self, label, formats="*", value=None, save=True,
                 root=None, optional=False):
        super().__init__(label, value=value, optional=optional)
        self.formats = formats.lstrip(".")
        self.root = root
        self.save = save

    def _create_widget(self):
        file_mode = "any_file" if self.save else "existing_file"
        mode = "save" if self.save else "open"
        widget = custom_widgets.FileChooserButton(file_mode=file_mode,
                                                  mode=mode,
                                                  root=self.root)
        if self.value is not None:
            widget.set_value(self.value)
        return widget


class Folder(DataItem):

    def __init__(self, label, value=None, root=None, mode="open", optional=False):
        super().__init__(label, value=value, optional=optional)
        self.mode = mode
        self.root = root

    def _create_widget(self):
        widget = custom_widgets.FileChooserButton(file_mode="directory",
                                                  mode=self.mode,
                                                  root=self.root)
        if self.value is not None:
            widget.set_value(self.value)
        return widget


class StringOrNumber(DataItem):

    def _create_widget(self):
        widget = custom_widgets.StringOrNumberWidget(self.label)
        if self.value is not None:
            widget.set_value(self.value)
        return widget


class Button(DataItem):
    """
    Construct a simple button that calls a method when hit
        * label [string]: text shown on the button
        * callback [function]: function with four params (dataset, item, value, parent)
            - dataset [DataSet]: instance of the parent dataset
            - item [DataItem]: instance of Button (i.e. self)
            - value [unspecified]: value of Button (default Button
              value or last value returned by the callback)
            - parent [QObject]: button's parent widget
        * icon [QIcon or string]: icon show on the button (optional)
        * check [bool]: if False, value is not checked (optional, value=True)
    """

    def __init__(self, label, callback, icon=None, value=None):
        super().__init__("", value=value)
        self.button_label = label
        self.icon = icon
        self.callback = callback

    def _create_widget(self):
        widget = widgets.PushButton(self.button_label)
        widget.set_icon(self.icon)
        if self.value is not None:
            widget.set_value(self.value)
        callback = functools.partial(self.callback, parent=widget.window())
        widget.clicked.connect(callback)
        return widget


class DataSetMeta(type):
    """
    DataSet metaclass

    Create class attribute `_items`: list of the DataSet class attributes,
    created in the same order as these attributes were written
    """
    def __new__(mcs, name, bases, dct):
        filtered = [b for b in bases if getattr(b, "__metaclass__", None) is DataSetMeta]
        items = {item._name: item for b in filtered for item in b._items}
        for attrname, value in list(dct.items()):
            if isinstance(value, DataItem):
                items[attrname] = value
        dct["_items"] = items
        return type.__new__(mcs, name, bases, dct)


class DataSet(object, metaclass=DataSetMeta):

    def __init__(self, title=None, comment=None, icon=""):
        # self.widget = custom_widgets.SettingsWidget()
        self.dialog_title = title
        self.dialog_comment = comment
        self.dialog_icon = icon
        self.ok_btn = None

    def create_dialog(self):
        dialog = widgets.BaseDialog()
        dialog.set_modality("application")
        dialog.setMinimumWidth(400)
        dialog.title = self.dialog_title
        dialog.set_icon(self.dialog_icon)
        dialog.set_layout("grid")
        dialog.box.set_spacing(10)
        dialog.box.set_margin(20)

        button_box = widgets.DialogButtonBox()
        self.ok_btn = button_box.add_default_button("ok", callback=dialog.accept)
        button_box.add_default_button("cancel", callback=dialog.reject)
        widget_dict = {k: v.create_widget() for k, v in self._items.items()}
        widget_dict = {k: v for k, v in widget_dict.items() if v is not None}

        def on_update():
            is_valid = all(i.is_valid() if hasattr(i, "is_valid") else True
                           for i in widget_dict.values())
            self.ok_btn.setEnabled(is_valid)

        for i, (k, item) in enumerate(self._items.items()):
            dialog.box[i, item.label_col] = widgets.Label(item.label)
            dialog.box[i, item.label_col + 1:item.label_col + 3] = widget_dict[k]
            widget = widget_dict[k]
            widget.id = k
            widget.value_changed.connect(on_update)
            for active in item.active_on:
                widget.setEnabled(widget_dict[active].get_value())
                widget_dict[active].value_changed.connect(widget.setEnabled)
            for active in item.not_active_on:
                widget.setDisabled(widget_dict[active].get_value())
                widget_dict[active].value_changed.connect(widget.setDisabled)
        if self.dialog_comment:
            label = widgets.Label(self.dialog_comment)
            label.setWordWrap(True)
            dialog.box[len(self._items) + 1, 0:3] = label
        dialog.box.append(button_box)
        on_update()
        return dialog

    def edit(self, preset: Optional[dict] = None) -> bool:
        dialog = self.create_dialog()
        if preset:
            for item in dialog.layout():
                if item.id in preset and preset[item.id] is not None:
                    item.set_value(preset[item.id])

        if not dialog.show_blocking():
            return False
        new_values = {item.id: item.get_value()
                      for item in dialog.layout()
                      if item.id}
        # new_values = {a: (str(b) if isinstance(b, pathlib.Path) else b)
        #               for a, b in dct.items()}
        for k, item in self._items.items():
            if k in new_values:
                item.set_value(new_values[k])
        return True

    def to_dict(self) -> dict:
        dct = {k: v.value
               for k, v in self._items.items()
               if not isinstance(v, Button)}
        return {a: (str(b) if isinstance(b, pathlib.Path) else b)
                for a, b in dct.items()}


if __name__ == "__main__":
    app = widgets.app()

    class Test(DataSet):
        boolitem = Bool(label="Bool")
        string1 = String(label="String Regex 0-9", regex="[0-9]")
        string2 = String(label="String Notempty", notempty=True)
        enum = Enum(label="Enum", choices=["A", "B"]).set_not_active("boolitem")
        floatitem = Float(label="Float").set_active("boolitem")
        fileitem = File(label="File", optional="Activate")
        folderitem = Folder(label="Folder")
        buttonitem = Button(label="Folder", icon="mdi.folder", callback=print)
        stringornumber = StringOrNumber(label="StringOrNumber", value=2.4)

    dlg = Test(icon="mdi.timer", comment="hallo")
    # dlg.widget.value_changed.connect(print)
    if dlg.edit(dict(boolitem=True)):
        from pprint import pprint
        pprint(dlg.to_dict())
