from __future__ import annotations

from prettyqt import widgets


class MarkdownWindow(widgets.MainWindow):
    def __init__(self):
        super().__init__()
        self.resize(500, 500)
        self.text_browser = widgets.TextBrowser()
        self.setCentralWidget(self.text_browser)
        # self.text_browser.loadFinished.connect(self._load_finished)
        self.create_menu()

    # def _load_finished(self):
    # frame = self.text_browser.page()
    # self.text_browser.page().setViewportSize(frame.contentsSize())
    # self.resize(frame.contentsSize())
    # html_data = frame.toHtml()

    def create_menu(self):
        act_exit = widgets.Action(
            text="&Exit",
            icon="mdi.exit-to-app",
            parent=self,
            shortcut="Ctrl+Q",
            statustip="Exit application",
            callback=self.close,
        )
        act_open = widgets.Action(
            text="&Open",
            icon="mdi.open-in-app",
            parent=self,
            shortcut="Ctrl+O",
            statustip="Open Markdown file",
            callback=self.open_new_file,
        )
        menubar = self.menuBar()
        menu_file = menubar.addMenu("&File")
        menu_file.addAction(act_open)
        menu_file.addAction(act_exit)

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
    #     self.show_markdown(self.filePath)

    def open_new_file(self):
        try:
            ext = {"All Text Files": [".md", ".markdown", ".txt"]}
            dlg = widgets.FileDialog(mode="open", extension_filter=ext)
            if (fname := dlg.open_file()) is not None:
                self.text_browser.set_markdown_file(fname[0])
        except UnicodeDecodeError:
            self.statusBar().showMessage("Please select only text files")
        except OSError:
            self.statusBar().showMessage("File open canceled!")


if __name__ == "__main__":
    app = widgets.app()
    reader = MarkdownWindow()
    # reader.text_browser.load(QtCore.QUrl("blank"))
    reader.show()
    app.main_loop()
