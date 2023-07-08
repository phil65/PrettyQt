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
from .importlibdistributionmodel import ImportlibTreeModel
from .jsonmodel import JsonModel
from .astmodel import AstModel
from .classtreemodel import SubClassTreeModel, ParentClassTreeModel
from .frameinfomodel import FrameInfoModel
from .moduleinfomodel import ModuleInfoModel
from .basefieldsmodel import BaseFieldsModel
from .basedataclassmodel import BaseDataclassModel
from .dataclassmodel import DataClassModel
from .dataclassfieldsmodel import DataClassFieldsModel
from .logrecordmodel import LogRecordModel
from .xmlmodel import BaseXmlModel, XmlModel
from .mappingmodel import MappingModel
from .pythonobjecttreemodel import PythonObjectTreeModel

# Qt type models

from .actionsmodel import ActionsModel
from .modelindexmodel import ModelIndexModel
from .storageinfomodel import StorageInfoModel
from .shortcutsmodel import ShortcutsModel
from .qobjectpropertiesmodel import QObjectPropertiesModel
from .widgetsdetailsmodel import WidgetsDetailsModel
from .widgethierarchymodel import WidgetHierarchyModel, LayoutHierarchyModel

# Slice Proxies

from .proxies.sliceidentityproxymodel import SliceIdentityProxyModel
from .proxies.slicedisplaytextproxymodel import SliceDisplayTextProxyModel
from .proxies.slicechangeiconsizeproxymodel import SliceChangeIconSizeProxyModel
from .proxies.slicefilterproxymodel import SliceFilterProxyModel
from .proxies.slicecheckableproxymodel import (
    SliceCheckableProxyModel,
    SliceCheckableTreeProxyModel,
)
from .proxies.sliceappearanceproxymodel import SliceAppearanceProxyModel
from .proxies.slicechangeflagsproxymodel import SliceChangeFlagsProxyModel
from .proxies.slicecolorvaluesproxymodel import SliceColorValuesProxyModel
from .proxies.slicevaluetransformationproxymodel import SliceValueTransformationProxyModel
from .proxies.slicehighlightcurrentproxymodel import SliceHighlightCurrentProxyModel
from .proxies.slicemaproleproxymodel import SliceMapRoleProxyModel

# Reshape proxies

from .proxies.tabletolistproxymodel import TableToListProxyModel
from .proxies.flattentreeproxymodel import FlattenTreeProxyModel
from .proxies.meltproxymodel import MeltProxyModel
from .proxies.columnorderproxymodel import ColumnOrderProxyModel

# Other proxies
from .proxies.fuzzyfilterproxymodel import FuzzyFilterProxyModel
from .proxies.multicolumnfilterproxymodel import MultiColumnFilterProxyModel
from .proxies.subsetfilterproxymodel import SubsetFilterProxyModel
from .proxies.valuefilterproxymodel import ValueFilterProxyModel
from .proxies.rangefilterproxymodel import RangeFilterProxyModel
from .proxies.appearanceproxymodel import AppearanceProxyModel
from .proxies.changeheadersproxymodel import ChangeHeadersProxyModel
from .proxies.columnjoinerproxymodel import ColumnJoinerProxyModel
from .proxies.predicatefilterproxymodel import PredicateFilterProxyModel
from .proxies.highlightmouseproxymodel import HighlightMouseProxyModel

# Proxy tooling
from .proxies.proxymapper import ProxyMapper
from .proxies.linkedselectionmodel import LinkedSelectionModel

# Models for "external types"
# import importlib.util

# if importlib.util.find_spec("attrs") is not None:
#     from .attrsmodel import AttrsModel
#     from .attrsfieldsmodel import AttrsFieldsModel
# if importlib.util.find_spec("pydantic") is not None:
#     from .pydanticmodel import PydanticModel
#     from .pydanticfieldsmodel import PydanticFieldsModel

__all__ = [
    "SelectionMixin",
    "TreeModel",
    "ImportlibTreeModel",
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
    "LogRecordModel",
    "BaseXmlModel",
    "XmlModel",
    "QObjectPropertiesModel",
    "WidgetHierarchyModel",
    "LayoutHierarchyModel",
    "WidgetsDetailsModel",
    "SliceChangeIconSizeProxyModel",
    "MultiColumnFilterProxyModel",
    "SliceIdentityProxyModel",
    "SliceDisplayTextProxyModel",
    "SliceFilterProxyModel",
    "FuzzyFilterProxyModel",
    "SubsetFilterProxyModel",
    "SliceValueTransformationProxyModel",
    "ValueFilterProxyModel",
    "RangeFilterProxyModel",
    "SliceCheckableProxyModel",
    "SliceCheckableTreeProxyModel",
    "TableToListProxyModel",
    "FlattenTreeProxyModel",
    "MeltProxyModel",
    "ColumnOrderProxyModel",
    "SliceAppearanceProxyModel",
    "ChangeHeadersProxyModel",
    "AppearanceProxyModel",
    "ColumnJoinerProxyModel",
    "PredicateFilterProxyModel",
    "SliceChangeFlagsProxyModel",
    "SliceHighlightCurrentProxyModel",
    "SliceMapRoleProxyModel",
    "SliceColorValuesProxyModel",
    "HighlightMouseProxyModel",
    "ProxyMapper",
    "LinkedSelectionModel",
    # external
    # "AttrsModel",
    # "AttrsFieldsModel",
    # "PydanticModel",
    # "PydanticFieldsModel",
]
