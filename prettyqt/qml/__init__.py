from __future__ import annotations

from prettyqt.qt.QtQml import *  # noqa: F403

from prettyqt.qt.QtQml import (
    qmlRegisterType as register_qml_type,
    qmlClearTypeRegistrations as clear_type_registrations,
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

    for Klass in classhelpers.iter_classes_for_module(module):
        if core.ObjectMixin in Klass.mro():
            register_class(Klass)


def register_class(Klass):
    register_qml_type(Klass, Klass.__module__, 1, 0, Klass.__name__)


__all__ = [
    "register_qml_type",
    "clear_type_registrations",
    "QmlParserStatus",
    "QmlError",
    "QmlExpression",
    "QmlProperty",
    "QmlParserStatusMixin",
    "QmlPropertyMap",
    "JSValue",
    "JSValueIterator",
    "QmlEngine",
    "QmlEngineMixin",
    "JSEngine",
    "JSEngineMixin",
    "QmlApplicationEngine",
    "QmlComponent",
    "QmlImageProviderBase",
    "QmlImageProviderBaseMixin",
]
