from __future__ import annotations

import enum
import logging

from prettyqt import core, custom_widgets, widgets
from prettyqt.qt import QtCore, QtGui, QtWidgets
from prettyqt.utils import bidict, datatypes


logger = logging.getLogger(__name__)


class WidgetEditor(widgets.ScrollArea):
    value_changed = core.Signal(object)

    def __init__(self, widget, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._widget = widget
        container = widgets.Widget()
        container.set_layout("form")
        self.setWidget(container)
        self.set_minimum_size(800, 1000)
        self.editors = bidict()
        # self.add_widget(container)
        metaobj = self._widget.get_metaobject()
        for i, prop in enumerate(metaobj.get_properties()):
            value = prop.read(widget)
            typ = prop.get_meta_type().get_type()
            name = prop.name()
            logger.info(f"setting {name} editor to {value}")
            if typ == bool:
                widget = widgets.CheckBox()
            elif typ == int:
                widget = widgets.SpinBox(maximum=999999)
            elif typ == float:
                widget = widgets.DoubleSpinBox(maximum=999999.0)
            elif typ == str:
                widget = widgets.LineEdit()
            elif typ == QtCore.QPoint:
                widget = custom_widgets.PointEdit()
            elif typ == QtCore.QRect:
                widget = custom_widgets.RectEdit()
            elif typ == QtGui.QRegion:
                widget = custom_widgets.RegionEdit()
            elif typ == QtCore.QSize:
                widget = custom_widgets.SizeEdit()
            elif typ == QtWidgets.QSizePolicy:
                widget = custom_widgets.SizePolicyEdit()
            elif typ == QtGui.QPalette:
                widget = custom_widgets.PaletteEdit()
            elif typ == QtGui.QIcon:
                widget = custom_widgets.IconEdit()
            elif typ == QtGui.QCursor:
                widget = custom_widgets.CursorEdit()
            elif typ == QtCore.QLocale:
                widget = custom_widgets.LocaleEdit()
            elif typ == QtGui.QFont:
                widget = widgets.FontComboBox()
            elif typ == QtGui.QColor:
                widget = custom_widgets.ColorComboBox()
            elif typ == enum.Enum:
                widget = custom_widgets.EnumComboBox(enum_class=type(value))
            else:
                raise ValueError(typ)
            widget.set_value(value)
            widget.value_changed.connect(self._on_value_change)
            widget.setEnabled(prop.isWritable())
            self.editors[name] = widget
            container.box[i, "left"] = widgets.Label(prop.name())
            container.box[i, "right"] = widget
            self.ensureWidgetVisible(container)
        self.setWidgetResizable(True)

    def _on_value_change(self):
        editor = self.sender()
        prop_name = self.editors.inverse[editor]
        prop = self._widget.get_metaobject().get_property(prop_name)
        value = editor.get_value()
        value = datatypes.make_qtype(value)
        logger.info(f"setting {prop_name} to {value}")
        prop.write(self._widget, value)
        self._widget.updateGeometry()
        self._widget.repaint()
        self._widget.parentWidget().updateGeometry()
        self._widget.parentWidget().repaint()


if __name__ == "__main__":
    app = widgets.app()
    app.enable_debug_mode()
    import sys

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    container = widgets.Widget()
    container.set_layout("horizontal")
    w = widgets.PlainTextEdit(parent=container)
    w2 = widgets.PlainTextEdit(parent=container)
    container.box.add(w)
    container.box.add(w2)
    container.show()
    editor = WidgetEditor(w)
    editor.show()
    app.main_loop()
    print(w.get_properties())
