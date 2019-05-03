# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtCore

from prettyqt import core, widgets


class ButtonDelegate(widgets.ItemDelegate):

    def __init__(self, parent, role=QtCore.Qt.UserRole):
        super().__init__(parent)
        self.fn_role = role

    def createEditor(self, parent, option, index) -> widgets.PushButton:
        label = index.data()
        btn_callback = index.data(self.fn_role)
        btn = widgets.PushButton(label, parent)
        if not btn_callback:
            btn.setEnabled(False)
        else:
            btn.clicked.connect(btn_callback)
        # btn.setStyleSheet("border:1px;")
        return btn

    def setEditorData(self, editor, index):
        editor.blockSignals(True)
        # editor.setCurrentIndex(int(index.model().data(index)))
        editor.blockSignals(False)

    def setModelData(self, editor, model, index):
        pass
        # model.setData(index, editor.text())

    @core.Slot()
    def currentIndexChanged(self):
        self.commitData.emit(self.sender())
