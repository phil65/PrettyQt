# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtCore, QtWidgets

from prettyqt import widgets

H_ALIGNMENTS = dict(left=QtCore.Qt.AlignLeft,
                    right=QtCore.Qt.AlignRight,
                    center=QtCore.Qt.AlignHCenter)


QtWidgets.QGroupBox.__bases__ = (widgets.Widget,)


class GroupBox(QtWidgets.QGroupBox):
    """GroupBox widget

    A group box provides a frame, a title on top, a keyboard shortcut,
    and displays various other widgets inside itself.
    The keyboard shortcut moves keyboard focus to one of the group box's child widgets.
    """

    def __init__(self, title="", checkable=False, parent=None):
        super().__init__(title, parent)
        self.setCheckable(checkable)

    def __repr__(self):
        return f"GroupBox({self.title()!r})"

    def __getstate__(self):
        return dict(checkable=self.isCheckable(),
                    checked=self.isChecked(),
                    tooltip=self.toolTip(),
                    layout=self.layout(),
                    flat=self.isFlat(),
                    # alignment=self.alignment(),
                    title=self.title())

    def __setstate__(self, state):
        self.__init__(state["title"])
        self.set_layout(state["layout"])
        self.setCheckable(state["checkable"])
        self.setChecked(state.get("checked", False))
        self.setFlat(state["flat"])
        self.setToolTip(state.get("tooltip", ""))
        # self.setAlignment(state["alignment"])

    def set_title(self, title: str):
        self.setTitle(title)

    def set_alignment(self, alignment):
        self.setAlignment(H_ALIGNMENTS[alignment])

    def set_enabled(self, state):
        for widget in self.layout():
            widget.setEnabled(state)


if __name__ == "__main__":
    app = widgets.app()
    widget = GroupBox()
    ly = widgets.BoxLayout()
    ly += widgets.RadioButton("test")
    widget.set_layout(ly)
    widget.show()
    app.exec_()
