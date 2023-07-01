PrettyQt includes a range of models for Qt-based types, Python built-in types as well as
some models for data structures of external libraries.
All models are proper views on datastructures, not populated StandardItemModels.

### Builtin-Type models


| Type | Model | Description |
|------|-------|-------------|
| `list[dict]` | MappingModel | xyz
| `type, types.UnionType`  | [SubClassTreeModel](subclasstreemodel.md) | Tree showing all subclasses
| `type` | [ParentClassTreeModel](parentclasstreemodel.md) | Tree showing all Parent classes
| `importlib.metadata.distribution`| ImportLibTreeModel | Tree model showing a dependency tree of given package
| `inspect.Traceback` | FrameInfoModel | Table model showing Traceback
| `inspect.FrameInfo` | FrameInfoModel | ""
| `DataClass` | [DataclassFieldsModel](dataclassfieldsmodel.md) | Table showing all fields + metadata of a dataclass
| `Sequence[DataClass]` | [DataclassModel](dataclassmodel.md) | Table showing a list of dataclasses and their field values
| `ast.AST` | AstModel | Tree model to show an abstract syntax tree
| `list[logging.LogRecord]` | LogRecordModel | Table showing a list of LogRecords
| `list[re.Match]` | RegexMatchesModel | Table do display list of regex matches
| `object`| xyz | Tree model showing all attributes of an object.
| `xml.etree.ElementTree` | XmlModel | Tree view for an xml ElementTree

### Qt-Type models

| Type | Model | Description |
|------|-------|-------------|
| `list[QtGui.QAction]` | [ActionsModel](actionsmodel.md)| Table displaying all available info for a QAction. Supports editing QAction properties.
| `list[QtGui.QShortcut]` | [ShortcutsModel](shortcutsmodel.md) | Table displaying a list of shortcuts. Supports editing Shortcut properties.
| `list[QtCore.QStorageInfo]` [StorageInfoModel](storageinfomodel.md) | Read-only list of available drives
| `list[QtWidgets.QWidget]` | xyz | Table displaying a list of QWidgets and their properties
| `list[QtCore.QModelIndex]` | [ModelIndexModel](modelindexmodel.md) | Model displaying all roles of a list of ModelIndexes.
| `QtCore.QObject` | xyz | Table model to display all available Properties of a QObject.

### External type models

| Type | Package | Model | Description |
|------|---------|-------|-------------|
| `AttrsDataclass` | attrs | [AttrsFieldsModel](attrsfieldsmodel.md) | Detail table containing all relevant information for each Attrs dataclass.
| `list[AttrsDataclass]`| attrs | [AttrsModel](attrsmodel.md) | comparison view for a list of Pydantic models.
|`pydantic.BaseModel`| pydantic | [PydanticFieldsModel](pydanticfieldsmodel.md) | Detail table containing all relevant information for each BaseModel field.
| `list[pydantic.BaseModel]` | pydantic | [PydanticModel](pydanticmodel.md) | comparison view for a list of Pydantic models.
| `fsspec.FileSystem` | fsspec | [FsSpecModel](fsspecmodel.md) | Model with same interface as QFileSystemModel
| `pandas.DataFrame` | fsspec | PandasTableModel | Model to show a pandas DataFrame
| `pandas.Index` | pandas | PandasIndexModel | Model to show a pandas (Multi)Index
| `polars.DataFrame` | polars | [PolarsTableModel](polarstablemodel.md) | Model to display a polars DataFrame
| `git.Repo`| gitpython | [GitPythonTreeModel](gitpythontreemodel.md) | Model to display a polars DataFrame
| `lxml.etree._Element` | lxml | Tree view for an xml ElementTree


