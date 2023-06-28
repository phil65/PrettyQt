from __future__ import annotations

from prettyqt import core, gui, widgets
from prettyqt.utils import get_repr


class PushButtonMixin(widgets.AbstractButtonMixin):
    value_changed = core.Signal(bool)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.toggled.connect(self.value_changed)
        self._action = None

    def __repr__(self):
        return get_repr(self, self.text())

    def set_action(self, action: gui.QAction):
        if self._action == action:
            return
        if self._action:
            self._action.changed.disconnect(self._update_button_for_action)
            self.clicked.disconnect(self._action.trigger)
        self._action = action
        self.clicked.connect(action.trigger)
        action.changed.connect(self._update_button_for_action)
        self._update_button_for_action()

    @core.Slot()
    def _update_button_for_action(self):
        self.setText(self._action.text())
        self.setIcon(self._action.icon())
        self.setStatusTip(self._action.statusTip())
        self.setToolTip(self._action.toolTip())
        self.setEnabled(self._action.isEnabled())
        self.setCheckable(self._action.isCheckable())
        self.setChecked(self._action.isChecked())


class PushButton(PushButtonMixin, widgets.QPushButton):
    pass


if __name__ == "__main__":
    app = widgets.app()
    widget = PushButton("This is a test")
    widget.show()
    app.exec()
