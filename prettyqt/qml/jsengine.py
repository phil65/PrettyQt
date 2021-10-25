from __future__ import annotations

from prettyqt import core, qml
from prettyqt.qt import QtQml
from prettyqt.utils import bidict


EXTENSIONS = bidict(
    translation=QtQml.QJSEngine.Extension.TranslationExtension,
    console=QtQml.QJSEngine.Extension.ConsoleExtension,
    garbage_collection=QtQml.QJSEngine.Extension.GarbageCollectionExtension,
    all=QtQml.QJSEngine.Extension.AllExtensions,
)

QtQml.QJSEngine.__bases__ = (core.Object,)


class JSEngine(QtQml.QJSEngine):
    def serialize_fields(self):
        return dict(ui_language=self.uiLanguage())

    def install_extensions(self, extension: str, obj: QtQml.QJSValue | None = None):
        if obj is None:
            obj = QtQml.QJSValue()
        self.installExtensions(EXTENSIONS[extension], obj)

    def new_array(self, length: int = 0) -> qml.JSValue:
        return qml.JSValue(self.newArray(length))

    def eval(self, program: str):
        result = self.evaluate(program)
        return qml.JSValue(result)  # type: ignore


if __name__ == "__main__":
    app = core.CoreApplication([])
    engine = JSEngine()
    fun = engine.eval("(function(a, b) { return a + b; })")
    result = fun(1, 2)
    print(result)
