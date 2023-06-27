from __future__ import annotations

import os
from typing import Literal

from prettyqt import core, gui
from prettyqt.utils import bidict, datatypes, get_repr, serializemixin


IconEngineHookStr = Literal["available_sizes", "icon_name", "is_null", "scaled_pixmap"]

ICON_ENGINE_HOOK: bidict[IconEngineHookStr, gui.QIconEngine.IconEngineHook] = bidict(
    # available_sizes=gui.QIconEngine.AvailableSizesHook,
    # icon_name=gui.QIconEngine.IconNameHook,
    is_null=gui.QIconEngine.IconEngineHook.IsNullHook,
    scaled_pixmap=gui.QIconEngine.IconEngineHook.ScaledPixmapHook,
)


class IconEngine(serializemixin.SerializeMixin, gui.QIconEngine):
    def __repr__(self):
        return get_repr(self)

    def __bool__(self):
        return not self.isNull()

    def add_file(
        self,
        path: datatypes.PathType,
        size: datatypes.SizeType,
        mode: gui.icon.ModeStr | gui.QIcon.Mode,
        state: gui.icon.StateStr | gui.QIcon.State,
    ):
        self.addFile(
            os.fspath(path),
            datatypes.to_size(size),
            gui.icon.MODE.get_enum_value(mode),
            gui.icon.STATE.get_enum_value(state),
        )

    def add_pixmap(
        self,
        pixmap: gui.QPixmap,
        mode: gui.icon.ModeStr | gui.QIcon.Mode,
        state: gui.icon.StateStr | gui.QIcon.State,
    ):
        self.addPixmap(
            pixmap,
            gui.icon.MODE.get_enum_value(mode),
            gui.icon.STATE.get_enum_value(state),
        )

    def get_actual_size(
        self,
        size: datatypes.SizeType,
        mode: gui.icon.ModeStr | gui.QIcon.Mode = "normal",
        state: gui.icon.StateStr | gui.QIcon.State = "off",
    ) -> core.Size:
        return core.Size(
            self.actualSize(
                datatypes.to_size(size),
                gui.icon.MODE.get_enum_value(mode),
                gui.icon.STATE.get_enum_value(state),
            )
        )

    def get_available_sizes(
        self,
        mode: gui.icon.ModeStr | gui.QIcon.Mode = "normal",
        state: gui.icon.StateStr | gui.QIcon.State = "off",
    ) -> list[core.Size]:
        return [
            core.Size(i)
            for i in self.availableSizes(
                gui.icon.MODE.get_enum_value(mode), gui.icon.STATE.get_enum_value(state)
            )
        ]

    def get_pixmap(
        self,
        size: datatypes.SizeType,
        mode: gui.icon.ModeStr | gui.QIcon.Mode = "normal",
        state: gui.icon.StateStr | gui.QIcon.State = "off",
        scale: float | None = None,
    ) -> gui.Pixmap:
        if scale is None:
            return gui.Pixmap(
                self.pixmap(
                    datatypes.to_size(size),
                    gui.icon.MODE.get_enum_value(mode),
                    gui.icon.STATE.get_enum_value(state),
                )
            )
        else:
            return gui.Pixmap(
                self.scaledPixmap(
                    datatypes.to_size(size),
                    gui.icon.MODE.get_enum_value(mode),
                    gui.icon.STATE.get_enum_value(state),
                    scale,
                )
            )


if __name__ == "__main__":
    app = gui.app()
    engine = IconEngine()
    print(repr(engine))
