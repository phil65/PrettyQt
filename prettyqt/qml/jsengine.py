# -*- coding: utf-8 -*-

from typing import Optional

from qtpy import QtQml

from prettyqt import core
from prettyqt.utils import bidict

EXTENSIONS = bidict(
    translation=QtQml.QJSEngine.TranslationExtension,
    console=QtQml.QJSEngine.ConsoleExtension,
    garbage_collection=QtQml.QJSEngine.GarbageCollectionExtension,
    all=QtQml.QJSEngine.AllExtensions,
)

QtQml.QJSEngine.__bases__ = (core.Object,)


class JSEngine(QtQml.QJSEngine):
    def serialize_fields(self):
        return dict(ui_language=self.uiLanguage())

    def install_extensions(self, extension: str, obj: Optional[QtQml.QJSValue] = None):
        if obj is None:
            obj = QtQml.QJSValue()
        self.installExtensions(EXTENSIONS[extension], obj)
