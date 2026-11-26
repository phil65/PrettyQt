from typing import TYPE_CHECKING

from prettyqt import core, qthelp
from prettyqt.utils import datatypes


if TYPE_CHECKING:
    from prettyqt.qt import QtHelp

    _HelpEngineCoreBase = QtHelp.QHelpEngineCore
else:
    _HelpEngineCoreBase = object


class HelpEngineCoreMixin(core.ObjectMixin, _HelpEngineCoreBase):
    """The core functionality of the help system."""

    def get_file_data(self, url: core.QUrl) -> bytes:
        return bytes(self.fileData(url).data())

    def get_files(
        self,
        namespace_name: str,
        filter_name: str,
        extension_filter: str | None = None,
    ) -> list[core.Url]:
        if extension_filter is None:
            extension_filter = ""
        return [
            core.Url(i) for i in self.files(namespace_name, filter_name, extension_filter)
        ]

    def find_file(self, url: datatypes.UrlType) -> core.Url:
        return core.Url(self.findFile(datatypes.to_url(url)))

    def get_filter_engine(self) -> qthelp.HelpFilterEngine:
        return qthelp.HelpFilterEngine(self.filterEngine())


class HelpEngineCore(HelpEngineCoreMixin, qthelp.QHelpEngineCore):
    pass


if __name__ == "__main__":
    engine = HelpEngineCore("")
    engine.get_files("a", "b")
