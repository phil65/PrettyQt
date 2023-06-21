Pandas
======

Pandas is a very popular python library for working with tabular data.

PrettyQt contains a range of tools to work with pandas data structures.


## Models

PrettyQt includes multiple models to display Pandas dataframes.
One of the key "issues" is that in contrast to QAbstractTableModels, a pandas DataFrame can have MultiIndexes.
PrettyQt offers several approaches to display these MultiIndexes.

DataTableWithHeaderModel is a very simple model which is displaying MultiIndexes by joining
the multiple index levels using a separator. (the separator value is exposed as a Qt Property)

In addition, two composed widgets are included which consist of three different tables (one for data, one for the index, one for the headers) which are synced on scrolling / resizing.

There is also a model to get a detailed view on an index and another one to display the categories of
a pandas category column.


## Proxies
Since working with pandas often means working with tables containing several hundred thousands of rows,
the default QSortFilterProxyModel does not work that well.

PrettyQt includes several proxy models which try to improve this.

PandasStringColumnFilterModel can be used to filter a column based on a search string.
Instead of looping over the cells, a filter index is built using NumPy operations.
This makes filtering super fast, even with several thousands of rows.

PandasEvalFilterModel works in a similar way, but filtering is done by a Python statement.
(example: '"a" > 10' would show all rows where the value of column "a" is greater than 10.)

To display heatmaps, PrettyQt also includes a proxy model to color the cells according to their values.
That proxy model includes several modes, also including modes which dont need to pre-compute min-max values,


## EventFilters
To prettify the mentioned composed widgets, an EventFilter is included which sets row / column spans
on-the-fly.


## Scikit-learn

Lastly, there are also models included to display Scikit-Learn estimators and their characteristics.

