from __future__ import annotations

from typing import Literal

from prettyqt import core
from prettyqt.qt import QtWebEngineCore
from prettyqt.utils import bidict


mod = QtWebEngineCore.QWebEngineContextMenuRequest

EDIT_FLAGS = bidict(
    undo=mod.EditFlag.CanUndo,
    redo=mod.EditFlag.CanRedo,
    cut=mod.EditFlag.CanCut,
    copy=mod.EditFlag.CanCopy,
    paste=mod.EditFlag.CanPaste,
    delete=mod.EditFlag.CanDelete,
    select_all=mod.EditFlag.CanSelectAll,
    translate=mod.EditFlag.CanTranslate,
    edit_richly=mod.EditFlag.CanEditRichly,
)

EditFlagStr = Literal[
    "undo",
    "redo",
    "cut",
    "copy",
    "paste",
    "delete",
    "select_all",
    "translate",
    "edit_richly",
]

MEDIA_FLAGS = bidict(
    in_error=mod.MediaFlag.MediaInError,
    paused=mod.MediaFlag.MediaPaused,
    muted=mod.MediaFlag.MediaMuted,
    loop=mod.MediaFlag.MediaLoop,
    can_save=mod.MediaFlag.MediaCanSave,
    has_audio=mod.MediaFlag.MediaHasAudio,
    can_toggle_controls=mod.MediaFlag.MediaCanToggleControls,
    controls=mod.MediaFlag.MediaControls,
    can_print=mod.MediaFlag.MediaCanPrint,
    can_rotate=mod.MediaFlag.MediaCanRotate,
)

MediaFlagStr = Literal[
    "in_error",
    "paused",
    "muted",
    "loop",
    "can_save",
    "has_audio",
    "can_toggle_controls",
    "controls",
    "can_print",
    "can_rotate",
]

MEDIA_TYPES = bidict(
    none=mod.MediaType.MediaTypeNone,
    image=mod.MediaType.MediaTypeImage,
    video=mod.MediaType.MediaTypeVideo,
    audio=mod.MediaType.MediaTypeAudio,
    canvas=mod.MediaType.MediaTypeCanvas,
    file=mod.MediaType.MediaTypeFile,
    plugin=mod.MediaType.MediaTypePlugin,
)

MediaTypeStr = Literal["none", "image", "video", "audio", "canvas", "file", "plugin"]


class WebEngineContextMenuRequest(QtWebEngineCore.QWebEngineContextMenuRequest):
    def get_media_url(self) -> core.Url:
        return core.Url(self.mediaUrl())

    def get_link_url(self) -> core.Url:
        return core.Url(self.linkUrl())

    def get_media_type(self) -> MediaTypeStr:
        return MEDIA_TYPES.inverse[self.mediaType()]

    def get_media_flags(self) -> list[MediaFlagStr]:
        return [k for k, v in MEDIA_FLAGS.items() if v & self.mediaFlags()]

    def get_edit_flags(self) -> list[MediaFlagStr]:
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
    from prettyqt import webenginecore, widgets

    app = widgets.app()
    page = webenginecore.WebEnginePage()
    context_menu_data = page.get_context_menu_data()
    app.main_loop()
