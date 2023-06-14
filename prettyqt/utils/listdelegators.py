from __future__ import annotations

from prettyqt.utils import helpers


class BaseListDelegator(list):
    """Delegates method calls to all list members."""

    def __init__(self, *args, parent=None):
        self._parent = parent
        super().__init__(*args)

    def __getitem__(self, index):
        match index:
            # for fx["prop"]. Might be worth it to have a separate delegator for props.
            case str():
                return BaseListDelegator(
                    [instance.__getitem__(index) for instance in self],
                    parent=self._parent,
                )
            case slice():
                return type(self)(super().__getitem__(index), parent=self._parent)
            case _:
                return super().__getitem__(index)

    def __getattr__(self, method_name: str):
        # method_name = helpers.to_lower_camel(method_name)

        # TODO: should implement a general way to deal with properties.
        if method_name == "fx":
            return BaseListDelegator(
                [instance.fx for instance in self], parent=self._parent
            )

        def delegator(*args, **kwargs):
            results = []
            for instance in self:
                result = getattr(instance, method_name)(*args, **kwargs)
                results.append(result)
            return results

        return delegator


class SplitterDelegator(BaseListDelegator):
    """Delegates method calls to either the parent splitter or to all list members."""

    def __getattr__(self, method_name: str):
        method_name = helpers.to_lower_camel(method_name)
        if method_name in {
            "setCollapsible",
            "setStretchFactor",
            "getRange",
            "isCollapsible",
            "handle",
        }:

            def delegator(*args, **kwargs):
                results = []
                for instance in self:
                    idx = self._parent.indexOf(instance)
                    result = getattr(self._parent, method_name)(idx, *args, **kwargs)
                    results.append(result)
                return results

            return delegator
        return super().__getattr__(method_name)


if __name__ == "__main__":
    from prettyqt import widgets

    app = widgets.app()
    with app.debug_mode():
        w1 = widgets.RadioButton("test")
        w2 = widgets.RadioButton("test")
        w3 = widgets.RadioButton("test")
        w4 = widgets.RadioButton("test")
        widget = widgets.Widget()
        container = widget.set_layout("horizontal")
        container.add(w1)
        container.add(w2)
        container.add(w3)
        container.add(w4)
        # container[2].fx["pos"].transition_from((0, -100), duration=2000)
        widget.show()
        container[::2].fx.slide(end=(0, 100), duration=3000, reverse=True)
        app.main_loop()