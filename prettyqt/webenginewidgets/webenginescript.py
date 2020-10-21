# -*- coding: utf-8 -*-


try:
    from PyQt5 import QtWebEngineWidgets  # type: ignore
except ImportError:
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
        return INJECTION_POINTS.inv[self.injectionPoint()]


if __name__ == "__main__":
    item = WebEngineScript()
