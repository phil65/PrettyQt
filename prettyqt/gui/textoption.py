from qtpy import QtGui


class TextOption(QtGui.QTextOption):
    def set_text(self, text: str):
        self.setPlainText(text)


if __name__ == "__main__":
    doc = TextOption()
