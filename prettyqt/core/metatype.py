from __future__ import annotations

import enum
from typing import Literal

from prettyqt.qt import QtCore
from prettyqt.utils import bidict, get_repr


TYPE = bidict(
    void=QtCore.QMetaType.Type.Void,
    bool=QtCore.QMetaType.Type.Bool,
    int=QtCore.QMetaType.Type.Int,
    u_int=QtCore.QMetaType.Type.UInt,
    double=QtCore.QMetaType.Type.Double,
    qchar=QtCore.QMetaType.Type.QChar,
    qstring=QtCore.QMetaType.Type.QString,
    byte_array=QtCore.QMetaType.Type.QByteArray,
    # nullptr=QtCore.QMetaType.Type.Nullptr,
    void_star=QtCore.QMetaType.Type.VoidStar,
    long=QtCore.QMetaType.Type.Long,
    long_long=QtCore.QMetaType.Type.LongLong,
    short=QtCore.QMetaType.Type.Short,
    char=QtCore.QMetaType.Type.Char,
    # char_16=QtCore.QMetaType.Type.Char16,
    # char_32=QtCore.QMetaType.Type.Char32,
    u_long=QtCore.QMetaType.Type.ULong,
    u_long_long=QtCore.QMetaType.Type.ULongLong,
    u_short=QtCore.QMetaType.Type.UShort,
    s_char=QtCore.QMetaType.Type.SChar,
    u_char=QtCore.QMetaType.Type.UChar,
    float=QtCore.QMetaType.Type.Float,
    # float_16=QtCore.QMetaType.Type.Float16,
    object_star=QtCore.QMetaType.Type.QObjectStar,
    cursor=QtCore.QMetaType.Type.QCursor,
    date=QtCore.QMetaType.Type.QDate,
    size=QtCore.QMetaType.Type.QSize,
    time=QtCore.QMetaType.Type.QTime,
    variant_list=QtCore.QMetaType.Type.QVariantList,
    polygon=QtCore.QMetaType.Type.QPolygon,
    polygonf=QtCore.QMetaType.Type.QPolygonF,
    color=QtCore.QMetaType.Type.QColor,
    color_space=QtCore.QMetaType.Type.QColorSpace,
    sizef=QtCore.QMetaType.Type.QSizeF,
    rectf=QtCore.QMetaType.Type.QRectF,
    line=QtCore.QMetaType.Type.QLine,
    text_length=QtCore.QMetaType.Type.QTextLength,
    string_list=QtCore.QMetaType.Type.QStringList,
    variant_map=QtCore.QMetaType.Type.QVariantMap,
    variant_hash=QtCore.QMetaType.Type.QVariantHash,
    # variant_pair=QtCore.QMetaType.Type.QVariantPair,
    icon=QtCore.QMetaType.Type.QIcon,
    pen=QtCore.QMetaType.Type.QPen,
    linef=QtCore.QMetaType.Type.QLineF,
    text_format=QtCore.QMetaType.Type.QTextFormat,
    rect=QtCore.QMetaType.Type.QRect,
    point=QtCore.QMetaType.Type.QPoint,
    url=QtCore.QMetaType.Type.QUrl,
    regular_expression=QtCore.QMetaType.Type.QRegularExpression,
    datetime=QtCore.QMetaType.Type.QDateTime,
    pointf=QtCore.QMetaType.Type.QPointF,
    palette=QtCore.QMetaType.Type.QPalette,
    font=QtCore.QMetaType.Type.QFont,
    brush=QtCore.QMetaType.Type.QBrush,
    region=QtCore.QMetaType.Type.QRegion,
    bit_array=QtCore.QMetaType.Type.QBitArray,
    image=QtCore.QMetaType.Type.QImage,
    key_sequence=QtCore.QMetaType.Type.QKeySequence,
    size_policy=QtCore.QMetaType.Type.QSizePolicy,
    pixmap=QtCore.QMetaType.Type.QPixmap,
    locale=QtCore.QMetaType.Type.QLocale,
    bitmap=QtCore.QMetaType.Type.QBitmap,
    transform=QtCore.QMetaType.Type.QTransform,
    matrix_4x4=QtCore.QMetaType.Type.QMatrix4x4,
    vector_2d=QtCore.QMetaType.Type.QVector2D,
    vector_3d=QtCore.QMetaType.Type.QVector3D,
    vector_4d=QtCore.QMetaType.Type.QVector4D,
    quaternion=QtCore.QMetaType.Type.QQuaternion,
    easing_curve=QtCore.QMetaType.Type.QEasingCurve,
    json_value=QtCore.QMetaType.Type.QJsonValue,
    json_object=QtCore.QMetaType.Type.QJsonObject,
    json_array=QtCore.QMetaType.Type.QJsonArray,
    json_document=QtCore.QMetaType.Type.QJsonDocument,
    cbor_value=QtCore.QMetaType.Type.QCborValue,
    cbor_array=QtCore.QMetaType.Type.QCborArray,
    cbor_map=QtCore.QMetaType.Type.QCborMap,
    cbor_simple_style=QtCore.QMetaType.Type.QCborSimpleType,
    model_index=QtCore.QMetaType.Type.QModelIndex,
    persistent_model_index=QtCore.QMetaType.Type.QPersistentModelIndex,
    uuid=QtCore.QMetaType.Type.QUuid,
    byte_array_list=QtCore.QMetaType.Type.QByteArrayList,
    variant=QtCore.QMetaType.Type.QVariant,
    user=QtCore.QMetaType.Type.User,
    unknown_type=QtCore.QMetaType.Type.UnknownType,
)

