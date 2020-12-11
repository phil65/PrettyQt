from typing import Literal

from qtpy import QtWidgets, QtCore

from prettyqt import core, gui
from prettyqt.utils import bidict, InvalidParamError

CONTEXT = bidict(
    widget=QtCore.Qt.WidgetShortcut,
    widget_with_children=QtCore.Qt.WidgetWithChildrenShortcut,
    window=QtCore.Qt.WindowShortcut,
    application=QtCore.Qt.ApplicationShortcut,
)

ContextStr = Literal["widget", "widget_with_children", "window", "application"]


QtWidgets.QShortcut.__bases__ = (core.Object,)


class Shortcut(QtWidgets.QShortcut):
    def __str__(self):
        return str(self.get_key())

    def __int__(self):
        return self.id()

    def serialize_field(self):
        return dict(
            auto_repeat=self.autoRepeat(),
            context=self.get_context(),
            enabled=self.isEnabled(),
            key=self.get_key(),
            whats_this=self.whatsThis(),
        )

    def set_context(self, context: ContextStr):
        """Set shortcut context.

        Args:
            context: shortcut context

        Raises:
            InvalidParamError: shortcut context does not exist
        """
        if context not in CONTEXT:
            raise InvalidParamError(context, CONTEXT)
        self.setContext(CONTEXT[context])

    def get_context(self) -> ContextStr:
        """Return shortcut context.

        Returns:
            shortcut context
        """
        return CONTEXT.inverse[self.context()]

    def get_key(self) -> gui.KeySequence:
        """Return the shortcut's key sequence.

        Returns:
            Key sequence
        """
        return gui.KeySequence(self.key())
