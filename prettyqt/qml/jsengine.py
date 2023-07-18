from __future__ import annotations

from prettyqt import core, qml
from prettyqt.utils import bidict


EXTENSIONS = bidict(
    translation=qml.QJSEngine.Extension.TranslationExtension,
    console=qml.QJSEngine.Extension.ConsoleExtension,
    garbage_collection=qml.QJSEngine.Extension.GarbageCollectionExtension,
    all=qml.QJSEngine.Extension.AllExtensions,
)


class JSEngineMixin(core.ObjectMixin):
    def install_extensions(self, extension: str, obj: qml.QJSValue | None = None):
        if obj is None:
            obj = qml.QJSValue()
        self.installExtensions(EXTENSIONS[extension], obj)

    def new_array(self, length: int = 0) -> qml.JSValue:
        return qml.JSValue(self.newArray(length))

    def eval(self, program: str) -> qml.JSValue:
        result = self.evaluate(program)
        return qml.JSValue(result)  # type: ignore


class JSEngine(JSEngineMixin, qml.QJSEngine):
    """Environment for evaluating JavaScript code."""


if __name__ == "__main__":
    app = core.app()
    engine = JSEngine()
    fun = engine.eval("(function(a, b) { return a + b; })")
    result = fun(1, 2)
    print(result)
