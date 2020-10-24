# -*- coding: utf-8 -*-

from qtpy import QtCore

from qtpy import PYQT5, PYSIDE2

if PYQT5:
    from PyQt5 import QtWebEngineCore  # type: ignore
elif PYSIDE2:
    from PySide2 import QtWebEngineCore

from prettyqt.utils import bidict, InvalidParamError

QWebEngineUrlScheme = QtWebEngineCore.QWebEngineUrlScheme

SYNTAX = bidict(
    host_port_user_info=QWebEngineUrlScheme.Syntax.HostPortAndUserInformation,
    host_port=QWebEngineUrlScheme.Syntax.HostAndPort,
    host=QWebEngineUrlScheme.Syntax.Host,
    path=QWebEngineUrlScheme.Syntax.Path,
)

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

    def get_scheme_by_name(self, name: str) -> "WebEngineUrlScheme":
        scheme = self.schemeByName(QtCore.QByteArray(name.encode()))
        return WebEngineUrlScheme(scheme)

    def set_name(self, name: str):
        self.setName(QtCore.QByteArray(name.encode()))

    def set_syntax(self, syntax: str):
        """Set syntax.

        Allowed values are "host_port_user_info", "host_port", "host", "path"

        Args:
            syntax: syntax to use

        Raises:
            InvalidParamError: syntax does not exist
        """
        if syntax not in SYNTAX:
            raise InvalidParamError(syntax, SYNTAX)
        self.setSyntax(SYNTAX[syntax])

    def get_syntax(self) -> str:
        """Return syntax.

        Possible values: "host_port_user_info", "host_port", "host", "path"

        Returns:
            syntax
        """
        return SYNTAX.inv[self.syntax()]


if __name__ == "__main__":
    item = WebEngineUrlScheme()
