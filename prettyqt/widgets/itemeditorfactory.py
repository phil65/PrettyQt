from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtCore, QtGui, QtWidgets


TYPES = {
    bool: 1,
    int: 2,
    str: 10,
    float: 38,
    QtGui.QColor: 67,
    QtGui.QCursor: 74,
    QtCore.QDate: 14,
    QtCore.QSize: 21,
    QtCore.QTime: 15,
    list: 9,
    QtGui.QPolygon: 71,
    QtGui.QPolygonF: 86,
    QtGui.QColor: 67,
    QtGui.QColorSpace: 87,
    QtCore.QSizeF: 22,
    QtCore.QRectF: 20,
    QtCore.QLine: 23,
    QtGui.QTextLength: 77,
    dict: 8,
    QtGui.QIcon: 69,
    QtGui.QPen: 76,
    QtCore.QLineF: 24,
    QtGui.QTextFormat: 78,
    QtCore.QRect: 19,
    QtCore.QPoint: 25,
    QtCore.QUrl: 17,
    QtCore.QRegularExpression: 44,
    QtCore.QDateTime: 16,
    QtCore.QPointF: 26,
    QtGui.QPalette: 68,
    QtGui.QFont: 64,
    QtGui.QBrush: 66,
    QtGui.QRegion: 72,
    QtGui.QImage: 70,
    QtGui.QKeySequence: 75,
    QtWidgets.QSizePolicy: 121,
    QtGui.QPixmap: 65,
    QtCore.QLocale: 18,
    QtGui.QBitmap: 73,
    QtGui.QMatrix4x4: 81,
    QtGui.QVector2D: 82,
    QtGui.QVector3D: 83,
    QtGui.QVector4D: 84,
    QtGui.QQuaternion: 85,
    QtCore.QEasingCurve: 29,
    QtCore.QJsonValue: 45,
    QtCore.QJsonDocument: 48,
    QtCore.QModelIndex: 42,
    QtCore.QPersistentModelIndex: 50,
    QtCore.QUuid: 30,
    "user": 1024,
}


class ItemEditorFactory(QtWidgets.QItemEditorFactory):
    @classmethod
    def register_default_editor(
        cls, editor_cls: type[QtWidgets.QWidget], typ: int | None = None
    ):
        factory = cls.defaultFactory()
        factory.register_editor(editor_cls, typ)
        cls.setDefaultFactory(factory)

    def register_editor(
        self,
        editor_cls: type[QtWidgets.QWidget],
        typ: int | None = None,
        property_name: str = "",
    ):
        class EditorCreator(widgets.ItemEditorCreatorBase):
            def createWidget(self, parent: QtWidgets.QWidget) -> QtWidgets.QWidget:
                return editor_cls(parent=parent)

            def valuePropertyName(self) -> QtCore.QByteArray:
                return QtCore.QByteArray(property_name.encode())

        if typ is None:
            typ = editor_cls.staticMetaObject.userProperty().userType()
        self.registerEditor(typ, EditorCreator())


factory = ItemEditorFactory()
ItemEditorFactory.setDefaultFactory(factory)
