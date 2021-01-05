from __future__ import annotations

from typing import List, Literal, Optional

from prettyqt import widgets
from prettyqt.qt import QtWidgets
from prettyqt.utils import InvalidParamError, bidict, types


INPUT_DIALOG_OPTION = bidict(
    no_buttons=QtWidgets.QInputDialog.NoButtons,
    use_listview_for_combobox_items=QtWidgets.QInputDialog.UseListViewForComboBoxItems,
    use_plaintextedit_for_text_input=QtWidgets.QInputDialog.UsePlainTextEditForTextInput,
)

InputDialogOptionStr = Literal[
    "no_buttons", "use_listview_for_combobox_items", "use_plaintextedit_for_text_input"
]

INPUT_MODE = bidict(
    text=QtWidgets.QInputDialog.TextInput,
    int=QtWidgets.QInputDialog.IntInput,
    double=QtWidgets.QInputDialog.DoubleInput,
)

InputModeStr = Literal["text", "int", "double"]

QtWidgets.QInputDialog.__bases__ = (widgets.BaseDialog,)


class InputDialog(QtWidgets.QInputDialog):
    @classmethod
    def get_int(
        cls,
        title: str = "",
        label: str = "",
        icon: types.IconType = None,
    ) -> Optional[int]:
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
    ) -> Optional[float]:
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
    ) -> Optional[str]:
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
        items: List[str],
        title: str = "",
        label: str = "",
        icon: types.IconType = None,
        editable: bool = False,
    ) -> Optional[str]:
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
