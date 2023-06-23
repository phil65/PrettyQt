Models
======

PrettyQt includes a range of models for Qt-based types, Python built-in types as well as
some models for data structures of external libraries.

## Models for following Python types are included:


`list[dict]`

`type`:
: Subclass tree, ParentClass tree)

`importlib.metadata.distribution`:
: Tree model showing a dependency tree of given package

`inspect.Traceback / inspect.FrameInfo`:
: Stack table

`DataClass | Sequence[DataClass]`:
: 2 models: Sequence[dataclass] and dataclass)

`ast.AST`:
: Tree model to show an abstract syntax tree

`list[logging.LogRecord]`
: Table containing log information

`list[re.Match]`
: Table do display list of regex matches

`object`
: Tree model showing all attributes of an object.

`xml.etree.ElementTree -> custom_models.XmlModel`
: Tree view for an xml ElementTree

## Models for following Qt types are included:


`list[QtGui.QAction] -> custom_models.ActionsModel`
: Table displaying all available info for a QAction. Supports editing QAction properties.

`list[QtGui.QShortcut] -> custom_models.ShortcutsModel`
: Table displaying a list of shortcuts. Supports editing Shortcut properties.

`list[QtCore.QStorageInfo] -> custom_models.StorageInfoModel`
: Read-only list of available drives

`list[QtWidgets.QWidget]`
: Table displaying a list of QWidgets and their properties

`list[QtCore.QModelIndex] -> custom_models.ModelIndexModel`

`QtCore.QObject -> `
: Table model to display all available Properties of a QObject.
Works by inspecting the MetaObject of the QObjects.

## Models for following external libraries are included:

`AttrsDataclass`
: Detail table containing all relevant information for each Attrs dataclass.
: If not frozen, values can be edited.

`list[AttrsDataclass]`
: comparison view for a list of Pydantic models.
: Columns get automatically inferred based on most recent ancestor.
: If not frozen, values can be edited.

`pydantic.BaseModel`
: Detail table containing all relevant information for each BaseModel field.
: If not frozen, values can be edited.

`list[pydantic.BaseModel]`
: comparison view for a list of Pydantic models.
: Columns get automatically inferred based on most recent ancestor.
: If not frozen, values can be edited.

`fsspec.FileSystem`
: Model with same interface as QFileSystemModel
: Can basically act as drop:in replacement
: Easy access to dropbox and all supported fsspec filesystems.

`pd.DataFrame`
: Model to show complete table
: Model to show column categories
: Model for a detailed ColumnView

Scikit-learn

