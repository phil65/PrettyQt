# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

import pathlib
from typing import Optional, Union

from bidict import bidict
from qtpy import QtCore, QtWidgets

from prettyqt import gui, widgets

H_ALIGNMENTS = dict(left=QtCore.Qt.AlignLeft,
                    right=QtCore.Qt.AlignRight,
                    center=QtCore.Qt.AlignHCenter,
                    justify=QtCore.Qt.AlignJustify)

V_ALIGNMENTS = dict(top=QtCore.Qt.AlignTop,
                    bottom=QtCore.Qt.AlignBottom,
                    center=QtCore.Qt.AlignVCenter,
                    baseline=QtCore.Qt.AlignBaseline)

TEXT_INTERACTION = bidict(dict(none=QtCore.Qt.NoTextInteraction,
                               by_mouse=QtCore.Qt.TextSelectableByMouse,
                               by_keyboard=QtCore.Qt.TextSelectableByKeyboard))

TEXT_FORMATS = bidict(dict(rich=QtCore.Qt.RichText,
                           plain=QtCore.Qt.PlainText,
                           auto=QtCore.Qt.AutoText))


class Label(QtWidgets.QLabel):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.openExternalLinks()

    def __repr__(self):
        return f"Label({self.text()!r})"

    def __getstate__(self):
        return dict(text=self.text(),
                    scaled_contents=self.hasScaledContents(),
                    indent=self.indent(),
                    margin=self.margin(),
                    text_format=self.get_text_format(),
                    # pixmap=self.pixmap(),
                    open_external_links=self.openExternalLinks(),
                    alignment=int(self.alignment()),
                    word_wrap=self.wordWrap())

    def __setstate__(self, state):
        self.__init__()
        self.setText(state.get("text", ""))
        self.setIndent(state.get("indent", -1))
        self.setMargin(state.get("margin", 0))
        self.setWordWrap(state.get("word_wrap", 0))
        self.set_text_format(state.get("text_format", 0))
        # self.setPixmap(state.get("pixmap"))
        self.setOpenExternalLinks(state.get("open_external_links", False))
        self.setAlignment(QtCore.Qt.Alignment(state.get("alignment")))
        self.setScaledContents(state["scaled_contents"])
        self.setWordWrap(state["word_wrap"])

    def set_alignment(self,
                      horizontal: Optional[str] = None,
                      vertical: Optional[str] = None):
        if horizontal is None and vertical is not None:
            flag = V_ALIGNMENTS.get(vertical)
        elif vertical is None and horizontal is not None:
            flag = H_ALIGNMENTS.get(horizontal)
        elif vertical is not None and horizontal is not None:
            flag = V_ALIGNMENTS.get(vertical) | H_ALIGNMENTS.get(horizontal)
        else:
            return
        self.setAlignment(flag)

    def set_text_format(self, text_format: str):
        self.setTextFormat(TEXT_FORMATS[text_format])

    def get_text_format(self) -> str:
        return TEXT_FORMATS.inv[self.textFormat()]

    def set_text_interaction(self, interaction_type: str):
        self.setTextInteractionFlags(TEXT_INTERACTION[interaction_type])

    def get_text_interaction(self) -> str:
        return TEXT_INTERACTION.inv[self.textInteractionFlags()]

    def set_image(self,
                  path: Union[pathlib.Path, str],
                  width: int = 300):
        self.setScaledContents(True)
        self.set_alignment(horizontal="center")
        self.setText("<html><head/><body><p>"
                     f"<img src={str(path)!r} width={str(width)!r}/>"
                     "</p></body></html>")

    @classmethod
    def image_from_path(cls,
                        path: Union[pathlib.Path, str],
                        parent=None) -> "Label":
        pixmap = gui.Pixmap.from_file(path)
        label = cls(parent=parent)
        label.setPixmap(pixmap)
        label.resize(pixmap.width(), pixmap.height())
        return label


Label.__bases__[0].__bases__ = (widgets.Frame,)


if __name__ == "__main__":
    app = widgets.app()
    widget = Label("test")
    widget.show()
    app.exec_()
