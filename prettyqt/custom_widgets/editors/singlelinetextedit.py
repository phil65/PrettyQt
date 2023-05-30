from __future__ import annotations

from prettyqt import widgets


class SingleLineTextEdit(widgets.PlainTextEdit):
    def __init__(self, *args, object_name: str = "singleline_textedit", **kwargs):
        super().__init__(*args, object_name=object_name, **kwargs)
        self.textChanged.connect(self._on_text_changed)
        font_metrics = self.get_font_metrics()
        row_height = font_metrics.lineSpacing()
        self.setFixedHeight(int(row_height * 1.5))
        self.set_size_policy(vertical="fixed")
        self.set_line_wrap_mode("none")
        self.set_scrollbar_policy("always_off")

    def _on_text_changed(self):
        text = self.text()
        with self.selecter.current_cursor() as c:
            pos = c.position()
            num_linebreaks = text.count("\n")
            with self.block_signals():
                self.set_text(text.replace("\n", ""))
            c.setPosition(pos - num_linebreaks)


if __name__ == "__main__":
    app = widgets.app()
    widget = SingleLineTextEdit()
    widget.show()
    app.main_loop()
