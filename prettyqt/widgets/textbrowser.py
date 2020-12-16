import pathlib
from typing import Union

from qtpy import QtWidgets

from prettyqt import core, gui, widgets


QtWidgets.QTextBrowser.__bases__ = (widgets.TextEdit,)


class TextBrowser(QtWidgets.QTextBrowser):

    value_changed = core.Signal(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setOpenExternalLinks(True)

    def serialize_fields(self):
        return dict(text=self.text(), font=gui.Font(self.font()))

    def __setstate__(self, state):
        self.setPlainText(state["text"])
        self.setEnabled(state.get("enabled", True))
        self.setFont(state["font"])

    def __reduce__(self):
        return type(self), (), self.__getstate__()

    # def dragEnterEvent(self, event):
    #     u = event.mimeData().urls()
    #     for url in u:
    #         file_path = os.path.abspath(url.toLocalFile())

    #         ext = file_path.split(".")[-1]
    #         if ext in ["txt", "md", "markdown"]:
    #             event.accept()
    #         else:
    #             event.ignore()

    # def dropEvent(self, event):
    #     event.accept()
    #     self.show_markdown_file(self.filePath)

    def set_markdown_file(self, file_path: Union[str, pathlib.Path]):
        if isinstance(file_path, str):
            file_path = pathlib.Path(file_path)
        with file_path.open() as f:
            file_content = f.read()
        self.set_markdown(file_content)

    def set_markdown(self, source: str):
        self.setMarkdown(source)

    def set_rst_file(self, file_path: Union[str, pathlib.Path]):
        if isinstance(file_path, str):
            file_path = pathlib.Path(file_path)
        with file_path.open() as f:
            file_content = f.read()
        self.set_rst(file_content)

    def set_rst(self, source: str):
        import docutils.core

        html = docutils.core.publish_string(source, writer_name="html")
        self.setHtml(str(html))


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    reader = TextBrowser()
    reader.show()
    app.main_loop()
