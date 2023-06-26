from __future__ import annotations

from typing import Literal

from typing_extensions import Self

from prettyqt.qt import QtWebEngineCore
from prettyqt.utils import bidict, datatypes


QWebEngineUrlScheme = QtWebEngineCore.QWebEngineUrlScheme

SyntaxStr = Literal["host_port_user_info", "host_port", "host", "path"]

SYNTAX: bidict[SyntaxStr, QWebEngineUrlScheme.Syntax] = bidict(
    host_port_user_info=QWebEngineUrlScheme.Syntax.HostPortAndUserInformation,
    host_port=QWebEngineUrlScheme.Syntax.HostAndPort,
    host=QWebEngineUrlScheme.Syntax.Host,
    path=QWebEngineUrlScheme.Syntax.Path,
)

FlagStr = Literal[
    "secure_scheme",
    "local_scheme",
    "local_access_allowed",
    "no_access_allowed",
    "service_workers_allowed",
    "view_source_allowed",
    "content_security_policy_ignored",
    "cors_enabled",
]

FLAGS: bidict[FlagStr, QWebEngineUrlScheme.Flag] = bidict(
    secure_scheme=QWebEngineUrlScheme.Flag.SecureScheme,
    local_scheme=QWebEngineUrlScheme.Flag.LocalScheme,
    local_access_allowed=QWebEngineUrlScheme.Flag.LocalAccessAllowed,
    no_access_allowed=QWebEngineUrlScheme.Flag.NoAccessAllowed,
    service_workers_allowed=QWebEngineUrlScheme.Flag.ServiceWorkersAllowed,
    view_source_allowed=QWebEngineUrlScheme.Flag.ViewSourceAllowed,
    content_security_policy_ignored=QWebEngineUrlScheme.Flag.ContentSecurityPolicyIgnored,
    cors_enabled=QWebEngineUrlScheme.Flag.CorsEnabled,
)


class WebEngineUrlScheme(QtWebEngineCore.QWebEngineUrlScheme):
    def get_name(self) -> str:
        return self.name().data().decode()

    @classmethod
    def get_scheme_by_name(cls, name: datatypes.ByteArrayType) -> Self:
        scheme = cls.schemeByName(datatypes.to_bytearray(name))
        return cls(scheme)

    def set_name(self, name: datatypes.ByteArrayType):
        self.setName(datatypes.to_bytearray(name))

    def set_syntax(self, syntax: SyntaxStr | QWebEngineUrlScheme.Syntax):
        """Set syntax.

        Args:
            syntax: syntax to use
        """
        self.setSyntax(SYNTAX.get_enum_value(syntax))

    def get_syntax(self) -> SyntaxStr:
        """Return syntax.

        Returns:
            syntax
        """
        return SYNTAX.inverse[self.syntax()]


if __name__ == "__main__":
    item = WebEngineUrlScheme()
