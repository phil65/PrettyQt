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



## Proxy Models

Every Class containing the AbstractItemViewMixin (widgets.TreeView, widgets.TableView, ...)
has quick access to proxy superpowers hidden behind the "proxifier" attribute.


Proxy models can be categorized


### Slice proxies

A lot of proxy models can be selectively applied by using python slicing syntax.
Each slice proxy can take an indexer and can be quickly set up via our proxifier.


Example:

``` py
    model = MyTableModel()
    table = widgets.TableView()
    table.set_model(model)

    # lets change the appearance a bit.
    # Set the font color of column 2 and 3 to red and font to Courier.

    table.proxifier[2:4, :].style(foreground="red", font="Courier")

    # Cut off last column and only show last 50 lines.
    table.proxifier[:-1, :50].filter()

    # Set first 20 lines of these 50 lines to read_only
    table.proxifier[:, :20].change_flags(editable=False)

    # Make first column checkable and trigger callback on checkstate change.
    table.proxifier[0, :].make_checkable(callback=my_callback)
```

Every call here basically adds another ProxyModel layer (all based on SliceIdentityProxyModel).
The proxy models should all perform very well with large tables since they never need to loop over the whole range.


Here is a short overview of the included slice proxies:


`SliceFilterProxyModel`
: ProxyModel which can filter columns and rows based on slices.
: Implemented as IdentityProxyModel instead of a FilterProxyModel
    in order to perform well with large tables.


`SliceAppearanceProxyModel`
: Applies styling to given slice by overriding font, color and alignment roles.


`CheckableProxyModel`
: Puts a checkbox into each cell and emits a signal containing the relevant index when any checkbox changes state.


`ChangeIconSizeProxymodel`
: Allows to change the size of the Icon / Pixmap shown for DecorationRole.
Changed icons / pixmaps are cached for performance reasons.


### Sort/Filter proxies.

In addition to the mentioned SliceFilterProxyModel, PrettyQt also contains
several proxies based on QSortFilterProxyModel. These can be more powerful
than our SliceFilterProxyModel, but scale with O(1) in respect to row / column count. (meaning that things might get slower for very large tables or when several proxies are layered on top of each other.)
Some of these proxies might partly overlap in functionality, but theres always a best one one for each use case to pick.


`FuzzyFilterProxyModel`
  : Model to make implementing CommandPalettes a la SubimeText or VS Code super easy.
  : A FilterProxyModel which sorts the results based on a matching score. Best matches are shown at the top.
  : Exposes matching score via a custom UserRole if desired.
  : Can also color the found Substring by converting the display role to an HTML representation when combined with our "HtmlItemDelegate", which allows to display HTML in ItemView cells.


`ValueFilterProxymodel`
: like the original QSortFilterProxyModel, but also works with non-str values.
: can be used for example to filter by checkstate role, or by any custom data behind any UserRole.
: The properties filterKeyColumn and filterRole of the base proxy model are taken into account.


`SubsetFilterProxyModel`
: Can filter rows / columns based on slices, index, a filter function, a list of indexes (like columns [0, 3, 7])

!!! note
    If you only need filtering based on slices or a single column / row,
    the SliceFilterProxymodel should be preferred for performance reasons.


`PredicateFilterProxyModel`
: The properties filterKeyColumn and filterRole of the base proxy model are taken into account.


`RangeFilterProxyModel`
: can filter numerical columns based on a min / max value.
: The properties filterKeyColumn and filterRole of the base proxy model are taken into account.


`MulticolumnFilterProxyModel`:
: can take a seperate search term / value for each column, thus avoiding to layer proxy models in case you want to filter based on several columns. That way it is less demanding since filtering for all columns is done in one go.
: used by our FilterHeader widget.



## Other Proxies

`ColorValuesProxyModel`
: Color cells based on their value (i.e. low numbers shown in green, high numbers shown in red.)
: To color cells, this proxy needs a minimum and maximum value. Three modes are available:
: Let the user choose a min max value.
: Use min max value from currently visible table section.
: use min max value from "seen" table content. (meaning that the model adapts min max values based.)

The last two modes have the advantage that nothing needs to be computed in advance, min/max values are calculated on-the fly.


`HighlightMouseProxymodel`
