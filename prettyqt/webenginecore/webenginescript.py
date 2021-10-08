from __future__ import annotations

from typing import Literal

from prettyqt.qt import QtWebEngineCore
from prettyqt.utils import InvalidParamError, bidict


INJECTION_POINT = bidict(
    document_creation=QtWebEngineCore.QWebEngineScript.InjectionPoint.DocumentCreation,
    document_ready=QtWebEngineCore.QWebEngineScript.InjectionPoint.DocumentReady,
    deferred=QtWebEngineCore.QWebEngineScript.InjectionPoint.Deferred,
)

InjectionPointStr = Literal["document_creation", "document_ready", "deferred"]

SCRIPT_WORLD_IDS = bidict(
    main_world=QtWebEngineCore.QWebEngineScript.ScriptWorldId.MainWorld,
    application_world=QtWebEngineCore.QWebEngineScript.ScriptWorldId.ApplicationWorld,
    user_world=QtWebEngineCore.QWebEngineScript.ScriptWorldId.UserWorld,
)

ScriptWorldIdStr = Literal["main_world", "application_world", "user_world"]


class WebEngineScript(QtWebEngineCore.QWebEngineScript):
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
