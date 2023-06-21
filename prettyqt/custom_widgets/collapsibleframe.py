from __future__ import annotations

from prettyqt import core, widgets


class CollapsibleFrame(widgets.Frame):
    expanded = core.Signal()
    collapsed = core.Signal()

    def __init__(self, text: str = "", **kwargs):
        super().__init__(frame_shape="styled_panel", frame_shadow="plain", **kwargs)
        _layout = self.set_layout("vertical", margin=0, spacing=0)
        # button
        self._button = widgets.ToolButton(
            self,
            clicked=self.on_button_click,
            arrow_type="right",
            auto_raise=False,
            text=text,
            visible=True,
        )
        self._button.set_style("text_beside_icon")
        self.set_size_policy("minimum_expanding", "fixed")
        _layout.addWidget(self._button, 0)
        # group box
        self._panel = widgets.Widget(self, visible=False)
        _layout.addWidget(self._panel)
        self._panel_layout = self._panel.set_layout("vertical", margin=1, spacing=2)
        self._is_collapsed = True

    def set_title(self, title: str):
        self._button.set_text(title)

    def add_widget(self, widget: widgets.Widget):
        self._panel_layout.addWidget(widget)

    def remove_widget(self, widget: widgets.Widget):
        self._panel_layout.removeWidget(widget)

    def is_expanded(self) -> bool:
        return not self._is_collapsed

    def expand(self):
        self._button.set_arrow_type("down")
        self._panel.setVisible(True)
        self._is_collapsed = False
        self.set_size_policy("minimum_expanding", "minimum_expanding")

    def collapse(self):
        self._panel.setVisible(False)
        self._button.set_arrow_type("right")
        self._is_collapsed = True
        self.set_size_policy("preferred", "preferred")

    @core.Slot()
    def on_button_click(self):
        if self._is_collapsed:
            self.expand()
            self.expanded.emit()
        else:
            self.collapse()
            self.collapsed.emit()


# class CollapsibleWidget(widgets.Frame):
#     """A collapsible widget to hide and unhide child widgets.

#     A signal is emitted when the widget is expanded (True) or collapsed (False).

#     Based on https://stackoverflow.com/a/68141638
#     """

#     toggled = core.Signal(bool)

#     def __init__(
#         self,
#         title: str = "",
#         parent: widgets.QWidget | None = None,
#         expanded_icon: gui.QIcon | str | None = "▼",
#         collapsed_icon: gui.QIcon | str | None = "▲",
#     ):
#         super().__init__(parent)
#         self._locked = False
#         self._is_animating = False
#         self._text = title

#         self._toggle_btn = widgets.PushButton(title, checkable=True,
#           toggled=self._toggle)
#         self.set_collapsed_icon(collapsed_icon)
#         self.set_expanded_icon(expanded_icon)
#         self._toggle_btn.setStyleSheet("text-align: left; border: none; outline: none;")
#         # frame layout
#         layout = self.set_layout("vertical")
#         layout.setAlignment(constants.AlignmentFlag.AlignTop)
#         layout.addWidget(self._toggle_btn)

#         # Create animators
#         self._animation = core.PropertyAnimation(
#             self,
#             finished=self._on_animation_done,
#             easing_curve="in_out_cubic",
#             duration=300,
#             start_value=0,
#         )
#         self._animation.set_property_name("maximumHeight")

#         # default content widget
#         _content = widgets.Widget()
#         _content.setLayout(widgets.VBoxLayout())
#         _content.setMaximumHeight(0)
#         _content.layout().setContentsMargins(core.QMargins(5, 0, 0, 0))
#         self.setContent(_content)

#     def setText(self, text: str):
#         """Set the text of the toggle button."""
#         current = self._toggle_btn.text()
#         self._toggle_btn.setText(current + text)

#     def text(self) -> str:
#         """Return the text of the toggle button."""
#         return self._toggle_btn.text()

#     def setContent(self, content: widgets.QWidget):
#         """Replace central widget (the widget that gets expanded/collapsed)."""
#         self._content = content
#         self.layout().addWidget(self._content)
#         self._animation.setTargetObject(content)

#     def content(self) -> widgets.QWidget:
#         """Return the current content widget."""
#         return self._content

#     def _convert_string_to_icon(self, symbol: str) -> gui.QIcon:
#         """Create a gui.QIcon from a string."""
#         size = self._toggle_btn.font().pointSize()
#         pixmap = gui.Pixmap(size, size)
#         pixmap.fill(constants.GlobalColor.transparent)
#         painter = gui.Painter(pixmap)
#         color = self._toggle_btn.palette().color(gui.QPalette.ColorRole.WindowText)
#         painter.setPen(color)
#         rect = core.QRect(0, 0, size, size)
#         painter.drawText(rect, constants.AlignmentFlag.AlignCenter, symbol)
#         painter.end()
#         return gui.QIcon(pixmap)

