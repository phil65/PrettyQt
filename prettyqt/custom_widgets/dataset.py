# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from prettyqt import custom_widgets, widgets


class DataItem(object):
    def __init__(self, label, *args, **kwargs):
        self.label = label
        self.colspan = 1
        self.label_col = 0
        self.active_on = list()
        self.not_active_on = list()

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


class FloatItem(DataItem):
    """
    Construct a float data item
        * label [string]: name
        * default [float]: default value (optional)
        * min [float]: minimum value (optional)
        * max [float]: maximum value (optional)
        * slider [bool]: if True, shows a slider widget right after the line
          edit widget (default is False)
        * step [float]: step between tick values with a slider widget (optional)
        * unit [string]: physical unit (optional)
        * check [bool]: if False, value is not checked (optional, default=True)
    """

    def __init__(self, label, default=None, min_val=None, max_val=None,
                 unit="", step=0.1, slider=False, check=True):
        super().__init__(label, default=default, min_val=min_val,
                         max_val=max_val, unit=unit, check=check)
        self.widget = widgets.DoubleSpinBox()
        self.widget.set_range(min_val, max_val)
        self.widget.setSingleStep(step)
        self.widget.setSuffix(unit)
        if default is not None:
            self.widget.set_value(default)


class IntItem(DataItem):
    """
    Construct an integer data item
        * label [string]: name
        * default [int]: default value (optional)
        * min [int]: minimum value (optional)
        * max [int]: maximum value (optional)
        * unit [string]: physical unit (optional)
        * slider [bool]: if True, shows a slider widget right after the line
          edit widget (default is False)
        * check [bool]: if False, value is not checked (optional, default=True)
    """

    def __init__(self, label, default=None, min_val=0, max_val=None,
                 unit="", step=1, slider=False, check=True):
        super().__init__(label, default=default, min_val=min_val, max_val=max_val,
                         unit=unit, check=check)
        if slider:
            self.widget = widgets.Slider()
        else:
            self.widget = widgets.SpinBox()
            self.widget.setSuffix(unit)
        self.widget.set_range(min_val, max_val)
        self.widget.setSingleStep(step)
        if default is not None:
            self.widget.set_value(default)


class StringItem(DataItem):
    """
    Construct a string data item
        * label [string]: name
        * default [string]: default value (optional)
        * notempty [bool]: if True, empty string is not a valid value (opt.)
    """

    def __init__(self, label, default=None, notempty=None,
                 regex=None):
        super().__init__(label, default=default)
        self.widget = widgets.LineEdit()
        if default is not None:
            self.widget.set_value(default)


class BoolItem(DataItem):
    """
    Construct a boolean data item
        * text [string]: form's field name (optional)
        * label [string]: name
        * default [string]: default value (optional)
        * check [bool]: if False, value is not checked (optional, default=True)
    """

    def __init__(self, label, default=None, check=True, use_push=False):
        super().__init__(label, default=default, check=check)
        if use_push:
            self.widget = widgets.PushButton()
            self.widget.setCheckable(True)
        else:
            self.widget = widgets.CheckBox()
        if default is not None:
            self.widget.set_value(default)


class ColorItem(DataItem):
    """
    Construct a color data item
        * label [string]: name
        * default [string]: default value (optional)
        * check [bool]: if False, value is not checked (optional, default=True)

    Color values are encoded as hexadecimal strings or Qt color names
    """

    def __init__(self, label, default=None, check=True):
        super().__init__(label, default=default, check=check)
        self.widget = custom_widgets.ColorChooserButton()
        if default is not None:
            self.widget.set_value(default)


