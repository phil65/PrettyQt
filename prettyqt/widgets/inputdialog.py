from __future__ import annotations

from typing import Literal

from prettyqt import widgets
from prettyqt.utils import bidict, datatypes


mod = widgets.QInputDialog

InputDialogOptionStr = Literal[
    "no_buttons", "use_listview_for_combobox_items", "use_plaintextedit_for_text_input"
]

INPUT_DIALOG_OPTION: bidict[InputDialogOptionStr, mod.InputDialogOption] = bidict(
    no_buttons=mod.InputDialogOption.NoButtons,
    use_listview_for_combobox_items=mod.InputDialogOption.UseListViewForComboBoxItems,
    use_plaintextedit_for_text_input=mod.InputDialogOption.UsePlainTextEditForTextInput,
)

InputModeStr = Literal["text", "int", "double"]

INPUT_MODE: bidict[InputModeStr, mod.InputMode] = bidict(
    text=mod.InputMode.TextInput,
    int=mod.InputMode.IntInput,
    double=mod.InputMode.DoubleInput,
)


class InputDialog(widgets.DialogMixin, widgets.QInputDialog):
    """Simple convenience dialog to get a single value from the user."""

    def _get_map(self):
        maps = super()._get_map()
        maps |= {
            "textEchoMode": widgets.lineedit.ECHO_MODE,
            "inputMode": INPUT_MODE,
            "options": INPUT_DIALOG_OPTION,
        }
        return maps

    @classmethod
    def get_int(
        cls,
        title: str = "",
        label: str = "",
        icon: datatypes.IconType = None,
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
        icon: datatypes.IconType = None,
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
        icon: datatypes.IconType = None,
        value: str = "",
        echo_mode: widgets.lineedit.EchoModeStr | widgets.QLineEdit.EchoMode = "normal",
    ) -> str | None:
        par = widgets.Dialog()
        par.set_icon(icon)
        v = cls.getText(
            par, title, label, widgets.lineedit.ECHO_MODE.get_enum_value(echo_mode), value
        )
        return v[0] if v[1] else None

    @classmethod
    def get_item(
        cls,
        items: list[str],
        title: str = "",
        label: str = "",
        icon: datatypes.IconType = None,
        editable: bool = False,
    ) -> str | None:
        par = widgets.Dialog()
        par.set_icon(icon)
        v = cls.getItem(par, title, label, items, editable=editable, current=0)
        return v[0] if v[1] else None

    def set_text_echo_mode(
        self, mode: widgets.lineedit.EchoModeStr | widgets.QLineEdit.EchoMode
    ):
        """Set text echo mode.

        Args:
            mode: echo mode to use
        """
        self.setTextEchoMode(widgets.lineedit.ECHO_MODE.get_enum_value(mode))

    def get_text_echo_mode(self) -> widgets.lineedit.EchoModeStr:
        """Return text echo mode.

        Returns:
            echo mode
        """
        return widgets.lineedit.ECHO_MODE.inverse[self.textEchoMode()]

    def set_input_mode(self, mode: InputModeStr | mod.InputMode):
        """Set input mode.

        Args:
            mode: input mode to use
        """
        self.setInputMode(INPUT_MODE.get_enum_value(mode))

    def get_input_mode(self) -> InputModeStr:
        """Return input mode.

        Returns:
            input mode
        """
        return INPUT_MODE.inverse[self.inputMode()]


if __name__ == "__main__":
    app = widgets.app()
    result = InputDialog.get_int("a", "b", icon="mdi.timer")
    app.exec()
