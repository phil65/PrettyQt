from typing import Literal

from qtpy import PYQT5, PYSIDE2


if PYQT5:
    from PyQt5 import QtWebEngineWidgets  # type: ignore
elif PYSIDE2:
    from PySide2 import QtWebEngineWidgets

from prettyqt.utils import InvalidParamError, bidict


INJECTION_POINT = bidict(
    document_creation=QtWebEngineWidgets.QWebEngineScript.DocumentCreation,
    document_ready=QtWebEngineWidgets.QWebEngineScript.DocumentReady,
    deferred=QtWebEngineWidgets.QWebEngineScript.Deferred,
)

InjectionPointStr = Literal["document_creation", "document_ready", "deferred"]

SCRIPT_WORLD_IDS = bidict(
    main_world=QtWebEngineWidgets.QWebEngineScript.MainWorld,
    application_world=QtWebEngineWidgets.QWebEngineScript.ApplicationWorld,
    user_world=QtWebEngineWidgets.QWebEngineScript.UserWorld,
)

ScriptWorldIdStr = Literal["main_world", "application_world", "user_world"]


class WebEngineScript(QtWebEngineWidgets.QWebEngineScript):
    def set_injection_point(self, point: InjectionPointStr):
        """Set injection point.

        Args:
            point: injection point to use

        Raises:
            InvalidParamError: injection point does not exist
        """
        if point not in INJECTION_POINT:
            raise InvalidParamError(point, INJECTION_POINT)
        self.setInjectionPoint(INJECTION_POINT[point])

    def get_injection_point(self) -> InjectionPointStr:
        """Return injection point.

        Returns:
            injection point
        """
        return INJECTION_POINT.inverse[self.injectionPoint()]


if __name__ == "__main__":
    item = WebEngineScript()
