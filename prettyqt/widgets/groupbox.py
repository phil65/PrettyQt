# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtCore, QtWidgets

from prettyqt import widgets

H_ALIGNMENTS = dict(left=QtCore.Qt.AlignLeft,
                    right=QtCore.Qt.AlignRight,
                    center=QtCore.Qt.AlignHCenter)


class GroupBox(QtWidgets.QGroupBox):

    def __repr__(self):
        return f"GroupBox: {self.count()} children"

    def __getstate__(self):
        return dict(checkable=self.isCheckable(),
                    checked=self.isChecked(),
                    layout=self.layout(),
                    flat=self.isFlat(),
                    # alignment=self.alignment(),
                    title=self.title())

    def __setstate__(self, state):
        self.__init__(state["title"])
        self.setLayout(state["layout"])
        self.setCheckable(state["checkable"])
        self.setChecked(state["checked"])
        self.setFlat(state["flat"])
        # self.setAlignment(state["alignment"])

    def set_alignment(self, alignment):
        self.setAlignment(H_ALIGNMENTS[alignment])

    def set_layout(self, layout):
        self.setLayout(layout)


if __name__ == "__main__":
    app = widgets.Application.create_default_app()
    widget = GroupBox()
    ly = widgets.BoxLayout()
    ly += widgets.RadioButton("test")
    widget.setLayout(ly)
    widget.show()
    app.exec_()
