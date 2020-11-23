# -*- coding: utf-8 -*-

from qtpy import QtGui


class TextBlock(QtGui.QTextBlock):
    def __repr__(self):
        return f"TextBlock('{self.text()}')"

    def __contains__(self, position: int):
        return self.contains(position)


if __name__ == "__main__":
    doc = TextBlock()