class ChoiceItem(DataItem):
    """
    Construct a data item for a list of choices.
        * label [string]: name
        * choices [list, tuple or function]: string list or (key, label) list
          function of two arguments (item, value) returning a list of tuples
          (key, label, image) where image is an icon path, a QIcon instance
          or a function of one argument (key) returning a QIcon instance
        * default [-]: default label or default key (optional)
        * check [bool]: if False, value is not checked (optional, default=True)
        * radio [bool]: if True, shows radio buttons instead of a combo box
          (default is False)
    """

    def __init__(self, label, choices, default=None, check=True, radio=False):
        super().__init__(label, default=default, check=check)
        if radio:
            self.widget = custom_widgets.SelectionWidget(layout="vertical")
        else:
            self.widget = widgets.ComboBox()
        for item in choices:
            if isinstance(item, tuple):
                if len(item) == 2:
                    self.widget.add(item[1], item[0])
                elif len(item) == 3:
                    self.widget.add(item[1], item[0], item[2])
            else:
                self.widget.add(item)
        if default is not None:
            self.widget.set_value(default)


class ImageChoiceItem(ChoiceItem):
    pass


class MultipleChoiceItem(DataItem):

    def __init__(self, label, choices, default=None, check=True):
        super().__init__(label, default=default, check=check)
        self.widget = widgets.ListWidget()
        self.widget.set_selection_mode("multi")
        for item in choices:
            if isinstance(item, tuple):
                if len(item) == 2:
                    self.widget.add(item[1], item[0])
                elif len(item) == 3:
                    self.widget.add(item[1], item[0], item[2])
            else:
                self.widget.add(item)
        if default is not None:
            self.widget.set_value(default)


class FileSaveItem(DataItem):

    def __init__(self, label, formats="*", default=None, basedir=None, check=True):
        super().__init__(label, default=default, check=check)
        self.widget = custom_widgets.FileChooserButton()
        if default is not None:
            self.widget.set_value(default)


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
        * default [unspecified]: default value passed to the callback (optional)
        * check [bool]: if False, value is not checked (optional, default=True)

    The value of this item is unspecified but is passed to the callback along
    with the whole dataset. The value is assigned the callback`s return value.
    """

    def __init__(self, label, callback, icon=None, default=None, check=True):
        super().__init__("", default=default, check=check)
        self.widget = widgets.PushButton(label)
        if default is not None:
            self.widget.set_value(default)


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
        self.dialog = widgets.BaseDialog()
        self.dialog.set_modality("application")
        self.dialog.setMinimumWidth(400)
        self.dialog.title = title
        self.dialog.set_icon(icon)
        self.dialog.set_layout("grid")
        self.dialog.box.setSpacing(20)
        self.dialog.box.set_margin(20)
        for i, (k, item) in enumerate(self._items.items()):
            self.dialog.box[i, item.label_col] = widgets.Label(item.label)
            self.dialog.box[i, item.label_col + 1:item.label_col + 3] = item.widget
            item.widget.id = k
            for active in item.active_on:
                item.widget.setEnabled(self._items[active].widget.get_value())
                self._items[active].widget.value_changed.connect(item.widget.setEnabled)
            for active in item.not_active_on:
                item.widget.setDisabled(self._items[active].widget.get_value())
                self._items[active].widget.value_changed.connect(item.widget.setDisabled)
        if comment:
            label = widgets.Label(comment)
            label.setWordWrap(True)
            self.dialog.box[i + 1, 0:3] = label
        self.dialog.add_buttonbox()

    def edit(self):
        return self.dialog.show_blocking()

    def to_dict(self):
        return {item.id: item.get_value()
                for item in self.dialog.layout()
                if item.id}

    def from_dict(self, dct):
        for item in self.dialog.layout():
            if item.id in dct and dct[item.id] is not None:
                item.set_value(dct[item.id])


if __name__ == "__main__":
    app = widgets.app()

    class Test(DataSet):
        boolitem = BoolItem(label="My first one")
        stringitem = ChoiceItem(label="A", choices=["A", "B"]).set_not_active("boolitem")
        floatitem = FloatItem(label="My first one").set_active("boolitem")

    dlg = Test(icon="mdi.timer")
    # dlg.widget.value_changed.connect(print)
    if dlg.edit():
        from pprint import pprint
        pprint(dlg.to_dict())
