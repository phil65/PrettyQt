from __future__ import annotations

from prettyqt import core, qthelp
from prettyqt.utils import datatypes


class HelpEngineCoreMixin(core.ObjectMixin):
    """The core functionality of the help system."""

    def get_file_data(self, url: core.QUrl) -> bytes:
        return self.fileData(url).data()

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
        if not isinstance(url, core.QUrl):
            url = core.QUrl(url)
        return core.Url(self.findFile(url))

    def get_filter_engine(self) -> qthelp.HelpFilterEngine:
        return qthelp.HelpFilterEngine(self.filterEngine())


class HelpEngineCore(HelpEngineCoreMixin, qthelp.QHelpEngineCore):
    pass


if __name__ == "__main__":
    engine = HelpEngineCore("")
    engine.get_files("a", "b")
