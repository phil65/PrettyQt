from __future__ import annotations

from typing import Literal

from qtpy import PYQT5, PYSIDE2, QtCore


if PYQT5:
    from PyQt5 import QtWebEngineCore  # type: ignore
elif PYSIDE2:
    from PySide2 import QtWebEngineCore

from prettyqt.utils import InvalidParamError, bidict


QWebEngineUrlScheme = QtWebEngineCore.QWebEngineUrlScheme

SYNTAX = bidict(
    host_port_user_info=QWebEngineUrlScheme.Syntax.HostPortAndUserInformation,
    host_port=QWebEngineUrlScheme.Syntax.HostAndPort,
    host=QWebEngineUrlScheme.Syntax.Host,
    path=QWebEngineUrlScheme.Syntax.Path,
)

SyntaxStr = Literal["host_port_user_info", "host_port", "host", "path"]

FLAGS = bidict(
    secure_scheme=QWebEngineUrlScheme.SecureScheme,
    local_scheme=QWebEngineUrlScheme.LocalScheme,
    local_access_allowed=QWebEngineUrlScheme.LocalAccessAllowed,
    no_access_allowed=QWebEngineUrlScheme.NoAccessAllowed,
    service_workers_allowed=QWebEngineUrlScheme.ServiceWorkersAllowed,
    view_source_allowed=QWebEngineUrlScheme.ViewSourceAllowed,
    content_security_policy_ignored=QWebEngineUrlScheme.ContentSecurityPolicyIgnored,
    cors_enabled=QWebEngineUrlScheme.CorsEnabled,
)


class WebEngineUrlScheme(QtWebEngineCore.QWebEngineUrlScheme):
    def get_name(self) -> str:
        return bytes(self.name()).decode()

    @classmethod
    def get_scheme_by_name(cls, name: str) -> WebEngineUrlScheme:
        scheme = cls.schemeByName(QtCore.QByteArray(name.encode()))
        return cls(scheme)

    def set_name(self, name: str):
        self.setName(QtCore.QByteArray(name.encode()))

    def set_syntax(self, syntax: SyntaxStr):
        """Set syntax.

        Args:
            syntax: syntax to use

        Raises:
            InvalidParamError: syntax does not exist
        """
        if syntax not in SYNTAX:
            raise InvalidParamError(syntax, SYNTAX)
        self.setSyntax(SYNTAX[syntax])

    def get_syntax(self) -> SyntaxStr:
        """Return syntax.

        Returns:
            syntax
        """
        return SYNTAX.inverse[self.syntax()]


if __name__ == "__main__":
    item = WebEngineUrlScheme()
