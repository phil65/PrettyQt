A large part of the library consists of a tree of mixins, with one mixin for each Qt class.
These mixins also inherit from each other and are applied to the Qt classes.
That way each class gets all helper methods from all sub-mixins.

Example: The class `TreeView` inherits from original Qt Class `QTreeView` and gets helper methods
from `TreeViewMxin`, `AbstractItemViewMixin`, `AbstractScrollAreaMixin`,
`FrameMixin`, `WidgetMixin` and `ObjectMixin`.

To illustrate this, we will use some of our included models:


!!! Example "Class hierarchy example"

    === "Subclass tree"

        ```py
        from prettyqt import itemmodels, widgets

        app = widgets.app()
        widget = widgets.TreeView()
        model = itemmodels.SubClassTreeModel(core.AbstractItemModelMixin)
        widget.set_model(model)
        widget.show()
        ```

        <figure markdown>
          ![Image title](images/abstractitemmodelmixin_subclasses.png)
          <figcaption>AbstractitemModelMixin subclasses</figcaption>
        </figure>

    === "Parentclass tree"

        ```py
        from prettyqt import itemmodels, widgets

        app = widgets.app()
        widget = widgets.TreeView()
        model = itemmodels.ParentClassTreeModel(widgets.TreeWidget)
        widget.set_model(model)
        widget.show()
        ```

        <figure markdown>
          ![Image title](images/treewidget_parentclasses.png)
          <figcaption>TreeWidget parent classes</figcaption>
        </figure>

    === "MRO tree"

        ```py
        from prettyqt import itemmodels, widgets

        app = widgets.app()
        widget = widgets.TreeView()
        model = itemmodels.ParentClassTreeModel(widgets.TreeWidget, mro=True)
        widget.set_model(model)
        widget.show()
        ```

        <figure markdown>
          ![Image title](images/treewidget_mro.png)
          <figcaption>TreeWidget MRO</figcaption>
        </figure>
