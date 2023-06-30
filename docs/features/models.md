Models
======

PrettyQt includes a range of models for Qt-based types, Python built-in types as well as
some models for data structures of external libraries.
All models are proper views on datastructures, not populated StandardItemModels.

### Builtin-Type models


| Type | Model | Description |
|------|-------|-------------|
| `list[dict]` | MappingModel | xyz
| `type, types.UnionType`  | SubClassModel | Tree showing all subclasses
| `type` | ParentClassModel | Tree showing all Parent classes
| `importlib.metadata.distribution`| ImportLibTreeModel | Tree model showing a dependency tree of given package
| `inspect.Traceback` | FrameInfoModel | Table model showing Traceback
| `inspect.FrameInfo` | FrameInfoModel | ""
| `DataClass` | DataclassFieldsModel | Table showing all fields + metadata of a dataclass
| `Sequence[DataClass]` | DataclassModel | Table showing a list of dataclasses and their field values
| `ast.AST` | AstModel | Tree model to show an abstract syntax tree
| `list[logging.LogRecord]` | LogRecordModel | Table showing a list of LogRecords
| `list[re.Match]` | RegexMatchesModel | Table do display list of regex matches
| `object`| xyz | Tree model showing all attributes of an object.
| `xml.etree.ElementTree` | XmlModel | Tree view for an xml ElementTree

### Qt-Type models

| Type | Model | Description |
|------|-------|-------------|
| `list[QtGui.QAction] | ActionsModel`| Table displaying all available info for a QAction. Supports editing QAction properties.
| `list[QtGui.QShortcut] | ShortcutsModel` | Table displaying a list of shortcuts. Supports editing Shortcut properties.
| `list[QtCore.QStorageInfo]` |StorageInfoModel | Read-only list of available drives
| `list[QtWidgets.QWidget]` | xyz | Table displaying a list of QWidgets and their properties
| `list[QtCore.QModelIndex]` | ModelIndexModel | Model displaying all roles of a list of ModelIndexes.
| `QtCore.QObject` | xyz | Table model to display all available Properties of a QObject.

### External type models

| Type | Model | Description |
|------|-------|-------------|
| `AttrsDataclass` | AttrsFieldsModel | Detail table containing all relevant information for each Attrs dataclass.
| `list[AttrsDataclass]`| AttrsModel | comparison view for a list of Pydantic models.
|`pydantic.BaseModel`| PydanticFieldsModel | Detail table containing all relevant information for each BaseModel field.
| `list[pydantic.BaseModel]` | PydanticModel | comparison view for a list of Pydantic models.
| `fsspec.FileSystem` | FsSpecModel | Model with same interface as QFileSystemModel
| `pandas.DataFrame` | PandasTableModel | Model to show a pandas DataFrame
| `pandas.Index` | PandasIndexModel | Model to show a pandas (Multi)Index
| `polars.DataFrame` | PolarsTableModel | Model to display a polars DataFrame


