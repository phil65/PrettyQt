# -*- coding: utf-8 -*-

from qtpy import QtGui


class TextBlock(QtGui.QTextBlock):
    def __repr__(self):
        return f"TextBlock('{self.text()}')"


if __name__ == "__main__":
    doc = TextBlock()
