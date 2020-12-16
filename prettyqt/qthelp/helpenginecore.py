from typing import List, Optional

from qtpy import QtCore, QtHelp

from prettyqt import core


QtHelp.QHelpEngineCore.__bases__ = (core.Object,)


class HelpEngineCore(QtHelp.QHelpEngineCore):
    def get_file_data(self, url: QtCore.QUrl) -> bytes:
        return bytes(self.fileData(url))

    def get_files(
        self,
        namespace_name: str,
        filter_name: str,
        extension_filter: Optional[str] = None,
    ) -> List[core.Url]:
        return [
            core.Url(i) for i in self.files(namespace_name, filter_name, extension_filter)
        ]

    def find_file(self, url: QtCore.QUrl) -> core.Url:
        return core.Url(self.findFile(url))


if __name__ == "__main__":
    engine = HelpEngineCore("")
    engine.get_files("a", "b")
