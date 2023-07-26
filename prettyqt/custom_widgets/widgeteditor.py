from __future__ import annotations

import logging

from prettyqt import core, eventfilters, widgets
from prettyqt.utils import bidict, datatypes, helpers


logger = logging.getLogger(__name__)


class WidgetEditor(widgets.Widget):
    value_changed = core.Signal(object)

    def __init__(self, qobject: core.QObject, connect: bool = True, **kwargs):
        super().__init__(**kwargs)
        self.set_layout("form")
        self._qobject = qobject
        self._initial_prop_values = {}
        self.event_catcher = eventfilters.EventCatcher(
            include=["resize", "move"], parent=self._qobject
        )
        if connect:
            self.event_catcher.caught.connect(self._update_editors)
            self._qobject.installEventFilter(self.event_catcher)
        self.set_minimum_size(800, 1000)
        self._editors = bidict()
        self._metaobj = core.MetaObject(self._qobject.metaObject())
        for i, prop in enumerate(self._metaobj.get_properties()):
            value = prop.read(self._qobject)
            # typ = prop.get_meta_type().get_type()
            name = prop.name()
            logger.info(f"setting {name} editor to {value}")
            widget = datatypes.get_editor_for_value(value)
            if widget is None:
                logger.warning(f"No editor found for {value!r}")
                continue
            widget.set_value(value)
            widget.value_changed.connect(self._on_value_change)
            widget.setEnabled(prop.isWritable())
            label = helpers.to_snake(prop.name()).replace("_", " ")
            self.box[i, "left"] = widgets.Label(label)
            self.box[i, "right"] = widget
            self._initial_prop_values[name] = value
            self._editors[name] = widget
            if prop.hasNotifySignal() and connect:
                notify_signal = prop.get_notify_signal()
                signal_name = notify_signal.get_name()
                signal = self._qobject.__getattribute__(signal_name)
                signal.connect(self._update_editors)

    # @classmethod
    # def setup_example(cls):
    #     scrollarea = widgets.ScrollArea()
    #     return cls(scrollarea, connect=False)

    def _on_value_change(self):
        editor = self.sender()
        prop_name = self._editors.inverse[editor]
        prop = self._metaobj.get_property(prop_name)
        value = editor.get_value()
        value = datatypes.make_qtype(value)
        # logger.debug(f"setting {prop_name} to {value}")
        prop.write(self._qobject, value)
        # brute force
        if isinstance(self._qobject, widgets.QWidget):
            self._qobject.updateGeometry()
            self._qobject.repaint()
            if (parent := self._qobject.parentWidget()) is not None:
                parent.updateGeometry()
                parent.repaint()

    def _update_editors(self):
        for prop_name, editor in self._editors.items():
            value = self._qobject.property(prop_name)
            editor.set_value(value)


if __name__ == "__main__":
    app = widgets.app()
    w = widgets.PlainTextEdit()
    w.show()
    editor = WidgetEditor(w)
    editor.show()
    with app.debug_mode():
        app.exec()
