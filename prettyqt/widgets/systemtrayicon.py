from qtpy import QtWidgets

from prettyqt import gui
from prettyqt.utils import bidict


ACTIVATION_REASONS = bidict(
    unknown=QtWidgets.QSystemTrayIcon.Unknown,
    context=QtWidgets.QSystemTrayIcon.Context,
    double_click=QtWidgets.QSystemTrayIcon.DoubleClick,
    trigger=QtWidgets.QSystemTrayIcon.Trigger,
    middle_click=QtWidgets.QSystemTrayIcon.MiddleClick,
)

MESSAGE_ICONS = bidict(
    none=QtWidgets.QSystemTrayIcon.NoIcon,
    information=QtWidgets.QSystemTrayIcon.Information,
    warning=QtWidgets.QSystemTrayIcon.Warning,
    critical=QtWidgets.QSystemTrayIcon.Critical,
)


class SystemTrayIcon(QtWidgets.QSystemTrayIcon):
    def set_icon(self, icon: gui.icon.IconType):
        """Set the system tray icon.

        Args:
            icon: icon to use
        """
        icon = gui.icon.get_icon(icon)
        self.setIcon(icon)

    def show_message(
        self,
        title: str,
        message: str = "",
        icon: gui.icon.IconType = None,
        timeout: int = 10,
    ):
        if icon is None:
            icon = "none"
        if icon in MESSAGE_ICONS:
            icon = MESSAGE_ICONS[icon]
        else:
            icon = gui.icon.get_icon(icon)
        self.showMessage(title, message, icon, timeout * 1000)


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    icon = SystemTrayIcon()
    icon.set_icon("mdi.folder")
    print(icon.isSystemTrayAvailable())
    icon.show_message("a", "b", "information")
    app.main_loop()
