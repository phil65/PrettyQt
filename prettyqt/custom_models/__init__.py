"""Custom_models module.

Contains custom models
"""

# BaseModels

from .selectionmixin import SelectionMixin
from .listmixin import ListMixin
from .treemodel import TreeModel
from .columnitemmodel import ColumnItemModel, ColumnTableModel, ColumnItem

# these are deprecated
from .modelmixin import ModelMixin
from .nesteditem import NestedItem
from .nestedmodel import NestedModel

# Python type models

from .regexmatchesmodel import RegexMatchesModel
from .importlibdistributionmodel import ImportlibDistributionModel
from .jsonmodel import JsonModel
from .astmodel import AstModel
from .classtreemodel import SubClassTreeModel, ParentClassTreeModel
from .frameinfomodel import FrameInfoModel
from .basefieldsmodel import BaseFieldsModel
from .basedataclassmodel import BaseDataclassModel
from .dataclassmodel import DataClassModel
from .dataclassfieldsmodel import DataClassFieldsModel
from .xmlmodel import XmlModel
from .mappingmodel import MappingModel
from .pythonobjecttreemodel import PythonObjectTreeModel

# Qt type models

from .actionsmodel import ActionsModel
from .modelindexmodel import ModelIndexModel
from .storageinfomodel import StorageInfoModel
from .shortcutsmodel import ShortcutsModel
from .widgetpropertiesmodel import WidgetPropertiesModel
from .widgetsdetailsmodel import WidgetsDetailsModel
from .widgethierarchymodel import WidgetHierarchyModel, LayoutHierarchyModel

# Proxies

from .sliceidentityproxymodel import SliceIdentityProxyModel
from .slicechangeiconsizeproxymodel import SliceChangeIconSizeProxyModel
from .slicefilterproxymodel import SliceFilterProxyModel
from .slicecheckableproxymodel import (
    SliceCheckableProxyModel,
    SliceCheckableTreeProxyModel,
)
from .sliceappearanceproxymodel import SliceAppearanceProxyModel
from .slicechangeflagsproxymodel import SliceChangeFlagsProxyModel
from .slicecolorvaluesproxymodel import SliceColorValuesProxyModel
from .slicevaluetransformationproxymodel import SliceValueTransformationProxyModel

from .fuzzyfiltermodel import FuzzyFilterProxyModel
from .multicolumnfilterproxymodel import MultiColumnFilterProxyModel
from .subsetfilterproxymodel import SubsetFilterProxyModel
from .valuefilterproxymodel import ValueFilterProxyModel
from .rangefilterproxymodel import RangeFilterProxyModel
from .tabletolistproxymodel import TableToListProxyModel
from .flattenedtreeproxymodel import FlattenedTreeProxyModel
from .appearanceproxymodel import AppearanceProxyModel
from .columnjoinerproxymodel import ColumnJoinerProxyModel
from .highlightcurrentproxymodel import HighlightCurrentProxyModel
from .highlightmouseproxymodel import HighlightMouseProxyModel

# Proxy tooling
from .proxymapper import ProxyMapper

__all__ = [
    "SelectionMixin",
    "TreeModel",
    "ImportlibDistributionModel",
    "ModelIndexModel",
    "RegexMatchesModel",
    "ColumnItemModel",
    "ColumnTableModel",
    "ListMixin",
    "ModelMixin",
    "ColumnItem",
    "NestedModel",
    "NestedItem",
    "JsonModel",
    "ActionsModel",
    "MappingModel",
    "PythonObjectTreeModel",
    "AstModel",
    "SubClassTreeModel",
    "ParentClassTreeModel",
    "FrameInfoModel",
    "BaseFieldsModel",
    "BaseDataclassModel",
    "DataClassModel",
    "StorageInfoModel",
    "ShortcutsModel",
    "DataClassFieldsModel",
    "XmlModel",
    "WidgetPropertiesModel",
    "WidgetHierarchyModel",
    "LayoutHierarchyModel",
    "WidgetsDetailsModel",
    "SliceChangeIconSizeProxyModel",
    "MultiColumnFilterProxyModel",
    "SliceIdentityProxyModel",
    "SliceFilterProxyModel",
    "FuzzyFilterProxyModel",
    "SubsetFilterProxyModel",
    "SliceValueTransformationProxyModel",
    "ValueFilterProxyModel",
    "RangeFilterProxyModel",
    "SliceCheckableProxyModel",
    "SliceCheckableTreeProxyModel",
    "TableToListProxyModel",
    "FlattenedTreeProxyModel",
    "SliceAppearanceProxyModel",
    "AppearanceProxyModel",
    "ColumnJoinerProxyModel",
    "SliceChangeFlagsProxyModel",
    "HighlightCurrentProxyModel",
    "SliceColorValuesProxyModel",
    "HighlightMouseProxyModel",
    "ProxyMapper",
]
