from __future__ import annotations

import enum

from prettyqt import core, gui, widgets


class EnumFlagWidget(widgets.ToolButton):
    value_changed = core.Signal(enum.Flag)

    def __init__(self, *args, object_name: str = "enum_flag_widget", **kwargs):
        self._enum_class = None
        self._action_map = {}
        self.button_menu = widgets.Menu(triggered=self._on_menu_click)
        super().__init__(*args, object_name=object_name, **kwargs)
        self.setMenu(self.button_menu)
        self.set_popup_mode("instant")

    def _on_menu_click(self):
        values = []
        value = self.get_value()
        for i in self._enum_class.__members__.values():
            if i.value == 0:
                continue
            # self._action_map[i].setChecked(value & i == i)
            if value & i == i:
                values.append(i)
        text = " | ".join(i.name for i in values) if values else self._enum_class(0).name
        self.set_text(text)
        self.value_changed.emit(value)

    def clear(self):
        self._action_map = {}
        self.button_menu.clear()

    def _set_enum_class(self, enum: enum.EnumMeta | None):
        """Set enum class from which members value should be selected."""
        if enum == self._enum_class:
            return None
        self._enum_class = enum
        self.clear()
        for i in self._enum_class.__members__.values():
            if i.value == 0:
                continue
            action = gui.Action(text=i.name.replace("_", " "), checkable=True)
            action.setData(i)
            self._action_map[i] = action
            self.button_menu.add(action)

    def get_enum_class(self) -> enum.EnumMeta | None:
        """Return current Enum class."""
        return self._enum_class

    def get_value(self) -> enum.Flag:
        """Current value as Enum member."""
        if self._enum_class is None:
            return None
        flag = self._enum_class(0)
        for k, v in self._action_map.items():
            if v.isChecked():
                flag |= k
        return flag

    def set_value(self, value: enum.Flag) -> None:
        """Set value with Enum."""
        if not isinstance(value, enum.Flag):
            value = self._enum_class(value)
        self._set_enum_class(value.__class__)
        if not isinstance(value, self._enum_class):
            raise TypeError(
                "setValue(self, Enum): argument 1 has unexpected type "
                f"{type(value).__name__!r}"
            )
        # this filter shouldnt be needed, see https://bugreports.qt.io/browse/PYSIDE-2369
        values = []
        for i in self._enum_class.__members__.values():
            if i.value == 0:
                continue
            if value & i == i:
                self._action_map[i].setChecked(True)
                values.append(i)
        text = " | ".join(i.name for i in values) if values else self._enum_class(0).name
        self.set_text(text)

    value = core.Property(enum.Flag, get_value, set_value, user=True)
    # enumClass = core.Property(type(enum.Flag), get_enum_class, set_enum_class)


if __name__ == "__main__":
    from prettyqt import constants

    app = widgets.app()
    flag = constants.FocusPolicy
    w = EnumFlagWidget()
    # w.set_value(flag.NoFocus)
    testwidget = widgets.TableView()
    print(type(testwidget.focusPolicy()))
    # print(type(testwidget.focusPolicy()))
    # print(repr(testwidget.focusPolicy()))
    w.set_value(testwidget.focusPolicy())
    w.value_changed.connect(print)
    w.show()
    app.exec()
