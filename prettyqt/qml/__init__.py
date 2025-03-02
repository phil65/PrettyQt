"""Classes for QML and JavaScript languages."""

from __future__ import annotations

from prettyqt.qt.QtQml import *  # noqa: F403

from prettyqt.qt.QtQml import (
    qmlRegisterType as register_qml_type,  # noqa: N813
    qmlClearTypeRegistrations as clear_type_registrations,  # noqa: N813
)
from .qmlparserstatus import QmlParserStatus, QmlParserStatusMixin
from .qmlerror import QmlError
from .qmlexpression import QmlExpression
from .qmlproperty import QmlProperty
from .qmlpropertymap import QmlPropertyMap
from .jsvalue import JSValue
from .jsvalueiterator import JSValueIterator
from .jsengine import JSEngine, JSEngineMixin
from .qmlengine import QmlEngine, QmlEngineMixin
from .qmlapplicationengine import QmlApplicationEngine
from .qmlcomponent import QmlComponent
from .qmlimageproviderbase import QmlImageProviderBase, QmlImageProviderBaseMixin
from prettyqt.qt import QtQml

QT_MODULE = QtQml


def register_objects_from_module(module):
    from prettyqt import core
    from prettyqt.utils import classhelpers

    for kls in classhelpers.iter_classes_for_module(module):
        if core.ObjectMixin in kls.mro():
            register_class(kls)


def register_class(kls):
    register_qml_type(kls, kls.__module__, 1, 0, kls.__name__)


__all__ = [
    "JSEngine",
    "JSEngineMixin",
    "JSValue",
    "JSValueIterator",
    "QmlApplicationEngine",
    "QmlComponent",
    "QmlEngine",
    "QmlEngineMixin",
    "QmlError",
    "QmlExpression",
    "QmlImageProviderBase",
    "QmlImageProviderBaseMixin",
    "QmlParserStatus",
    "QmlParserStatusMixin",
    "QmlProperty",
    "QmlPropertyMap",
    "clear_type_registrations",
    "register_qml_type",
]
