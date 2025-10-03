from __future__ import annotations

from typing import TYPE_CHECKING

from prettyqt import iconprovider
from prettyqt.qt import QtWidgets


if TYPE_CHECKING:
    from prettyqt.qt import QtGui


mod = QtWidgets.QStyle

MAPPING = {
    mod.StandardPixmap.SP_TitleBarMinButton: "mdi.window-minimize",
    mod.StandardPixmap.SP_TitleBarMenuButton: "mdi.microsoft-windows",
    mod.StandardPixmap.SP_TitleBarMaxButton: "mdi.window-maximize",
    mod.StandardPixmap.SP_TitleBarCloseButton: "mdi.window-close",
    mod.StandardPixmap.SP_TitleBarNormalButton: "mdi.window-restore",
    mod.StandardPixmap.SP_TitleBarShadeButton: "mdi.arrow-up",
    mod.StandardPixmap.SP_TitleBarUnshadeButton: "mdi.arrow-down",
    mod.StandardPixmap.SP_TitleBarContextHelpButton: "mdi.help",
    mod.StandardPixmap.SP_MessageBoxInformation: "mdi.information",
    mod.StandardPixmap.SP_MessageBoxWarning: "mdi.alert",
    mod.StandardPixmap.SP_MessageBoxCritical: "mdi.alert-circle-outline",
    mod.StandardPixmap.SP_MessageBoxQuestion: "mdi.tooltip-question-outline",
    mod.StandardPixmap.SP_DesktopIcon: "mdi.monitor",
    mod.StandardPixmap.SP_TrashIcon: "mdi.trash-can",
    mod.StandardPixmap.SP_ComputerIcon: "mdi.desktop-classic",
    mod.StandardPixmap.SP_DriveFDIcon: "mdi.floppy",
    mod.StandardPixmap.SP_DriveHDIcon: "mdi.harddisk",
    mod.StandardPixmap.SP_DriveCDIcon: "mdi.disc",
    mod.StandardPixmap.SP_DriveDVDIcon: "mdi.disc",
    mod.StandardPixmap.SP_DriveNetIcon: "mdi.network-outline",
    mod.StandardPixmap.SP_DirHomeIcon: "mdi.home-circle",
    mod.StandardPixmap.SP_DirOpenIcon: "mdi.folder-multiple-outline",
    mod.StandardPixmap.SP_DirClosedIcon: "mdi.folder-outline",
    mod.StandardPixmap.SP_DirIcon: "mdi.folder",
    mod.StandardPixmap.SP_DirLinkIcon: "mdi.link-box-outline",
    mod.StandardPixmap.SP_DirLinkOpenIcon: "mdi.link-plus",
    mod.StandardPixmap.SP_FileIcon: "mdi.file-outline",
    mod.StandardPixmap.SP_FileLinkIcon: "mdi.file-link-outline",
    mod.StandardPixmap.SP_FileDialogStart: "mdi.ray-start-arrow",
    mod.StandardPixmap.SP_FileDialogEnd: "mdi.ray-end-arrow",
    mod.StandardPixmap.SP_FileDialogToParent: "mdi.keyboard-return",
    mod.StandardPixmap.SP_FileDialogNewFolder: "mdi.folder-plus-outline",
    mod.StandardPixmap.SP_FileDialogDetailedView: "mdi.details",
    mod.StandardPixmap.SP_FileDialogInfoView: "mdi.information-outline",
    mod.StandardPixmap.SP_FileDialogContentsView: "mdi.content-paste",
    mod.StandardPixmap.SP_FileDialogListView: "mdi.format-list-bulleted",
    mod.StandardPixmap.SP_FileDialogBack: "mdi.arrow-left",
    mod.StandardPixmap.SP_DockWidgetCloseButton: "mdi.close-circle-outline",
    mod.StandardPixmap.SP_ToolBarHorizontalExtensionButton: "mdi.pan-horizontal",
    mod.StandardPixmap.SP_ToolBarVerticalExtensionButton: "mdi.pan-vertical",
    mod.StandardPixmap.SP_DialogOkButton: "mdi.check",
    mod.StandardPixmap.SP_DialogCancelButton: "mdi.cancel",
    mod.StandardPixmap.SP_DialogHelpButton: "mdi.help",
    mod.StandardPixmap.SP_DialogOpenButton: "mdi.play-protected-content",
    mod.StandardPixmap.SP_DialogSaveButton: "mdi.content-save-outline",
    mod.StandardPixmap.SP_DialogCloseButton: "mdi.window-close",
    mod.StandardPixmap.SP_DialogApplyButton: "mdi.thumb-up-outline",
    mod.StandardPixmap.SP_DialogResetButton: "mdi.lock-reset",
    mod.StandardPixmap.SP_DialogDiscardButton: "mdi.file-undo",
    mod.StandardPixmap.SP_DialogYesButton: "mdi.check",
    mod.StandardPixmap.SP_DialogNoButton: "mdi.cancel",
    mod.StandardPixmap.SP_ArrowUp: "mdi.arrow-up",
    mod.StandardPixmap.SP_ArrowDown: "mdi.arrow-down",
    mod.StandardPixmap.SP_ArrowLeft: "mdi.arrow-left",
    mod.StandardPixmap.SP_ArrowRight: "mdi.arrow-right",
    mod.StandardPixmap.SP_ArrowBack: "mdi.arrow-left",
    mod.StandardPixmap.SP_ArrowForward: "mdi.arrow-right",
    mod.StandardPixmap.SP_CommandLink: "mdi.apple-keyboard-command",
    mod.StandardPixmap.SP_VistaShield: "mdi.shield",
    mod.StandardPixmap.SP_BrowserReload: "mdi.reload",
    mod.StandardPixmap.SP_BrowserStop: "mdi.stop-circle-outline",
    mod.StandardPixmap.SP_MediaPlay: "mdi.play-circle-outline",
    mod.StandardPixmap.SP_MediaStop: "mdi.stop-circle-outline",
    mod.StandardPixmap.SP_MediaPause: "mdi.pause-circle-outline",
    mod.StandardPixmap.SP_MediaSkipForward: "mdi.skip-next-circle-outline",
    mod.StandardPixmap.SP_MediaSkipBackward: "mdi.skip-previous-circle-outline",
    mod.StandardPixmap.SP_MediaSeekForward: "mdi.step-forward",
    mod.StandardPixmap.SP_MediaSeekBackward: "mdi.step-backward",
    mod.StandardPixmap.SP_MediaVolume: "mdi.volume-high",
    mod.StandardPixmap.SP_MediaVolumeMuted: "mdi.volume-mute",
    mod.StandardPixmap.SP_LineEditClearButton: "mdi.close-circle-outline",
    mod.StandardPixmap.SP_DialogYesToAllButton: "mdi.check",
    mod.StandardPixmap.SP_DialogNoToAllButton: "mdi.cancel",
    mod.StandardPixmap.SP_DialogSaveAllButton: "mdi.content-save-outline",
    mod.StandardPixmap.SP_DialogAbortButton: "mdi.exit-to-app",
    mod.StandardPixmap.SP_DialogRetryButton: "mdi.repeat",
    mod.StandardPixmap.SP_DialogIgnoreButton: "mdi.minus-circle-outline",
    mod.StandardPixmap.SP_RestoreDefaultsButton: "mdi.history",
    mod.StandardPixmap.SP_TabCloseButton: "mdi.cancel",
    mod.StandardPixmap.SP_CustomBase: "mdi.firebase",
}


class MaterialIconStyle(QtWidgets.QProxyStyle):
    def standardIcon(
        self,
        standard_icon: QtWidgets.QStyle.StandardPixmap,
        option: QtWidgets.QStyleOption | None = None,
        widget: QtWidgets.QWidget | None = None,
    ) -> QtGui.QIcon:
        """Implement QProxyStyle.standardIcon."""
        icon_name = MAPPING.get(standard_icon)
        if icon_name is None:
            return super().standardIcon(standard_icon, option, widget)

        return iconprovider.get_icon(icon_name, as_qicon=True)


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    style = MaterialIconStyle()
    app.setStyle(style)
    app.exec()
