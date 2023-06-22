from __future__ import annotations

from typing import Literal

from prettyqt import core, gui, iconprovider
from prettyqt.qt import QtWidgets
from prettyqt.utils import bidict, datatypes


ActivationReasonStr = Literal[
    "unknown", "context", "double_click", "trigger", "middle_click"
]

ACTIVATION_REASONS: bidict[
    ActivationReasonStr, QtWidgets.QSystemTrayIcon.ActivationReason
] = bidict(
    unknown=QtWidgets.QSystemTrayIcon.ActivationReason.Unknown,
    context=QtWidgets.QSystemTrayIcon.ActivationReason.Context,
    double_click=QtWidgets.QSystemTrayIcon.ActivationReason.DoubleClick,
    trigger=QtWidgets.QSystemTrayIcon.ActivationReason.Trigger,
    middle_click=QtWidgets.QSystemTrayIcon.ActivationReason.MiddleClick,
)

MessageIconStr = Literal["none", "information", "warning", "critical"]

MESSAGE_ICONS: bidict[MessageIconStr, QtWidgets.QSystemTrayIcon.MessageIcon] = bidict(
    none=QtWidgets.QSystemTrayIcon.MessageIcon.NoIcon,
    information=QtWidgets.QSystemTrayIcon.MessageIcon.Information,
    warning=QtWidgets.QSystemTrayIcon.MessageIcon.Warning,
    critical=QtWidgets.QSystemTrayIcon.MessageIcon.Critical,
)


class SystemTrayIcon(core.ObjectMixin, QtWidgets.QSystemTrayIcon):
    def set_icon(self, icon: datatypes.IconType):
        """Set the system tray icon.

        Args:
            icon: icon to use
        """
        icon = iconprovider.get_icon(icon)
        self.setIcon(icon)

    def show_message(
        self,
        title: str,
        message: str = "",
        icon: datatypes.IconType = None,
        timeout: int = 10,
    ):
        if icon is None:
            ico = gui.Icon()
        if icon in MESSAGE_ICONS:
            ico = MESSAGE_ICONS[icon]
        else:
            ico = iconprovider.get_icon(icon)
        self.showMessage(title, message, ico, timeout * 1000)


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    icon = SystemTrayIcon()
    icon.set_icon("mdi.folder")
    icon.show_message("a", "b", "information")
    app.exec()
