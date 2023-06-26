from __future__ import annotations

from typing import Literal

from prettyqt.qt import QtWebEngineCore
from prettyqt.utils import bidict


InjectionPointStr = Literal["document_creation", "document_ready", "deferred"]

INJECTION_POINT: bidict[
    InjectionPointStr, QtWebEngineCore.QWebEngineScript.InjectionPoint
] = bidict(
    document_creation=QtWebEngineCore.QWebEngineScript.InjectionPoint.DocumentCreation,
    document_ready=QtWebEngineCore.QWebEngineScript.InjectionPoint.DocumentReady,
    deferred=QtWebEngineCore.QWebEngineScript.InjectionPoint.Deferred,
)

ScriptWorldIdStr = Literal["main_world", "application_world", "user_world"]

SCRIPT_WORLD_IDS: bidict[
    ScriptWorldIdStr, QtWebEngineCore.QWebEngineScript.ScriptWorldId
] = bidict(
    main_world=QtWebEngineCore.QWebEngineScript.ScriptWorldId.MainWorld,
    application_world=QtWebEngineCore.QWebEngineScript.ScriptWorldId.ApplicationWorld,
    user_world=QtWebEngineCore.QWebEngineScript.ScriptWorldId.UserWorld,
)


class WebEngineScript(QtWebEngineCore.QWebEngineScript):
    def set_injection_point(
        self, point: InjectionPointStr | QtWebEngineCore.QWebEngineScript.InjectionPoint
    ):
        """Set injection point.

        Args:
            point: injection point to use
        """
        self.setInjectionPoint(INJECTION_POINT.get_enum_value(point))

    def get_injection_point(self) -> InjectionPointStr:
        """Return injection point.

        Returns:
            injection point
        """
        return INJECTION_POINT.inverse[self.injectionPoint()]


if __name__ == "__main__":
    item = WebEngineScript()
