Every class containing the AbstractItemViewMixin (`widgets.TreeView`, `widgets.TableView`, ...)
has quick access to proxy superpowers hidden behind the "[proxifier](proxifier.md)" attribute.
The following section will give an overview about the included proxies and how to apply them.


## Slice proxies

{%
   include-markdown "sliceproxies.md"
%}


## Sort/Filter proxies.

{%
   include-markdown "sortfilterproxies.md"
%}


## Reshape / Styling proxies


{%
   include-markdown "reshapeproxies.md"
%}

## Other Proxies

| Proxy                                                  | Description                                          |
| -------------------------------------------------------|------------------------------------------------------|
|[HighlightMouseProxymodel](highlightmouseproxymodel.md) | Highlight regions the mouse cursor is hovering over. |



## Miscellaneous

| Class                  | Description                                                                            |
| -----------------------|----------------------------------------------------------------------------------------|
| [ProxyMapper](proxymapper.md)          | A helper for mapping indexes between proxies in any proxy tree.                        |
| [LinkedSelectionModel](linkedselectionmodel.md) | A SelectionModel which keeps indexes of any amount of proxies / source models in sync. |
| [ProxyComparerWidget](proxycomparerwidget.md)  | A widget to compare a proxy chain, useful for debugging.                               |
