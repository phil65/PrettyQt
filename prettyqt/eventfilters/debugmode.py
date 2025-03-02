from __future__ import annotations

import logging

from prettyqt import constants, core, eventfilters, widgets


logger = logging.getLogger(__name__)


class DebugMode(eventfilters.BaseEventFilter):
    ID = "debug_mode"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.menu = widgets.Menu(
            hovered=self._on_entered,
            triggered=self._on_clicked,
            about_to_hide=self._on_hide,
        )
        self.frame = widgets.RubberBand("rectangle")
        self.frame.setObjectName("testframe")

    def eventFilter(self, source: core.QObject, event: core.QEvent) -> bool:
        border_keys = [constants.Key.Key_Control, constants.Key.Key_Alt]
        match event.type():
            case core.Event.Type.KeyPress if event.key() in border_keys:
                with widgets.app().edit_stylesheet() as ss:
                    ss.QWidget.border.setValue("1px solid red")
            case core.Event.Type.KeyRelease if event.key() in border_keys:
                widgets.app().setStyleSheet("")
            case core.Event.Type.MouseButtonPress:
                mods = widgets.Application.query_keyboard_modifiers()
                if "ctrl" in mods:
                    pos = source.mapToGlobal(event.pos())
                    candidates = widgets.Application.widgets_at(pos)
                    self.menu.clear()
                    for candidate in candidates:
                        self.menu.add_action(text=repr(candidate), data=candidate)
                    self.menu.exec(pos)
                    return True
                if "alt" in mods:
                    from prettyqt import ipython

                    self.frame.hide()
                    console = ipython.InProcessIPythonWidget(self)
                    console.show()
                    pos = source.mapToGlobal(event.pos())
                    widgets.Application.sleep(1)
                    variables = {}
                    i = 0
                    for w in widgets.Application.widgets_at(pos):
                        if (name := w.objectName()) and name not in variables:
                            variables[name] = w
                        else:
                            name = f"{type(w).__name__}_{i}".lower()
                            variables[name] = w
                            i += 1
                    console.push_vars(dict(app=widgets.app(), **variables))
            # case core.QEvent.Type.ToolTip if source.isWidgetType():
            #     metaobj = core.MetaObject(source.metaObject())
            #     lines = [
            #         f"{k}: {v!r}"
            #         for k, v in metaobj.get_property_values(source).items()
            #         if not k == "toolTip"
            #     ]
            #     source.setToolTip("<br>".join(lines))

        return False

    def _on_hide(self):
        self.frame.hide()

    def _on_clicked(self, item):
        from prettyqt import debugging

        logger.debug("clicked on %s", item)
        widget = item.data()
        self.editor = debugging.QObjectDetailsDialog(widget)
        self.menu.close()
        # self.frame.hide()
        self.editor.show()

    def _on_entered(self, index):
        widget = index.data()
        # logger.info(widget)
        for item in self.menu:
            if item.data() == widget:
                self.frame.resize(widget.size())
                # self.frame.setParent(widget)
                pos = widget.mapToGlobal(core.Point(0, 0))
                self.frame.move(pos)
                self.menu.raise_()
                self.frame.show()


if __name__ == "__main__":
    app = widgets.app()
    container = widgets.Widget()
    container.set_layout("horizontal")
    w = widgets.PlainTextEdit(parent=container)
    w2 = widgets.RadioButton(parent=container)
    container.box.add(w)
    container.box.add(w2)
    container.show()
    with app.debug_mode():
        app.sleep(1)
        app.exec()
