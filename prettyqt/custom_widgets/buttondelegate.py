# -*- coding: utf-8 -*-
"""
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
            btn.set_disabled()
        else:
            btn.clicked.connect(btn_callback)
        return btn

    def setEditorData(self, editor, index):
        pass

    def setModelData(self, editor, model, index):
        pass

    @core.Slot()
    def currentIndexChanged(self):
        self.commitData.emit(self.sender())
