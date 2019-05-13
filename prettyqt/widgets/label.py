# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

import pathlib
from typing import Optional, Union

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

TEXT_INTERACTION = dict(none=QtCore.Qt.NoTextInteraction,
                        by_mouse=QtCore.Qt.TextSelectableByMouse,
                        by_keyboard=QtCore.Qt.TextSelectableByKeyboard)


class Label(QtWidgets.QLabel):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.openExternalLinks()

    def __repr__(self):
        return f"Label('{self.text()}'')"

    def __getstate__(self):
        return dict(text=self.text(),
                    scaled_contents=self.hasScaledContents(),
                    word_wrap=self.wordWrap())

    def __setstate__(self, state):
        super().__init__()
        self.setText(state["text"])
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

    def set_text_interaction(self, interaction_type):
        self.setTextInteractionFlags(TEXT_INTERACTION[interaction_type])

    def set_image(self,
                  path: Union[pathlib.Path, str],
                  width: int = 300):
        self.setScaledContents(True)
        self.set_alignment(horizontal="center")
        self.setText("<html><head/><body><p>"
                     f'<img src="{path}" width="{width}"/>'
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


if __name__ == "__main__":
    app = widgets.Application.create_default_app()
    widget = Label("test")
    widget.show()
    app.exec_()
