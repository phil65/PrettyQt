PrettyQt includes a large amount of ItemModels for Qt-based types, Python built-in types as well as for different data structures of external libraries.

* All models are proper views on data structures, not populated StandardItemModels.
* Boolean values are always handled via CheckState role, both for editing and displaying.
* Some of the models should be used in conjunction with the [EditorDelegate](editordelegate.md). That delegate supports editing a large amount of different datatypes and should be the
preferred choice for most models.
* In general, the models are unstyled (with some few exceptions. Styling should be done via the extensive [proxy system](proxies.md) which is baked into PrettyQt.

## Builtin-Type models


| Type | Model | Description |
|------|-------|-------------|
| `list[dict]` | [MappingModel](mappingmodel.md) | xyz
| `type, types.UnionType`  | [SubClassTreeModel](subclasstreemodel.md) | Tree showing all subclasses
| `type` | [ParentClassTreeModel](parentclasstreemodel.md) | Tree showing all Parent classes
| `importlib.metadata.distribution`| [ImportLibTreeModel](importlibtreemodel.md) | Tree model showing a dependency tree of given package
| `inspect.Traceback` | [FrameInfoModel](frameinfomodel.md) | Table model showing Traceback
| `inspect.FrameInfo` | [FrameInfoModel](frameinfomodel.md) | Table model showing FrameInfo
| `DataClass` | [DataclassFieldsModel](dataclassfieldsmodel.md) | Table showing all fields + metadata of a dataclass
| `Sequence[DataClass]` | [DataclassModel](dataclassmodel.md) | Table showing a list of dataclasses and their field values
| `ast.AST` | [AstModel](astmodel.md) | Tree model to show an abstract syntax tree
| `list[logging.LogRecord]` | [LogRecordModel](logrecordmodel.md) | Table showing a list of LogRecords
| `list[re.Match]` | [RegexMatchesModel](regexmatchesmodel.md) | Table do display list of regex matches
| `object`| [PythonObjectTreeModel](pythonobjecttreemodel.md) | Tree model showing all attributes of an object.
| `xml.etree.ElementTree, ElementTreeIterator` | [XmlModel](xmlmodel.md) | Tree view for an xml ElementTree
| `pkgutil.ModuleInfo, types.ModuleType` | [ModuleInfoModel](ModuleInfoModel.md) | Tree view to display a module hierarchy.

## Qt-Type models

| Type | Model | Description |
|------|-------|-------------|
| `list[QtGui.QAction]` | [ActionsModel](actionsmodel.md)| Table displaying all available info for a QAction. Supports editing QAction properties.
| `list[QtGui.QShortcut]` | [ShortcutsModel](shortcutsmodel.md) | Table displaying a list of shortcuts. Supports editing Shortcut properties.
| `list[QtCore.QStorageInfo]` | [StorageInfoModel](storageinfomodel.md) | Read-only list of available drives
| `list[QtWidgets.QWidget]` | xyz | Table displaying a list of QWidgets and their properties
| `list[QtCore.QModelIndex]` | [ModelIndexModel](modelindexmodel.md) | Model displaying all roles of a list of ModelIndexes.
| `QtCore.QObject` | xyz | Table model to display all available Properties of a QObject.

## External type models

| Type | Package | Model | Description |
|------|---------|-------|-------------|
| `AttrsDataclass` | [attrs](https://www.attrs.org/en/stable/) | [AttrsFieldsModel](attrsfieldsmodel.md) | Detail table containing all relevant information for each Attrs dataclass.
| `list[AttrsDataclass]`| [attrs](https://www.attrs.org/en/stable/) | [AttrsModel](attrsmodel.md) | Comparison view for a list of Pydantic models.
| `pydantic.BaseModel`| [pydantic](https://pydantic.dev) | [PydanticFieldsModel](pydanticfieldsmodel.md) | Table containing all relevant information for each BaseModel field.
| `list[pydantic.BaseModel]` | [pydantic](https://pydantic.dev) | [PydanticModel](pydanticmodel.md) | Comparison view for a list of Pydantic models.
| `fsspec.FileSystem` | [fsspec](https://filesystem-spec.readthedocs.io/en/latest/) | [FsSpecModel](fsspecmodel.md) | Model with same interface as QFileSystemModel
| `pandas.DataFrame` | [fsspec](https://filesystem-spec.readthedocs.io/en/latest/) | [PandasDataFrameModel](pandasdataframemodel.md) | Model to show a pandas DataFrame
| `pandas.Index` | [pandas](https://pandas.pydata.org) | [PandasIndexModel](pandasindexmodel.md) | Model to show a pandas (Multi)Index
| `polars.DataFrame` | [polars](https://www.pola.rs) | [PolarsDataFrameModel](polarsdataframemodel.md) | Model to display a polars DataFrame
| `git.Repo, git.Tree`| [gitpython](https://github.com/gitpython-developers/GitPython) | [GitPythonTreeModel](gitpythontreemodel.md) | Model to display a polars DataFrame
| `lxml.etree.Element, lxml.etree.iterparse` | [lxml](https://pypi.org/project/lxml/) | [LazyLxmlModel](lazylxmlmodel.md) | Tree view for an lxml iterparse iterator (lazy)
| `lxml.etree.ElementTree` | [lxml](https://pypi.org/project/lxml/) | [LxmlModel](lxmlmodel.md) | Tree view for an lxml ElementTree (full DOM)


