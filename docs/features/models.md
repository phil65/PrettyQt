Models
======

PrettyQt includes a range of models for Qt-based types, Python built-in types as well as
some models for data structures of external libraries.

## Models for following Python types are included:


list[dict]

type:
- Subclass tree
- ParentClass tree)

importlib.metadata.distribution:
- Dependency Tree

inspect.Traceback / inspect.FrameInfo:
- Stack table

DataClass | Sequence[DataClass]:
- 2 models: Sequence[dataclass] and dataclass)

ast.AST:
- Model for AST trees

list[logging.LogRecord]
- Table containing log information

list[re.Match]:
- Table do display list of regex matches

object
- Tree model showing all attributes of an instance.

xml.etree.ElementTree

## Models for following Qt types are included:

list[QtGui.QAction]
- Table displaying all available info for a QAction.

list[QtGui.QShortcut]

list[QtCore.QStorageInfo]

list[QtWidgets.QWidget]

list[QtCore.QModelIndex]

QtCore.QObject
- Table model to display all available Properties of a QObject.
- Works by inspecting the MetaObject of the QObjects.

## Models for following external libraries are included:

AttrsDataclass:
- Detail table containing all relevant information for each Attrs dataclass.
- If not frozen, values can be edited.

list[AttrsDataclass]:
- comparison view for a list of Pydantic models.
- Columns get automatically inferred based on most recent ancestor.
- If not frozen, values can be edited.

pydantic.BaseModel:
- Detail table containing all relevant information for each BaseModel field.
- If not frozen, values can be edited.

list[pydantic.BaseModel]:
- comparison view for a list of Pydantic models.
- Columns get automatically inferred based on most recent ancestor.
- If not frozen, values can be edited.

fsspec.FileSystem:
- One model with same interface as QFileSystemModel
- Can basically act as drop-in replacement
- Easy access to dropbox and all supported fsspec filesystems.

pd.DataFrame:
- Model to show complete table
- Model to show column categories
- Model for a detailed ColumnView
Scikit-learn



## Proxy Models

Every Class with an AbstractItemViewMixin (widgets.TreeView, widgets.TableView, ...)
has quick access to proxy superpowers hidden behind the "proxifier" attribute.
A lot of proxy models can be selectively applied by using python slicing syntax.

Example:

    model = MyTableModel()
    table = widgets.TableView()
    table.set_model(model)

    # lets change the appearance a bit.
    # Set the font color of column 2 and 3 to red and font to Courier.

    table.proxifier[2:4, :].style(foreground="red", font="Courier")

    # Cut off last column and only show last 50 lines.
    table.proxifier[:-1, :50].filter()

    # Set first 20 lines of these 50 lines to read_only
    table.proxifier[:, :20].set_read_only()

    # Make first column checkable and trigger callback on checkstate change.
    table.proxifier[0, :].make_checkable(callback=my_callback)


Every call here basically adds another ProxyModel layer (all based on SliceIdentityProxyModel).
The proxy models should all perform very well with large tables since they never need to loop over the whole range.


Here is a short overview for the included models:


FuzzyFilterProxyModel
  - Model to make implementing CommandPalettes a la SubimeText or VS Code super easy.
  - A FilterProxyModel which sorts the results based on a matching score.
  - Exposes matching score via a custom UserRole.
  - Can also color the found Substring when combined with our "HtmlItemDelegate".


SliceFilterProxyModel
  - ProxyModel which can filter columns and rows based on slices.
  - Implemented as IdentityProxyModel instead of a FilterProxyModel
    in order to perform well with large tables.


SliceAppearanceProxyModel
  - Applies styling to given slice by overriding font, color and alignment roles.





## Models for Qt Types


## Proxies

Every Model has a "proxifier" attribute which gives quick access to proxy models.



