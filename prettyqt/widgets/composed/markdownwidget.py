# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

import sys

from qtpy import QtWidgets
from prettyqt import gui, widgets

import markdown


class MarkdownWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.resize(500, 500)
        self.web_view = MarkdownWidget(self)
        self.setCentralWidget(self.web_view)
        # self.web_view.loadFinished.connect(self._load_finished)
        self.create_menu()

    # def _load_finished(self):
        # frame = self.web_view.page()
        # self.web_view.page().setViewportSize(frame.contentsSize())
        # self.resize(frame.contentsSize())
        # html_data = frame.toHtml()

    def create_menu(self):
        act_exit = widgets.Action(gui.Icon('exit.png'), '&Exit', self)
        act_exit.setShortcut('Ctrl+Q')
        act_exit.setStatusTip('Exit application')
        act_exit.triggered.connect(self.close)

        act_open = widgets.Action(gui.Icon('open.png'), '&Open', self)
        act_open.setShortcut('Ctrl+O')
        act_open.setStatusTip('Open Markdown file')
        act_open.triggered.connect(self.open_new_file)

        self.statusBar()

        menubar = self.menuBar()
        menu_file = menubar.addMenu('&File')
        menu_file.addAction(act_open)
        menu_file.addAction(act_exit)

    def open_new_file(self):
        try:
            fname = widgets.FileDialog.getOpenFileName(self,
                                                       'open file',
                                                       '',
                                                       'All Text Files (*.md *.markdown *.txt *.*)',
                                                       None,
                                                       QtWidgets.QFileDialog.DontUseNativeDialog)
            self.web_view.show_markdown(fname[0])
        except UnicodeDecodeError:
            self.statusBar().showMessage('Please select only text files')
        except IOError:
            self.statusBar().showMessage('File open canceled!')


class MarkdownWidget(QtWidgets.QTextBrowser):

    # def dragEnterEvent(self, event):
    #     u = event.mimeData().urls()
    #     for url in u:
    #         file_path = os.path.abspath(url.toLocalFile())

    #         ext = file_path.split('.')[-1]
    #         if ext in ['txt', 'md', 'markdown']:
    #             event.accept()
    #         else:
    #             event.ignore()

    # def dropEvent(self, event):
    #     event.accept()
    #     self.show_markdown(self.filePath)

    def contextMenuEvent(self, event):
        pass

    def show_markdown(self, file_path):
        markdown_file = open(file_path)
        file_content = markdown_file.read()
        self.setHtml(markdown.markdown(file_content))


def main():
    qtapp = QtWidgets.QApplication(sys.argv)
    reader = MarkdownWindow()
    # reader.web_view.load(QtCore.QUrl('blank'))
    reader.show()
    qtapp.exec_()


if __name__ == '__main__':
    main()
