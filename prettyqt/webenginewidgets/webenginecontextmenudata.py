from typing import List

from qtpy import PYQT5, PYSIDE2


if PYQT5:
    from PyQt5 import QtWebEngineWidgets  # type: ignore
elif PYSIDE2:
    from PySide2 import QtWebEngineWidgets

from prettyqt import core
from prettyqt.utils import bidict


mod = QtWebEngineWidgets.QWebEngineContextMenuData

EDIT_FLAGS = bidict(
    undo=mod.CanUndo,
    redo=mod.CanRedo,
    cut=mod.CanCut,
    copy=mod.CanCopy,
    paste=mod.CanPaste,
    delete=mod.CanDelete,
    select_all=mod.CanSelectAll,
    translate=mod.CanTranslate,
    edit_richly=mod.CanEditRichly,
)


MEDIA_FLAGS = bidict(
    in_error=mod.MediaInError,
    paused=mod.MediaPaused,
    muted=mod.MediaMuted,
    loop=mod.MediaLoop,
    can_save=mod.MediaCanSave,
    has_audio=mod.MediaHasAudio,
    can_toggle_controls=mod.MediaCanToggleControls,
    controls=mod.MediaControls,
    can_print=mod.MediaCanPrint,
    can_rotate=mod.MediaCanRotate,
)

MEDIA_TYPES = bidict(
    none=mod.MediaTypeNone,
    image=mod.MediaTypeImage,
    video=mod.MediaTypeVideo,
    audio=mod.MediaTypeAudio,
    canvas=mod.MediaTypeCanvas,
    file=mod.MediaTypeFile,
    plugin=mod.MediaTypePlugin,
)


class WebEngineContextMenuData(QtWebEngineWidgets.QWebEngineContextMenuData):
    def get_media_url(self) -> core.Url:
        return core.Url(self.mediaUrl())

    def get_link_url(self) -> core.Url:
        return core.Url(self.linkUrl())

    def get_media_type(self) -> str:
        return MEDIA_TYPES.inverse[self.mediaType()]

    def get_media_flags(self) -> List[str]:
        return [k for k, v in MEDIA_FLAGS.items() if v & self.mediaFlags()]

    def get_edit_flags(self) -> List[str]:
        return [k for k, v in EDIT_FLAGS.items() if v & self.editFlags()]

    def can_undo(self) -> bool:
        return mod.CanUndo & self.editFlags()

    def can_redo(self) -> bool:
        return mod.CanRedo & self.editFlags()

    def can_cut(self) -> bool:
        return mod.CanCut & self.editFlags()

    def can_copy(self) -> bool:
        return mod.CanCopy & self.editFlags()

    def can_paste(self) -> bool:
        return mod.CanPaste & self.editFlags()

    def can_delete(self) -> bool:
        return mod.CanDelete & self.editFlags()

    def can_select_all(self) -> bool:
        return mod.CanSelectAll & self.editFlags()

    def can_translate(self) -> bool:
        return mod.CanTranslate & self.editFlags()

    def can_edit_richly(self) -> bool:
        return mod.CanEditRichly & self.editFlags()


if __name__ == "__main__":
    from prettyqt import webenginewidgets, widgets

    app = widgets.app()
    page = webenginewidgets.WebEnginePage()
    context_menu_data = page.get_context_menu_data()
    app.main_loop()
