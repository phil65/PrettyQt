from __future__ import annotations

from typing import Literal

from prettyqt import widgets
from prettyqt.qt import QtWidgets
from prettyqt.utils import InvalidParamError, bidict, types


mod = QtWidgets.QInputDialog

INPUT_DIALOG_OPTION = bidict(
    no_buttons=mod.InputDialogOption.NoButtons,
    use_listview_for_combobox_items=mod.InputDialogOption.UseListViewForComboBoxItems,
    use_plaintextedit_for_text_input=mod.InputDialogOption.UsePlainTextEditForTextInput,
)

InputDialogOptionStr = Literal[
    "no_buttons", "use_listview_for_combobox_items", "use_plaintextedit_for_text_input"
]

INPUT_MODE = bidict(
    text=mod.InputMode.TextInput,
    int=mod.InputMode.IntInput,
    double=mod.InputMode.DoubleInput,
)

InputModeStr = Literal["text", "int", "double"]

QtWidgets.QInputDialog.__bases__ = (widgets.Dialog,)


class InputDialog(QtWidgets.QInputDialog):
    @classmethod
    def get_int(
        cls,
        title: str = "",
        label: str = "",
        icon: types.IconType = None,
    ) -> int | None:
        par = widgets.Dialog()
        par.set_icon(icon)
        v = cls.getInt(par, title, label, value=0)
        return v[0] if v[1] else None

    @classmethod
    def get_float(
        cls,
        title: str = "",
        label: str = "",
        icon: types.IconType = None,
    ) -> float | None:
        par = widgets.Dialog()
        par.set_icon(icon)
        v = cls.getDouble(par, title, label, value=0.0)
        return v[0] if v[1] else None

    @classmethod
    def get_text(
        cls,
        title: str = "",
        label: str = "",
        icon: types.IconType = None,
        default_value: str = "",
        echo_mode: widgets.lineedit.EchoModeStr = "normal",
    ) -> str | None:
        par = widgets.Dialog()
        par.set_icon(icon)
        if echo_mode not in widgets.lineedit.ECHO_MODE:
            raise InvalidParamError(echo_mode, widgets.lineedit.ECHO_MODE)
        v = cls.getText(
            par, title, label, widgets.lineedit.ECHO_MODE[echo_mode], default_value
        )
        return v[0] if v[1] else None

    @classmethod
    def get_item(
        cls,
        items: list[str],
        title: str = "",
        label: str = "",
        icon: types.IconType = None,
        editable: bool = False,
    ) -> str | None:
        par = widgets.Dialog()
        par.set_icon(icon)
        v = cls.getItem(par, title, label, items, editable=editable, current=0)
        return v[0] if v[1] else None

    def set_text_echo_mode(self, mode: widgets.lineedit.EchoModeStr):
        """Set text echo mode.

        Args:
            mode: echo mode to use

        Raises:
            InvalidParamError: invalid echo mode
        """
        if mode not in widgets.lineedit.ECHO_MODE:
            raise InvalidParamError(mode, widgets.lineedit.ECHO_MODE)
        self.setTextEchoMode(widgets.lineedit.ECHO_MODE[mode])

    def get_text_echo_mode(self) -> widgets.lineedit.EchoModeStr:
        """Return text echo mode.

        Returns:
            echo mode
        """
        return widgets.lineedit.ECHO_MODE.inverse[self.textEchoMode()]

    def set_input_mode(self, mode: InputModeStr):
        """Set input mode.

        Args:
            mode: input mode to use

        Raises:
            InvalidParamError: invalid input mode
        """
        if mode not in INPUT_MODE:
            raise InvalidParamError(mode, INPUT_MODE)
        self.setInputMode(INPUT_MODE[mode])

    def get_input_mode(self) -> InputModeStr:
        """Return input mode.

        Returns:
            input mode
        """
        return INPUT_MODE.inverse[self.inputMode()]


if __name__ == "__main__":
    app = widgets.app()
    result = InputDialog.get_int("a", "b", icon="mdi.timer")
    print(result)
    app.main_loop()
