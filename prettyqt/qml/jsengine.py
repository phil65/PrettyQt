from typing import TYPE_CHECKING, Literal

from prettyqt import core, qml
from prettyqt.utils import bidict


ExtensionStr = Literal["translation", "console", "garbage_collection", "all"]

EXTENSIONS: bidict[ExtensionStr, qml.QJSEngine.Extension] = bidict(
    translation=qml.QJSEngine.Extension.TranslationExtension,
    console=qml.QJSEngine.Extension.ConsoleExtension,
    garbage_collection=qml.QJSEngine.Extension.GarbageCollectionExtension,
    all=qml.QJSEngine.Extension.AllExtensions,
)


if TYPE_CHECKING:
    from prettyqt.qt import QtQml

    _JSEngineBase = QtQml.QJSEngine
else:
    _JSEngineBase = object


class JSEngineMixin(core.ObjectMixin, _JSEngineBase):
    def install_extensions(
        self,
        extension: ExtensionStr | qml.QJSEngine.Extension,
        obj: qml.QJSValue | None = None,
    ):
        if obj is None:
            obj = qml.QJSValue()
        self.installExtensions(EXTENSIONS.get_enum_value(extension), obj)

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
