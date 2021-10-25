from __future__ import annotations

from prettyqt import constants, core, gui
from prettyqt.qt import QtWidgets
from prettyqt.utils import InvalidParamError


QtWidgets.QShortcut.__bases__ = (core.Object,)


class Shortcut(QtWidgets.QShortcut):
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
