from __future__ import annotations

from prettyqt import core, widgets


class HoverIconEventFilter(core.Object):
    def __init__(self, normal, hover, parent=None):
        super().__init__(parent)
        self.normal = normal
        self.hover = hover

    def eventFilter(self, obj, event: core.Event):
        if event.type() == core.Event.Type.Enter:
            obj.set_icon(self.hover)
        elif event.type() == core.Event.Type.Leave:
            obj.set_icon(self.normal)
        return super().eventFilter(obj, event)


if __name__ == "__main__":
    app = widgets.app()
    widget = widgets.PushButton()
    test = HoverIconEventFilter("mdi.timer", "mdi.folder")
    widget.installEventFilter(test)
    widget.show()
    app.main_loop()
