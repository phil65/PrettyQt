from __future__ import annotations

from typing_extensions import Self

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
    QtGui.QTransform: QtCore.QMetaType.Type.QTransform,
    QtCore.QByteArray: QtCore.QMetaType.Type.QByteArray,
}


def get_creator_class(editor_cls: type[QtWidgets.QWidget], property_name: str = ""):
    class EditorCreator(widgets.ItemEditorCreatorBase):
        def createWidget(self, parent: QtWidgets.QWidget) -> QtWidgets.QWidget:
            return editor_cls(parent=parent)

        def valuePropertyName(self) -> QtCore.QByteArray:
            return QtCore.QByteArray(property_name.encode())

    return EditorCreator


class ItemEditorFactory(QtWidgets.QItemEditorFactory):
    creators = []

    @classmethod
    def register_default_editor(
        cls,
        editor_cls: type[QtWidgets.QWidget],
        typ: int | None | type = None,
        property_name: str = "",
    ):
        factory = cls.defaultFactory()
        creator = get_creator_class(editor_cls, property_name)()
        cls.creators.append(creator)
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
        creator = get_creator_class(editor_cls, property_name)()
        self.creators.append(creator)
        if typ is None:
            typ = editor_cls.staticMetaObject.userProperty().userType()
        elif isinstance(typ, type) and typ in TYPES:
            typ = TYPES[typ].value
        self.registerEditor(typ, creator)

    @classmethod
    def create_extended(cls) -> Self:
        factory = cls()
        factory.register_editor(widgets.CheckBox, bool, "")
        factory.register_editor(widgets.SpinBox, int, "value")
        factory.register_editor(widgets.LineEdit, str, "text")
        factory.register_editor(widgets.DoubleSpinBox, float, "value")
        factory.register_editor(widgets.DateEdit, QtCore.QDate, "date")
        factory.register_editor(widgets.TimeEdit, QtCore.QTime, "time")
        factory.register_editor(widgets.DateTimeEdit, QtCore.QDateTime, "dateTime")
        factory.register_editor(custom_widgets.PointEdit, QtCore.QPoint, "value")
        factory.register_editor(custom_widgets.SizeEdit, QtCore.QSize, "value")
        factory.register_editor(custom_widgets.RectEdit, QtCore.QRect, "value")
        # factory.register_editor(custom_widgets.EnumFlagWidget, 66231, "value")
        # factory.register_editor(custom_widgets.EnumComboBox, 20001, "value")
        factory.register_editor(custom_widgets.RegionEdit, QtGui.QRegion, "value")
        factory.register_editor(
            custom_widgets.SizePolicyEdit, QtWidgets.QSizePolicy, "value"
        )
        factory.register_editor(
            widgets.KeySequenceEdit, QtGui.QKeySequence, "keySequence"
        )
        factory.register_editor(
            custom_widgets.ColorComboBox, QtGui.QColor, "current_color"
        )
        factory.register_editor(widgets.FontComboBox, QtGui.QFont, "currentFont")
        factory.register_editor(widgets.LineEdit, QtCore.QUrl, "text")
        factory.register_editor(widgets.LineEdit, QtCore.QRegularExpression, "text")
        return factory


# factory = ItemEditorFactory()
# ItemEditorFactory.setDefaultFactory(factory)

if __name__ == "__main__":
    """Run the application."""
    from prettyqt import constants, custom_widgets

    app = widgets.app()
    table_widget = widgets.TableWidget(15, 2)
    # table_widget.set_delegate(StarDelegate(), column=1)
    table_widget.setEditTriggers(
        table_widget.EditTrigger.DoubleClicked  # type: ignore
        | table_widget.EditTrigger.SelectedClicked
    )
    table_widget.set_selection_behavior("rows")
    table_widget.setHorizontalHeaderLabels(["Title", "Rating"])
    factory = ItemEditorFactory.create_extended()
    # factory = ItemEditorFactory()
    # factory.register_editor(custom_widgets.ColorChooserButton, QtGui.QColor, "color")
    factory.setDefaultFactory(factory)
    types = dict(
        color=QtGui.QColor(30, 30, 30),
        time=QtCore.QTime(1, 1, 1),
        date=QtCore.QDate(1, 1, 1),
        datetime=QtCore.QDateTime(1, 1, 1, 1, 1, 1),
        font=QtGui.QFont(),
        str="fdsf",
        int=8,
        float=8.2,
        url=QtCore.QUrl("http://www.google.de"),
        regex=QtCore.QRegularExpression("[a-z]"),
        bool=True,
        keysequence=QtGui.QKeySequence("Ctrl+A"),
        enum=widgets.AbstractItemView.EditTrigger.DoubleClicked,
    )
    for i, (k, v) in enumerate(types.items()):
        item_1 = widgets.TableWidgetItem(k)
        item_2 = widgets.TableWidgetItem()
        item_2.setData(constants.DISPLAY_ROLE, v)
        table_widget[i, 0] = item_1
        table_widget[i, 1] = item_2

    table_widget.resizeColumnsToContents()
    table_widget.resize(500, 300)
    table_widget.show()

    app.main_loop()