TypeFlagStr = Literal[
    "needs_construction",
    "needs_copy_construction",
    "needs_move_construction",
    "needs_destruction",
    "relocatable_type",
    "is_enumeration",
    "is_unsigned_enumeration",
    "pointer_to_qobject",
    "is_pointer",
    "is_const",
]

TYPE_FLAG = bidict(
    needs_construction=QtCore.QMetaType.TypeFlag.NeedsConstruction,
    needs_copy_construction=QtCore.QMetaType.TypeFlag.NeedsCopyConstruction,
    needs_move_construction=QtCore.QMetaType.TypeFlag.NeedsMoveConstruction,
    needs_destruction=QtCore.QMetaType.TypeFlag.NeedsDestruction,
    relocatable_type=QtCore.QMetaType.TypeFlag.RelocatableType,
    is_enumeration=QtCore.QMetaType.TypeFlag.IsEnumeration,
    is_unsigned_enumeration=QtCore.QMetaType.TypeFlag.IsUnsignedEnumeration,
    pointer_to_qobject=QtCore.QMetaType.TypeFlag.PointerToQObject,
    is_pointer=QtCore.QMetaType.TypeFlag.IsPointer,
    is_const=QtCore.QMetaType.TypeFlag.IsConst,
)

TYPE_END_INDEX = 63

ENUM_START_INDEX = 65537
ENUM_END_INDEX = 66065


