# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from prettyqt import custom_validators, custom_widgets, gui, widgets


class DataItem(object):
    def __init__(self, label, *args, **kwargs):
        self.label = label
        self.colspan = 1
        self.label_col = 0
        self.active_on = list()
        self.not_active_on = list()
        self.widget = None

    def __get__(self, instance, owner):
        return self.widget.get_value()

    def set_pos(self, col=0, colspan=None):
        """
        Set data item's position on a GUI layout
        """
        self.label_col = col
        self.colspan = colspan
        return self

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
                 unit="", step=0.1, slider=False, check=True):
        super().__init__(label, value=value, min_val=min_val,
                         max_val=max_val, unit=unit, check=check)
        self.value = value
        self.range = (min_val, max_val)
        self.step = step
        self.unit = unit
        self.widget = self.create_widget()

    def create_widget(self):
        self.widget = widgets.DoubleSpinBox()
        self.widget.set_range(*self.range)
        self.widget.setSingleStep(self.step)
        self.widget.setSuffix(self.unit)
        if self.value is not None:
            self.widget.set_value(self.value)
        return self.widget


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
                 unit="", step=1, slider=False, check=True):
        super().__init__(label, value=value, min_val=min_val, max_val=max_val,
                         unit=unit, check=check)
        self.value = value
        self.range = (min_val, max_val)
        self.step = step
        self.unit = unit
        self.slider = slider
        self.widget = self.create_widget()

    def create_widget(self):
        if self.slider:
            self.widget = widgets.Slider()
        else:
            self.widget = widgets.SpinBox()
            self.widget.setSuffix(self.unit)
        self.widget.set_range(*self.range)
        self.widget.setSingleStep(self.step)
        if self.value is not None:
            self.widget.set_value(self.value)
        return self.widget


class String(DataItem):
    """
    Construct a string data item
        * label [string]: name
        * value [string]: default value (optional)
        * notempty [bool]: if True, empty string is not a valid value (opt.)
    """

    def __init__(self, label, value=None, notempty=False, regex=None):
        super().__init__(label, value=value)
        self.value = value
        self.notempty = notempty
        self.regex = regex
        self.widget = self.create_widget()

    def create_widget(self):
        self.widget = widgets.LineEdit()
        if self.notempty:
            val = custom_validators.NotEmptyValidator()
            self.widget.set_validator(val)
        if self.regex is not None:
            val = gui.RegExpValidator()
            val.set_regex(self.regex)
            self.widget.set_validator(val)
        if self.value is not None:
            self.widget.set_value(self.value)
        return self.widget

    def is_valid(self):
        return self.widget.is_valid()


class Bool(DataItem):
    """
    Construct a boolean data item
        * text [string]: form's field name (optional)
        * label [string]: name
        * value [string]: default value (optional)
        * check [bool]: if False, value is not checked (optional, value=True)
    """

    def __init__(self, label, value=None, check=True, use_push=False):
        super().__init__(label, value=value, check=check)
        self.use_push = use_push
        self.value = value
        self.widget = self.create_widget()

    def create_widget(self):
        if self.use_push:
            self.widget = widgets.PushButton()
            self.widget.setCheckable(True)
        else:
            self.widget = widgets.CheckBox()
        if self.value is not None:
            self.widget.set_value(self.value)
        return self.widget


class Color(DataItem):
    """
    Construct a color data item
        * label [string]: name
        * value [string]: default value (optional)
        * check [bool]: if False, value is not checked (optional, value=True)

    Color values are encoded as hexadecimal strings or Qt color names
    """

    def __init__(self, label, value=None, check=True):
        super().__init__(label, value=value, check=check)
        self.value = value
        self.widget = self.create_widget()

    def create_widget(self):
        self.widget = custom_widgets.ColorChooserButton()
        if self.value is not None:
            self.widget.set_value(self.value)
        return self.widget


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

    def __init__(self, label, choices, value=None, check=True, radio=False):
        super().__init__(label, value=value, check=check)
        self.value = value
        self.radio = radio
        self.choices = choices
        self.widget = self.create_widget()

    def create_widget(self):
        if self.radio:
            self.widget = custom_widgets.SelectionWidget(layout="vertical")
        else:
            self.widget = widgets.ComboBox()
        for item in self.choices:
            if isinstance(item, tuple):
                if len(item) == 2:
                    self.widget.add(item[1], item[0])
                elif len(item) == 3:
                    self.widget.add(item[1], item[0], item[2])
            else:
                self.widget.add(item)
        if self.value is not None:
            self.widget.set_value(self.value)
        return self.widget


