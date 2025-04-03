"""Classes for integrating documentation into applications."""

from __future__ import annotations

from prettyqt.qt.QtHelp import *  # noqa: F403

from .helplink import HelpLink
from .helpindexmodel import HelpIndexModel
from .helpfilterdata import HelpFilterData
from .helpcontentitem import HelpContentItem
from .helpsearchresult import HelpSearchResult
from .helpcontentmodel import HelpContentModel
from .helpcontentwidget import HelpContentWidget
from .helpindexwidget import HelpIndexWidget
from .helpsearchresultwidget import HelpSearchResultWidget
from .helpsearchquerywidget import HelpSearchQueryWidget
from .helpfiltersettingswidget import HelpFilterSettingsWidget
from .helpenginecore import HelpEngineCore, HelpEngineCoreMixin
from .helpengine import HelpEngine
from .helpsearchengine import HelpSearchEngine
from .helpfilterengine import HelpFilterEngine
from prettyqt.qt import QtHelp

QT_MODULE = QtHelp

__all__ = [
    "HelpContentItem",
    "HelpContentModel",
    "HelpContentWidget",
    "HelpEngine",
    "HelpEngineCore",
    "HelpEngineCoreMixin",
    "HelpFilterData",
    "HelpFilterEngine",
    "HelpFilterSettingsWidget",
    "HelpIndexModel",
    "HelpIndexWidget",
    "HelpLink",
    "HelpSearchEngine",
    "HelpSearchQueryWidget",
    "HelpSearchResult",
    "HelpSearchResultWidget",
]
