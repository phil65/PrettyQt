from __future__ import annotations

from prettyqt import widgets
from prettyqt.qt import QtCore, QtGui, QtWidgets


TYPES = {
    bool: QtCore.QMetaType.Type.Bool,
    int: QtCore.QMetaType.Type.Int,
    str: QtCore.QMetaType.Type.QString,
    float: QtCore.QMetaType.Type.Double,
    QtGui.QColor: QtCore.QMetaType.Type.QColor,
    QtGui.QCursor: QtCore.QMetaType.Type.QCursor,
    QtCore.QDate: QtCore.QMetaType.Type.QDate,
    QtCore.QSize: QtCore.QMetaType.Type.QSize,
    QtCore.QTime: QtCore.QMetaType.Type.QTime,
    list: QtCore.QMetaType.Type.QVariantList,
    QtGui.QPolygon: QtCore.QMetaType.Type.QPolygon,
    QtGui.QPolygonF: QtCore.QMetaType.Type.QPolygonF,
    QtGui.QColor: QtCore.QMetaType.Type.QColor,
    QtGui.QColorSpace: QtCore.QMetaType.Type.QColorSpace,
    QtCore.QSizeF: QtCore.QMetaType.Type.QSizeF,
    QtCore.QRectF: QtCore.QMetaType.Type.QRectF,
    QtCore.QLine: QtCore.QMetaType.Type.QLine,
    QtGui.QTextLength: QtCore.QMetaType.Type.QTextLength,
    dict: QtCore.QMetaType.Type.QVariantMap,
    QtGui.QIcon: QtCore.QMetaType.Type.QIcon,
    QtGui.QPen: QtCore.QMetaType.Type.QPen,
    QtCore.QLineF: QtCore.QMetaType.Type.QLineF,
    QtGui.QTextFormat: QtCore.QMetaType.Type.QTextFormat,
    QtCore.QRect: QtCore.QMetaType.Type.QRect,
    QtCore.QPoint: QtCore.QMetaType.Type.QPoint,
    QtCore.QUrl: QtCore.QMetaType.Type.QUrl,
    QtCore.QRegularExpression: QtCore.QMetaType.Type.QRegularExpression,
    QtCore.QDateTime: QtCore.QMetaType.Type.QDateTime,
    QtCore.QPointF: QtCore.QMetaType.Type.QPointF,
    QtGui.QPalette: QtCore.QMetaType.Type.QPalette,
    QtGui.QFont: QtCore.QMetaType.Type.QFont,
    QtGui.QBrush: QtCore.QMetaType.Type.QBrush,
    QtGui.QRegion: QtCore.QMetaType.Type.QRegion,
    QtGui.QImage: QtCore.QMetaType.Type.QImage,
    QtGui.QKeySequence: QtCore.QMetaType.Type.QKeySequence,
    QtWidgets.QSizePolicy: QtCore.QMetaType.Type.QSizePolicy,
    QtGui.QPixmap: QtCore.QMetaType.Type.QPixmap,
    QtCore.QLocale: QtCore.QMetaType.Type.QLocale,
    QtGui.QBitmap: QtCore.QMetaType.Type.QBitmap,
    QtGui.QMatrix4x4: QtCore.QMetaType.Type.QMatrix4x4,
    QtGui.QVector2D: QtCore.QMetaType.Type.QVector2D,
    QtGui.QVector3D: QtCore.QMetaType.Type.QVector3D,
    QtGui.QVector4D: QtCore.QMetaType.Type.QVector4D,
    QtGui.QQuaternion: QtCore.QMetaType.Type.QQuaternion,
    QtCore.QEasingCurve: QtCore.QMetaType.Type.QEasingCurve,
    QtCore.QJsonValue: QtCore.QMetaType.Type.QJsonValue,
    QtCore.QJsonDocument: QtCore.QMetaType.Type.QJsonDocument,
    QtCore.QModelIndex: QtCore.QMetaType.Type.QModelIndex,
    QtCore.QPersistentModelIndex: QtCore.QMetaType.Type.QPersistentModelIndex,
    QtCore.QUuid: QtCore.QMetaType.Type.QUuid,
}


def get_creator(editor_cls: type[QtWidgets.QWidget], property_name: str = ""):
    class EditorCreator(widgets.ItemEditorCreatorBase):
        def createWidget(self, parent: QtWidgets.QWidget) -> QtWidgets.QWidget:
            return editor_cls(parent=parent)

        def valuePropertyName(self) -> QtCore.QByteArray:
            return QtCore.QByteArray(property_name.encode())

    return EditorCreator()


class ItemEditorFactory(QtWidgets.QItemEditorFactory):
    @classmethod
    def register_default_editor(
        cls,
        editor_cls: type[QtWidgets.QWidget],
        typ: int | None | type = None,
        property_name: str = "",
    ):
        factory = cls.defaultFactory()
        creator = get_creator(editor_cls, property_name)
        if typ is None:
            typ = editor_cls.staticMetaObject.userProperty().userType()
        elif isinstance(typ, type):
            typ = TYPES[typ].value
        factory.registerEditor(typ, creator)
        cls.setDefaultFactory(factory)

    def register_editor(
        self,
        editor_cls: type[QtWidgets.QWidget],
        typ: int | None | type = None,
        property_name: str = "",
    ):
        creator = get_creator(editor_cls, property_name)
        if typ is None:
            typ = editor_cls.staticMetaObject.userProperty().userType()
        elif isinstance(typ, type):
            typ = TYPES[typ].value
        self.registerEditor(typ, creator)


# factory = ItemEditorFactory()
# ItemEditorFactory.setDefaultFactory(factory)

if __name__ == "__main__":
    """Run the application."""
    from prettyqt import constants, custom_widgets

    app = widgets.app()
    table_widget = widgets.TableWidget(1, 2)
    # table_widget.set_delegate(StarDelegate(), column=1)
    table_widget.setEditTriggers(
        table_widget.EditTrigger.DoubleClicked  # type: ignore
        | table_widget.EditTrigger.SelectedClicked
    )
    table_widget.set_selection_behaviour("rows")
    table_widget.setHorizontalHeaderLabels(["Title", "Rating"])
    factory = ItemEditorFactory()
    factory.register_editor(custom_widgets.ColorChooserButton, QtGui.QColor, "color")
    factory.setDefaultFactory(factory)
    item_1 = widgets.TableWidgetItem("Test1")
    item_2 = widgets.TableWidgetItem()
    item_2.setData(constants.DISPLAY_ROLE, QtGui.QColor(30, 30, 30))
    table_widget[0, 0] = item_1
    table_widget[0, 1] = item_2

    table_widget.resizeColumnsToContents()
    table_widget.resize(500, 300)
    table_widget.show()

    app.main_loop()