class MultipleChoiceItem(DataItem):

    def __init__(self, label, choices, value=None, check=True):
        super().__init__(label, value=value, check=check)
        self.value = value
        self.choices = choices
        self.widget = self.create_widget()

    def create_widget(self):
        self.widget = widgets.ListWidget()
        self.widget.set_selection_mode("multi")
        for item in self.choices:
            if isinstance(item, tuple):
                if len(item) == 2:
                    self.widget.add(item[1], item[0])
                elif len(item) == 3:
                    self.widget.add(item[1], item[0], item[2])
            else:
                self.widget.add(item)
        if self.value is not None:
            self.widget.set_value(self.value)
        return self.widget


class FileSaveItem(DataItem):

    def __init__(self, label, formats="*", value=None, basedir=None, check=True):
        super().__init__(label, value=value, check=check)
        self.value = value
        self.widget = self.create_widget()

    def create_widget(self):
        self.widget = custom_widgets.FileChooserButton()
        if self.value is not None:
            self.widget.set_value(self.value)
        return self.widget


class ButtonItem(DataItem):
    """
    Construct a simple button that calls a method when hit
        * label [string]: text shown on the button
        * callback [function]: function with four params (dataset, item, value, parent)
            - dataset [DataSet]: instance of the parent dataset
            - item [DataItem]: instance of ButtonItem (i.e. self)
            - value [unspecified]: value of ButtonItem (default ButtonItem
              value or last value returned by the callback)
            - parent [QObject]: button's parent widget
        * icon [QIcon or string]: icon show on the button (optional)
          (string: icon filename as in guidata/guiqwt image search paths)
        * value [unspecified]: default value passed to the callback (optional)
        * check [bool]: if False, value is not checked (optional, value=True)

    The value of this item is unspecified but is passed to the callback along
    with the whole dataset. The value is assigned the callback`s return value.
    """

    def __init__(self, label, callback, icon=None, value=None, check=True):
        super().__init__("", value=value, check=check)
        self.button_label = label
        self.value = value
        self.widget = self.create_widget()

    def create_widget(self):
        self.widget = widgets.PushButton(self.button_label)
        if self.value is not None:
            self.widget.set_value(self.value)
        return self.widget


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
        self.dialog = self.create_dialog()

    def create_dialog(self):
        dialog = widgets.BaseDialog()
        dialog.set_modality("application")
        dialog.setMinimumWidth(400)
        dialog.title = self.dialog_title
        dialog.set_icon(self.dialog_icon)
        dialog.set_layout("grid")
        dialog.box.set_spacing(20)
        dialog.box.set_margin(20)
        for i, (k, item) in enumerate(self._items.items()):
            dialog.box[i, item.label_col] = widgets.Label(item.label)
            widget = item.create_widget()
            dialog.box[i, item.label_col + 1:item.label_col + 3] = widget
            widget.id = k
            widget.value_changed.connect(self.on_update)
            for active in item.active_on:
                widget.setEnabled(self._items[active].widget.get_value())
                self._items[active].widget.value_changed.connect(widget.setEnabled)
            for active in item.not_active_on:
                widget.setDisabled(self._items[active].widget.get_value())
                self._items[active].widget.value_changed.connect(widget.setDisabled)
        if self.dialog_comment:
            label = widgets.Label(self.dialog_comment)
            label.setWordWrap(True)
            dialog.box[i + 1, 0:3] = label
        button_box = widgets.DialogButtonBox()
        self.ok_btn = button_box.add_default_button("ok", callback=dialog.accept)
        button_box.add_default_button("cancel", callback=dialog.reject)
        dialog.box.append(button_box)
        self.on_update()
        self.dialog = dialog
        return dialog

    def edit(self):
        return self.dialog.show_blocking()

    def to_dict(self):
        return {item.id: item.get_value()
                for item in self.dialog.layout()
                if item.id}

    def build_from_dict(self, dct):
        for item in self.dialog.layout():
            if item.id in dct and dct[item.id] is not None:
                item.set_value(dct[item.id])

    def on_update(self):
        is_valid = all(i.is_valid() for i in self._items.values())
        self.ok_btn.setEnabled(is_valid)


if __name__ == "__main__":
    app = widgets.app()

    class Test(DataSet):
        boolitem = Bool(label="My first one")
        string1 = String(label="My first one", regex="[0-9]")
        string2 = String(label="My second one", notempty=True)
        stringitem = Enum(label="A", choices=["A", "B"]).set_not_active("boolitem")
        floatitem = Float(label="My first one").set_active("boolitem")

    dlg = Test(icon="mdi.timer")
    # dlg.widget.value_changed.connect(print)
    if dlg.edit():
        from pprint import pprint
        pprint(dlg.to_dict())
