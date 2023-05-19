from __future__ import annotations

import logging

from prettyqt import constants, core, widgets
from prettyqt.qt import QtCore


logger = logging.getLogger(__name__)


class DebugMode(core.Object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.list = widgets.ListWidget()
        self.list.setMouseTracking(True)
        self.list.entered.connect(self._on_entered)
        self.list.itemClicked.connect(self._on_clicked)
        self.frame = widgets.Frame()
        self.frame.set_frame_shape("box")
        self.frame.set_frame_shadow("plain")
        # self.frame.setGeometry(0, 0, 1920, 1080)
        self.frame.setObjectName("testframe")
        self.frame.setStyleSheet("#testframe {border: 5px solid green;}")
        self.frame.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.Tool
            | QtCore.Qt.WindowType.WindowTransparentForInput
            | QtCore.Qt.WindowType.WindowDoesNotAcceptFocus
            | QtCore.Qt.WindowType.WindowStaysOnTopHint
        )
        # self.frame.setWindowOpacity(0.5)
        # self.mask = widgets.Widget()
        # self.mask.set_background_color("green")

    def eventFilter(self, source: QtCore.QObject, event: QtCore.QEvent) -> bool:
        match event.type():
            case core.Event.Type.MouseButtonPress:
                mods = widgets.Application.query_keyboard_modifiers()
                if "ctrl" in mods:
                    pos = source.mapToGlobal(event.pos())
                    candidates = widgets.Application.widgets_at(pos)
                    self.list.clear()
                    for candidate in candidates:
                        self.list.add_item(f"{candidate!r}", data={"user": candidate})
                    self.list.show()
                    return True
                elif "alt" in mods:
                    from prettyqt import ipython

                    console = ipython.InProcessIPythonWidget(self)
                    console.show()
                    pos = source.mapToGlobal(event.pos())
                    widgets.Application.sleep(1)
                    console.push_vars(
                        dict(
                            widgets=widgets.Application.widgets_at(pos), app=widgets.app()
                        )
                    )
                    console.execute("print(widgets)")
        return False

    def _on_clicked(self, item):
        from prettyqt.custom_widgets import widgeteditor

        logger.debug(f"clicked on {item}")
        widget = item.get_data("user")
        self.editor = widgeteditor.WidgetEditor(widget)
        self.list.hide()
        self.editor.show()

    def _on_entered(self, index):
        widget = index.data(constants.USER_ROLE)
        # logger.info(widget)
        for item in self.list:
            candidate = item.get_data("user")
            if candidate != widget:
                pass
                # effect = widgets.GraphicsOpacityEffect(candidate, opacity=0.5)
            else:
                # effect = widgets.GraphicsOpacityEffect(candidate, opacity=0.7)
                # self.mask.setParent(widget)
                # self.mask.setGeometry(widget.geometry())
                # self.mask.show()
                # print("hfd")
                # rect = widget.contentsRect()
                # top_left = rect.topLeft()
                # bottom_right = rect.bottomRight()
                # top_left = widget.mapToGlobal(top_left)
                # bottom_right = widget.mapToGlobal(bottom_right)

                # rect = core.Rect(top_left, bottom_right)
                # whole_frame_region = gui.Region(rect)
                # inner_region = gui.Region(rect.marginsRemoved(core.Margins(5, 5, 5, 5)))
                # inner_frame_region = whole_frame_region.subtracted(inner_region)
                # self.frame.setMask(inner_frame_region)
                self.frame.resize(widget.size())
                self.frame.setParent(widget)
                self.frame.show()

        # with widget.edit_palette() as palette:
        #     palette.setColor(
        #         gui.Palette.ColorRole.Base,
        #         widget.palette().color(gui.Palette.ColorRole.Highlight),
        #     )


if __name__ == "__main__":
    app = widgets.app()
    container = widgets.Widget()
    container.set_layout("horizontal")
    w = widgets.PlainTextEdit(parent=container)
    w2 = widgets.PlainTextEdit(parent=container)
    container.box.add(w)
    container.box.add(w2)
    container.show()
    with app.debug_mode():
        app.sleep(1)
        app.main_loop()
    print(w.get_properties())
