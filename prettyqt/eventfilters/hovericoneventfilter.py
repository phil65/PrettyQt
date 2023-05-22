from __future__ import annotations

from prettyqt import core, eventfilters


class HoverIconEventFilter(eventfilters.BaseEventFilter):
    def __init__(self, normal, hover, pressed=None, parent=None):
        super().__init__(parent)
        self.normal = normal
        self.hover = hover
        self.pressed = pressed

    def eventFilter(self, obj, event: core.Event) -> bool:
        # if obj is not self.parent():
        #     return super().eventFilter(obj, event)
        match event.type():
            case core.Event.Type.Enter | core.Event.Type.MouseButtonRelease if self.hover:
                obj.set_icon(self.hover)
            case core.Event.Type.Leave:
                obj.set_icon(self.normal)
            case core.Event.Type.MouseButtonPress if self.pressed:
                obj.set_icon(self.pressed)
        return super().eventFilter(obj, event)


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    widget = widgets.PushButton()
    widget.set_icon("mdi.folder")
    test = HoverIconEventFilter("mdi.folder", "mdi.folder-outline", "mdi.timer", widget)
    widget.installEventFilter(test)
    widget.show()
    app.main_loop()
