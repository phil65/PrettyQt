## ScrollAreaTocWidget

A TreeView subclass which can show a Table-of-contents list based on a given ScrollArea.

With default settings, it will scan the widgets contained in the scrollArea for a windowTitle.
These widgets will be shown in the TreeView, and the TreeView selection will be synced to what is
currently visible in the ScrollArea.
This basically emulates the behaviour of many websites (like the [Qt Website][https://doc.qt.io/qt-6/supported-platforms.html]) or from VS code settings.

You can set up the Toc Tree by passing a ScrollArea instance:

```py
widget = widgets.Widget()
layout = widget.set_layout("horizontal")
scrollarea = widgets.ScrollArea()
# add some widgets to the ScrollArea here
# ...
toc = ScrollAreaTocWidget(scrollarea)
layout.add(toc)
layout.add(scrollarea)
```

The Toc tree can be configured to use other properties for populating than windowTitle.
You can also set a widget class filter if you only want a specific widget class to be shown.

The widget supports 3 different scroll modes:

1) Single: Only one row in the Tree will be highlighted. (the one which equals the topmost one from the scrollArea)
2) Multi: All rows which equal to visible widgets in the ScrollArea will be shown.
3) HeadersOnly: like Single, but only highlights top-level widgets from the ScrollArea.

There are also two different expand modes to choose from:

1) ExpandAll: All subsections are always expanded.
2) on_focus: Only the section containing the focused item is expanded.

This widget is used by [ConfigWidget][configwidget].

### Qt Properties

| Qt Property     | Type        | Description             |
| ----------------|-------------| ------------------------|
| **scroll_mode** | `Enum`      | Scroll mode (see above) |
| **expand_mode** | `Enum`      | Expand mode (see above) |
