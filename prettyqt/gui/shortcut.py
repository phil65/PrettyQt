from __future__ import annotations

from prettyqt import constants, core, gui
from prettyqt.qt import QtGui
from prettyqt.utils import InvalidParamError


class Shortcut(core.ObjectMixin, QtGui.QShortcut):
    def __str__(self):
        return self.key().toString()

    def serialize_field(self):
        return dict(
            auto_repeat=self.autoRepeat(),
            context=self.get_context(),
            enabled=self.isEnabled(),
            key=self.get_key(),
            whats_this=self.whatsThis(),
        )

    def set_context(self, context: constants.ContextStr):
        """Set shortcut context.

        Args:
            context: shortcut context

        Raises:
            InvalidParamError: shortcut context does not exist
        """
        if context not in constants.CONTEXT:
            raise InvalidParamError(context, constants.CONTEXT)
        self.setContext(constants.CONTEXT[context])

    def get_context(self) -> constants.ContextStr:
        """Return shortcut context.

        Returns:
            shortcut context
        """
        return constants.CONTEXT.inverse[self.context()]

    def get_key(self) -> gui.KeySequence:
        """Return the shortcut's key sequence.

        Returns:
            Key sequence
        """
        return gui.KeySequence(
            self.key().toString(), gui.KeySequence.SequenceFormat.PortableText
        )

    def get_keys(self) -> list[gui.KeySequence]:
        return [gui.KeySequence(i) for i in self.keys()]