class MetaType(QtCore.QMetaType):
    def __bool__(self):
        return self.isValid()

    def __repr__(self):
        return get_repr(self, self.get_name())

    @classmethod
    def get_regular_types(cls):
        return [
            meta for i in range(TYPE_END_INDEX + 1) if (meta := MetaType(i)).isValid()
        ]

    @classmethod
    def get_enum_types(cls):
        return [
            meta
            for i in range(ENUM_START_INDEX, ENUM_END_INDEX + 1)
            if (meta := MetaType(i)).isValid()
        ]

    def get_name(self) -> str | None:
        return name.decode() if isinstance(name := self.name(), bytes) else name

    def get_type_name(self) -> str:
        return TYPE.inverse[QtCore.QMetaType.Type(self.id())]

    def is_enumeration(self) -> bool:
        return bool(self.flags() & QtCore.QMetaType.TypeFlag.IsEnumeration)

    # def get_meta_object(self) -> core.MetaObject:  # apparently doesnt exist in bindings
    #     return core.MetaObject(self.metaObject())

    # @classmethod  # and this one gives deprecated message
    # def get_meta_object_for_type(cls, typ: int) -> core.MetaObject:
    #     return core.MetaObject(cls.metaObjectForType(typ))

    def get_type(self) -> type:
        meta_type = QtCore.QMetaType.Type(self.id())
        match meta_type:
            case QtCore.QMetaType.Type.Bool:
                return bool
            case QtCore.QMetaType.Type.Int | QtCore.QMetaType.Type.UInt:
                return int
            case QtCore.QMetaType.Type.Double | QtCore.QMetaType.Type.Float:
                return float
            case QtCore.QMetaType.Type.QChar | QtCore.QMetaType.Type.QString:
                return str
            case QtCore.QMetaType.Type.QByteArray:
                return bytes
            case QtCore.QMetaType.Type.QVariantList:
                return list
            case QtCore.QMetaType.Type.QVariantMap:
                return dict
            case QtCore.QMetaType.Type.QSize:
                return QtCore.QSize
            case QtCore.QMetaType.Type.QSizeF:
                return QtCore.QSizeF
            case QtCore.QMetaType.Type.QTime:
                return QtCore.QTime
            case QtCore.QMetaType.Type.QDate:
                return QtCore.QDate
            case QtCore.QMetaType.Type.QDateTime:
                return QtCore.QDateTime
            case QtCore.QMetaType.Type.QRect:
                return QtCore.QRect
            case QtCore.QMetaType.Type.QRectF:
                return QtCore.QRectF
            case QtCore.QMetaType.Type.QLine:
                return QtCore.QLine
            case QtCore.QMetaType.Type.QLineF:
                return QtCore.QLineF
            case QtCore.QMetaType.Type.QPoint:
                return QtCore.QPoint
            case QtCore.QMetaType.Type.QPointF:
                return QtCore.QPointF
            case QtCore.QMetaType.Type.QRegularExpression:
                return QtCore.QRegularExpression
            case QtCore.QMetaType.Type.QLocale:
                return QtCore.QLocale
            case QtCore.QMetaType.Type.QUrl:
                return QtCore.QUrl
            case _ if self.is_enumeration():
                return enum.Enum

        from prettyqt.qt import QtGui

        match meta_type:
            case QtCore.QMetaType.Type.QPolygon:
                return QtGui.QPolygon
            case QtCore.QMetaType.Type.QPolygonF:
                return QtGui.QPolygonF
            case QtCore.QMetaType.Type.QTextLength:
                return QtGui.QTextLength
            case QtCore.QMetaType.Type.QRegion:
                return QtGui.QRegion
            case QtCore.QMetaType.Type.QPalette:
                return QtGui.QPalette
            case QtCore.QMetaType.Type.QColor:
                return QtGui.QColor
            case QtCore.QMetaType.Type.QPen:
                return QtGui.QPen
            case QtCore.QMetaType.Type.QFont:
                return QtGui.QFont
            case QtCore.QMetaType.Type.QBrush:
                return QtGui.QBrush
            case QtCore.QMetaType.Type.QImage:
                return QtGui.QImage
            case QtCore.QMetaType.Type.QPixmap:
                return QtGui.QPixmap
            case QtCore.QMetaType.Type.QTransform:
                return QtGui.QTransform
            case QtCore.QMetaType.Type.QKeySequence:
                return QtGui.QKeySequence
            case QtCore.QMetaType.Type.QVector3D:
                return QtGui.QVector3D
            case QtCore.QMetaType.Type.QVector4D:
                return QtGui.QVector4D
            case QtCore.QMetaType.Type.QCursor:
                return QtGui.QCursor
            case QtCore.QMetaType.Type.QIcon:
                return QtGui.QIcon

        from prettyqt.qt import QtWidgets

        match meta_type:
            case QtCore.QMetaType.Type.QSizePolicy:
                return QtWidgets.QSizePolicy
            case _:
                raise NotImplementedError(self.id())


if __name__ == "__main__":
    metatype = MetaType(2)
