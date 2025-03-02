"""Provides classes / tools for creating and embedding state machines from SCXML files."""

from __future__ import annotations

from prettyqt.qt.QtScxml import *  # noqa: F403

from .scxmlcompiler import ScxmlCompiler
from scxmlstatemachine import ScxmlStateMachine
from .scxmldatamodel import ScXmlDataModel
from .scxmlcppdatamodel import ScXmlCppDataModel
from .scxmlnulldatamodel import ScXmlNullDataModel
from .scxmlinvokableservice import ScXmlInvokableService
from .scxmlinvokableservicefactory import ScXmlInvokableServiceFactory
from prettyqt.qt import QtScxml

QT_MODULE = QtScxml

__all__ = [
    "ScXmlCppDataModel",
    "ScXmlDataModel",
    "ScXmlInvokableService",
    "ScXmlInvokableServiceFactory",
    "ScXmlNullDataModel",
    "ScxmlCompiler",
    "ScxmlStateMachine",
]
