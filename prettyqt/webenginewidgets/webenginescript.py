from qtpy import PYQT5, PYSIDE2

if PYQT5:
    from PyQt5 import QtWebEngineWidgets  # type: ignore
elif PYSIDE2:
    from PySide2 import QtWebEngineWidgets

from prettyqt.utils import bidict, InvalidParamError


INJECTION_POINTS = bidict(
    document_creation=QtWebEngineWidgets.QWebEngineScript.DocumentCreation,
    document_ready=QtWebEngineWidgets.QWebEngineScript.DocumentReady,
    deferred=QtWebEngineWidgets.QWebEngineScript.Deferred,
)

SCRIPT_WORLD_IDS = bidict(
    main_world=QtWebEngineWidgets.QWebEngineScript.MainWorld,
    application_world=QtWebEngineWidgets.QWebEngineScript.ApplicationWorld,
    user_world=QtWebEngineWidgets.QWebEngineScript.UserWorld,
)


class WebEngineScript(QtWebEngineWidgets.QWebEngineScript):
    def set_injection_point(self, point: str):
        """Set injection point.

        Allowed values are "document_creation", "document_ready", "deferred"

        Args:
            point: injection point to use

        Raises:
            InvalidParamError: injection point does not exist
        """
        if point not in INJECTION_POINTS:
            raise InvalidParamError(point, INJECTION_POINTS)
        self.setInjectionPoint(INJECTION_POINTS[point])

    def get_injection_point(self) -> str:
        """Return injection point.

        Possible values: "document_creation", "document_ready", "deferred"

        Returns:
            injection point
        """
        return INJECTION_POINTS.inverse[self.injectionPoint()]


if __name__ == "__main__":
    item = WebEngineScript()
