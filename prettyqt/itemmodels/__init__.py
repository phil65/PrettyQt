"""Module containing ItemModels for common data structures.

PrettyQt includes a large amount of ItemModels for Qt-based types,
Python built-in types as well as for different data structures of external libraries.

* All models are proper views on data structures, not populated StandardItemModels.
* Boolean values are always handled via CheckState role, both for editing and displaying.
* Some of the models should be used in conjunction with the
[EditorDelegate](editordelegate.md). That delegate supports editing a large amount of
different datatypes and should be the
preferred choice for most models.
* In general, the models are unstyled (with some few exceptions.
Styling should be done via the extensive [proxy system](proxies.md)
which is baked into PrettyQt.

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
from .tupletreemodel import TupleTreeModel
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
from .proxies.slicecolorcategoriesproxymodel import SliceColorCategoriesProxyModel
from .proxies.slicevaluetransformationproxymodel import SliceValueTransformationProxyModel
from .proxies.slicehighlightcurrentproxymodel import SliceHighlightCurrentProxyModel
from .proxies.slicemaproleproxymodel import SliceMapRoleProxyModel
from .proxies.slicetomarkdownproxymodel import SliceToMarkdownProxyModel

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

# tooling
from .itemmodelresolver import ItemModelResolver
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
    "ActionsModel",
    "AppearanceProxyModel",
    "AstModel",
    "BaseDataclassModel",
    "BaseFieldsModel",
    "BaseXmlModel",
    "ChangeHeadersProxyModel",
    "ColumnItem",
    "ColumnItemModel",
    "ColumnJoinerProxyModel",
    "ColumnOrderProxyModel",
    "ColumnTableModel",
    "DataClassFieldsModel",
    "DataClassModel",
    "FlattenTreeProxyModel",
    "FrameInfoModel",
    "FuzzyFilterProxyModel",
    "HighlightMouseProxyModel",
    "ImportlibTreeModel",
    "ItemModelResolver",
    "JsonModel",
    "LayoutHierarchyModel",
    "LinkedSelectionModel",
    "ListMixin",
    "LogRecordModel",
    "MappingModel",
    "MeltProxyModel",
    "ModelIndexModel",
    "ModelMixin",
    "ModuleInfoModel",
    "MultiColumnFilterProxyModel",
    "NestedItem",
    "NestedModel",
    "ParentClassTreeModel",
    "PredicateFilterProxyModel",
    "ProxyMapper",
    "PythonObjectTreeModel",
    "QObjectPropertiesModel",
    "RangeFilterProxyModel",
    "RegexMatchesModel",
    "SelectionMixin",
    "ShortcutsModel",
    "SliceAppearanceProxyModel",
    "SliceChangeFlagsProxyModel",
    "SliceChangeIconSizeProxyModel",
    "SliceCheckableProxyModel",
    "SliceCheckableTreeProxyModel",
    "SliceColorCategoriesProxyModel",
    "SliceColorValuesProxyModel",
    "SliceDisplayTextProxyModel",
    "SliceFilterProxyModel",
    "SliceHighlightCurrentProxyModel",
    "SliceIdentityProxyModel",
    "SliceMapRoleProxyModel",
    "SliceToMarkdownProxyModel",
    "SliceValueTransformationProxyModel",
    "StorageInfoModel",
    "SubClassTreeModel",
    "SubsetFilterProxyModel",
    "TableToListProxyModel",
    "TreeModel",
    "TupleTreeModel",
    "ValueFilterProxyModel",
    "WidgetHierarchyModel",
    "WidgetsDetailsModel",
    "XmlModel",
    "attrsfieldsmodel",
    # external
    "attrsmodel",
    "fsspectreemodel",
    "pydanticfieldsmodel",
    "pydanticmodel",
]
