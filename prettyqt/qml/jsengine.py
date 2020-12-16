from typing import Optional

from qtpy import QtQml

from prettyqt import core, qml
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

    def new_array(self, length=0) -> qml.JSValue:
        return qml.JSValue(self.newArray(length))


if __name__ == "__main__":
    app = core.CoreApplication([])
    val = JSEngine()
    arr = val.new_array()
    arr["test"] = 1
    arr["tes2t"] = 1
    assert arr["test"] == 1
    for name, val in arr:
        print(name, val)
