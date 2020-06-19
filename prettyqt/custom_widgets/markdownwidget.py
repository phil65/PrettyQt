# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from prettyqt import gui, widgets


class MarkdownWindow(widgets.MainWindow):

    def __init__(self):
        super().__init__()
        self.resize(500, 500)
        self.web_view = widgets.TextBrowser()
        self.setCentralWidget(self.web_view)
        # self.web_view.loadFinished.connect(self._load_finished)
        self.create_menu()

    # def _load_finished(self):
        # frame = self.web_view.page()
        # self.web_view.page().setViewportSize(frame.contentsSize())
        # self.resize(frame.contentsSize())
        # html_data = frame.toHtml()

    def create_menu(self):
        act_exit = widgets.Action(text="&Exit", icon=gui.Icon("exit.png"), parent=self)
        act_exit.set_shortcut("Ctrl+Q")
        act_exit.setStatusTip("Exit application")
        act_exit.triggered.connect(self.close)

        act_open = widgets.Action(text="&Open", icon=gui.Icon("open.png"), parent=self)
        act_open.set_shortcut("Ctrl+O")
        act_open.setStatusTip("Open Markdown file")
        act_open.triggered.connect(self.open_new_file)

        self.statusBar()

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
            dlg = widgets.FileDialog
            fname = dlg.getOpenFileName(self,
                                        "open file",
                                        "",
                                        "All Text Files (*.md *.markdown *.txt *.*)",
                                        None)
            self.web_view.set_markdown_file(fname[0])
        except UnicodeDecodeError:
            self.statusBar().showMessage("Please select only text files")
        except IOError:
            self.statusBar().showMessage("File open canceled!")


if __name__ == "__main__":
    app = widgets.app()
    reader = MarkdownWindow()
    # reader.web_view.load(QtCore.QUrl("blank"))
    reader.show()
    app.exec_()
