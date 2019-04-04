# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

import sys

from qtpy import QtWidgets

import markdown
import docutils.core


class TextBrowser(QtWidgets.QTextBrowser):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setOpenExternalLinks(True)

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

    def show_markdown(self, file_path):
        with open(file_path) as f:
            file_content = f.read()
        self.setHtml(markdown.markdown(file_content))

    def show_rst(self, file_path):
        with open(file_path) as f:
            html = docutils.core.publish_string(f.read(), writer_name='html')
        self.setHtml(str(html))


def main():
    qtapp = QtWidgets.QApplication(sys.argv)
    reader = TextBrowser()
    reader.show()
    qtapp.exec_()


if __name__ == '__main__':
    main()
