from __future__ import annotations

from prettyqt import gui, eventfilters


class ClickableLabelEventFilter(eventfilters.BaseEventFilter):
    """Eventfilter which underlines text on hover."""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        parent.setFont(gui.Font("Arial"))
        parent.setFixedHeight(24)
        parent.set_size_policy("minimum", "expanding")

    def eventFilter(self, source, event):
        match event.type():
            case event.Type.Enter:
                with source.edit_font() as font:
                    font.setUnderline(True)
                source.set_cursor("pointing_hand")
                source.update()
            case event.Type.Leave:
                with source.edit_font() as font:
                    font.setUnderline(False)
                source.unsetCursor()
        return False

    def setText(self, text: str):
        fm = gui.FontMetrics(self.parent().font())
        width = fm.width(text)
        self.parent().setFixedWidth(width + 18)
        super().setText(text)


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    widget = widgets.Label("test", tool_tip="testus")
    ef = ClickableLabelEventFilter(widget)
    widget.installEventFilter(ef)
    widget.show()
    app.main_loop()
