"""qthelp module.

contains QtHelp-based classes
"""

from .helpindexmodel import HelpIndexModel
from .helpcontentitem import HelpContentItem
from .helpsearchresult import HelpSearchResult
from .helpcontentmodel import HelpContentModel
from .helpcontentwidget import HelpContentWidget
from .helpindexwidget import HelpIndexWidget
from .helpsearchresultwidget import HelpSearchResultWidget
from .helpsearchquerywidget import HelpSearchQueryWidget
from .helpenginecore import HelpEngineCore
from .helpengine import HelpEngine
from .helpsearchengine import HelpSearchEngine

from prettyqt import core

if core.VersionNumber.get_qt_version() >= (5, 13, 0):
    from .helpfilterengine import HelpFilterEngine

__all__ = [
    "HelpIndexModel",
    "HelpContentItem",
    "HelpSearchResult",
    "HelpContentModel",
    "HelpContentWidget",
    "HelpIndexWidget",
    "HelpSearchEngine",
    "HelpSearchResultWidget",
    "HelpSearchQueryWidget",
    "HelpFilterEngine",
    "HelpEngineCore",
    "HelpEngine",
]
