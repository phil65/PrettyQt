from __future__ import annotations

from typing import Literal

from prettyqt import core
from prettyqt.qt import QtCore
from prettyqt.utils import bidict


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
    point_f=QtCore.QMetaType.Type.QPointF,
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
    "pinter_to_qobject",
    "is_pointer",
    "is_const",
]

TYPE_FLAG = bidict(
    needs_construction=QtCore.QMetaType.TypeFlag.NeedsConstruction,
    # needs_copy_construction=QtCore.QMetaType.TypeFlag.NeedsCopyConstruction,
    # needs_move_construction=QtCore.QMetaType.TypeFlag.NeedsMoveConstruction,
    needs_destruction=QtCore.QMetaType.TypeFlag.NeedsDestruction,
    relocatable_type=QtCore.QMetaType.TypeFlag.RelocatableType,
    is_enumeration=QtCore.QMetaType.TypeFlag.IsEnumeration,
    is_unsigned_enumeration=QtCore.QMetaType.TypeFlag.IsUnsignedEnumeration,
    pinter_to_qobject=QtCore.QMetaType.TypeFlag.PointerToQObject,
    is_pointer=QtCore.QMetaType.TypeFlag.IsPointer,
    is_const=QtCore.QMetaType.TypeFlag.IsConst,
)


class MetaType(QtCore.QMetaType):
    def __init__(self, metatype: QtCore.QMetaType):
        self.item = metatype

    def __bool__(self):
        return self.item.isValid()

    def __repr__(self):
        return f"{type(self).__name__}({self.get_name()!r})"

    def get_name(self) -> str:
        return self.item.name()  # type: ignore


if __name__ == "__main__":
    metaobj = core.Object.get_metaobject()
    metatype = metaobj.get_meta_type()
    print(metatype.get_name())
