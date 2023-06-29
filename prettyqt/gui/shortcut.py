from __future__ import annotations

from collections.abc import Iterable

from prettyqt import constants, core, gui
from prettyqt.utils import datatypes


class Shortcut(core.ObjectMixin, gui.QShortcut):
    def __init__(self, *args, **kwargs):
        match args:
            case (str(), *rest):
                args = (gui.KeySequence(args[0]), *rest)
        super().__init__(*args, **kwargs)

    def __str__(self):
        return self.key().toString()

    def set_context(
        self, context: constants.ShortcutContextStr | constants.ShortcutContext
    ):
        """Set shortcut context.

        Args:
            context: shortcut context
        """
        self.setContext(constants.SHORTCUT_CONTEXT.get_enum_value(context))

    def get_context(self) -> constants.ShortcutContextStr:
        """Return shortcut context.

        Returns:
            shortcut context
        """
        return constants.SHORTCUT_CONTEXT.inverse[self.context()]

    def set_key(
        self,
        key: datatypes.KeyCombinationType,
    ):
        keysequence = gui.KeySequence(key)
        self.setKey(keysequence)

    def set_keys(self, keys: Iterable[datatypes.KeyCombinationType]):
        keysequences = [gui.KeySequence(key) for key in keys]
        self.setKeys(keysequences)

    def get_key(self) -> gui.KeySequence:
        """Return the shortcut's key sequence.

        Returns:
            Key sequence
        """
        return gui.KeySequence(self.key())

    def get_keys(self) -> list[gui.KeySequence]:
        return [gui.KeySequence(i) for i in self]


if __name__ == "__main__":
    app = gui.app()
    shortcut = Shortcut("enter", None)
    print(shortcut.get_properties())
