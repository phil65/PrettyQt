"""Custom_models module.

Contains custom models
"""

from prettyqt import core
from .selectionmixin import SelectionMixin

if core.VersionNumber.get_qt_version() < (6, 0, 0):
    from .playlistmodel import PlaylistModel
from .transposeproxymodel import TransposeProxyModel
from .importlibdistributionmodel import ImportlibDistributionModel
from .regexmatchesmodel import RegexMatchesModel
from .columnitemmodel import ColumnItemModel, ColumnItem

__all__ = [
    "SelectionMixin",
    "TransposeProxyModel",
    "ImportlibDistributionModel",
    "PlaylistModel",
    "RegexMatchesModel",
    "ColumnItemModel",
    "ColumnItem",
]
