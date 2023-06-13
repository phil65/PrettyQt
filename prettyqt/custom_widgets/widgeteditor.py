from __future__ import annotations

import builtins
import enum
import logging

from prettyqt import core, custom_widgets, eventfilters, widgets
from prettyqt.qt import QtCore, QtGui, QtWidgets
from prettyqt.utils import bidict, datatypes, helpers


logger = logging.getLogger(__name__)


def widget_for_type(typ: type):
    match typ:
        case builtins.bool:
            return widgets.CheckBox()
        case builtins.int:
            return widgets.SpinBox(maximum=999999)
        case builtins.float:
            return widgets.DoubleSpinBox(maximum=999999.0)
        case builtins.str:
            return widgets.LineEdit()
        case QtCore.QPoint:
            return custom_widgets.PointEdit()
        case QtCore.QRect:
            return custom_widgets.RectEdit()
        case QtGui.QRegion:
            return custom_widgets.RegionEdit()
        case QtCore.QSize:
            return custom_widgets.SizeEdit()
        case QtWidgets.QSizePolicy:
            return custom_widgets.SizePolicyEdit()
        case QtGui.QPalette:
            return custom_widgets.PaletteEdit()
        case QtGui.QIcon:
            return custom_widgets.IconEdit()
        case QtGui.QCursor:
            return custom_widgets.CursorEdit()
        case QtCore.QLocale:
            return custom_widgets.LocaleEdit()
        case QtGui.QFont:
            return widgets.FontComboBox()
        case QtGui.QColor:
            return custom_widgets.ColorComboBox()
        case enum.Flag:
            return custom_widgets.EnumFlagWidget()
        case enum.Enum:
            return custom_widgets.EnumComboBox()
        case _:
            raise ValueError(typ)


class WidgetEditor(widgets.ScrollArea):
    value_changed = core.Signal(object)

    def __init__(self, widget: QtWidgets.QWidget, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._widget = widget
        self._initial_prop_values = {}
        self.event_catcher = eventfilters.EventCatcher(
            exclude=QtCore.QEvent.Type.Paint, parent=self._widget
        )
        self.event_catcher.caught.connect(self._update_editors)
        self._widget.installEventFilter(self.event_catcher)
        container = widgets.Widget()
        container.set_layout("form")
        self.setWidget(container)
        self.set_minimum_size(800, 1000)
        self._editors = bidict()
        # self.add_widget(container)
        self._metaobj = core.MetaObject(self._widget.metaObject())
        for i, prop in enumerate(self._metaobj.get_properties()):
            value = prop.read(self._widget)
            typ = prop.get_meta_type().get_type()
            name = prop.name()
            logger.info(f"setting {name} editor to {value}")
            widget = widget_for_type(typ)
            widget.set_value(value)
            widget.value_changed.connect(self._on_value_change)
            widget.setEnabled(prop.isWritable())
            label = helpers.to_snake(prop.name()).replace("_", " ")
            container.box[i, "left"] = widgets.Label(label)
            container.box[i, "right"] = widget
            self._initial_prop_values[name] = value
            self._editors[name] = widget
            if prop.hasNotifySignal():
                notify_signal = prop.get_notify_signal()
                signal_name = notify_signal.get_name()
                signal = self._widget.__getattribute__(signal_name)
                signal.connect(self._update_editors)
            self.ensureWidgetVisible(container)
        self.setWidgetResizable(True)

    def _on_value_change(self):
        editor = self.sender()
        prop_name = self._editors.inverse[editor]
        prop = self._metaobj.get_property(prop_name)
        value = editor.get_value()
        value = datatypes.make_qtype(value)
        logger.info(f"setting {prop_name} to {value}")
        prop.write(self._widget, value)
        # brute force
        self._widget.updateGeometry()
        self._widget.repaint()
        if (parent := self._widget.parentWidget()) is not None:
            parent.updateGeometry()
            parent.repaint()

    def _update_editors(self):
        for i in range(self._widget.metaObject().propertyCount()):
            prop = self._widget.metaObject().property(i)
            prop_name = prop.name()
            editor = self._editors[prop_name]
            value = prop.read(self._widget)
            editor.set_value(value)


if __name__ == "__main__":
    app = widgets.app()
    container = widgets.Widget()
    container.set_layout("horizontal")
    w = widgets.PlainTextEdit(parent=container)
    w2 = widgets.PlainTextEdit(parent=container)
    container.box.add(w)
    container.box.add(w2)
    container.show()
    editor = WidgetEditor(w)
    editor.show()
    with app.debug_mode():
        app.main_loop()
