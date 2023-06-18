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
from .slicefilterproxymodel import SliceFilterProxyModel
from .fuzzyfiltermodel import FuzzyFilterProxyModel
from .subsetfilterproxymodel import SubsetFilterProxyModel
from .valuetransformationproxymodel import ValueTransformationProxyModel
from .valuefilterproxymodel import ValueFilterProxyModel
from .rangefilterproxymodel import RangeFilterProxyModel
from .checkableproxymodel import CheckableProxyModel
from .tabletolistproxymodel import TableToListProxyModel
from .flattenedtreeproxymodel import FlattenedTreeProxyModel
from .appearanceproxymodel import AppearanceProxyModel
from .sliceappearanceproxymodel import SliceAppearanceProxyModel
from .columnjoinerproxymodel import ColumnJoinerProxyModel
from .readonlyproxymodel import ReadOnlyProxyModel
from .highlightcurrentproxymodel import HighlightCurrentProxyModel
from .colorvaluesproxymodel import ColorValuesProxyModel
from .highlightmouseproxymodel import HighlightMouseProxyModel

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
    "SliceIdentityProxyModel",
    "SliceFilterProxyModel",
    "FuzzyFilterProxyModel",
    "SubsetFilterProxyModel",
    "ValueTransformationProxyModel",
    "ValueFilterProxyModel",
    "RangeFilterProxyModel",
    "CheckableProxyModel",
    "TableToListProxyModel",
    "FlattenedTreeProxyModel",
    "SliceAppearanceProxyModel",
    "AppearanceProxyModel",
    "ColumnJoinerProxyModel",
    "ReadOnlyProxyModel",
    "HighlightCurrentProxyModel",
    "ColorValuesProxyModel",
    "HighlightMouseProxyModel",
]