#     def get_expanded_icon(self) -> gui.QIcon:
#         """Returns the icon used when the widget is expanded."""
#         return self._expanded_icon

#     def set_expanded_icon(self, icon: gui.QIcon | str | None = None):
#         """Set the icon on the toggle button when the widget is expanded."""
#         match icon:
#             case gui.QIcon():
#                 self._expanded_icon = icon
#             case str():
#                 self._expanded_icon = self._convert_string_to_icon(icon)
#             case _:
#                 raise TypeError(icon)

#         if self.isExpanded():
#             self._toggle_btn.setIcon(self._expanded_icon)

#     def get_collapsed_icon(self) -> gui.QIcon:
#         """Returns the icon used when the widget is collapsed."""
#         return self._collapsed_icon

#     def set_collapsed_icon(self, icon: gui.QIcon | str | None = None):
#         """Set the icon on the toggle button when the widget is collapsed."""
#         match icon:
#             case gui.QIcon():
#                 self._collapsed_icon = icon
#             case str():
#                 self._collapsed_icon = self._convert_string_to_icon(icon)
#             case _:
#                 raise TypeError(icon)

#         if not self.isExpanded():
#             self._toggle_btn.setIcon(self._collapsed_icon)

#     def setDuration(self, msecs: int):
#         """Set duration of the collapse/expand animation."""
#         self._animation.setDuration(msecs)

#     def set_easing_curve(self, easing: core.QEasingCurve):
#         """Set the easing curve for the collapse/expand animation."""
#         self._animation.setEasingCurve(easing)

#     def addWidget(self, widget: widgets.QWidget):
#         """Add a widget to the central content widget's layout."""
#         widget.installEventFilter(self)
#         self._content.layout().addWidget(widget)

#     def removeWidget(self, widget: widgets.QWidget):
#         """Remove widget from the central content widget's layout."""
#         self._content.layout().removeWidget(widget)
#         widget.removeEventFilter(self)

#     def expand(self, animate: bool = True):
#         """Expand (show) the collapsible section."""
#         self._expand_collapse(core.QPropertyAnimation.Direction.Forward, animate)

#     def collapse(self, animate: bool = True):
#         """Collapse (hide) the collapsible section."""
#         self._expand_collapse(core.QPropertyAnimation.Direction.Backward, animate)

#     def isExpanded(self) -> bool:
#         """Return whether the collapsible section is visible."""
#         return self._toggle_btn.isChecked()

#     def setLocked(self, locked: bool = True):
#         """Set whether collapse/expand is disabled."""
#         self._locked = locked
#         self._toggle_btn.setCheckable(not locked)

#     def locked(self) -> bool:
#         """Return True if collapse/expand is disabled."""
#         return self._locked

#     def _expand_collapse(
#         self,
#         direction: core.QPropertyAnimation.Direction,
#         animate: bool = True,
#         emit: bool = True,
#     ):
#         """Set values for the widget based on whether it is expanding or collapsing.

#         An emit flag is included so that the toggle signal is only called once (it
#         was being emitted a few times via eventFilter when the widget was expanding
#         previously).
#         """
#         if self._locked:
#             return

#         forward = direction == core.QPropertyAnimation.Direction.Forward
#         icon = self._expanded_icon if forward else self._collapsed_icon
#         self._toggle_btn.setIcon(icon)
#         self._toggle_btn.setChecked(forward)

#         _content_height = self._content.sizeHint().height() + 10
#         if animate:
#             self._animation.setDirection(direction)
#             self._animation.setEndValue(_content_height)
#             self._is_animating = True
#             self._animation.start()
#         else:
#             self._content.setMaximumHeight(_content_height if forward else 0)
#         if emit:
#             self.toggled.emit(direction == core.QPropertyAnimation.Direction.Forward)

#     def _toggle(self):
#         self.expand() if self.isExpanded() else self.collapse()

#     def eventFilter(self, source: core.QObject, event: core.QEvent) -> bool:
#         """If a child widget resizes, we need to update our expanded height."""
#         if (
#             event.type() == core.QEvent.Type.Resize
#             and self.isExpanded()
#             and not self._is_animating
#         ):
#             self._expand_collapse(
#                 core.QPropertyAnimation.Direction.Forward, animate=False, emit=False
#             )
#         return False

#     def _on_animation_done(self):
#         self._is_animating = False


if __name__ == "__main__":
    app = widgets.app()
    widget = CollapsibleFrame()
    widget.add_widget(widgets.Label("test"))
    widget.show()
    app.exec()
