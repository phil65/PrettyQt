from __future__ import annotations

from prettyqt.utils import helpers


class BaseListDelegator(list):
    """Delegates method calls to all list members."""

    def __init__(self, *args, parent=None):
        self._parent = parent
        super().__init__(*args)

    def __getattr__(self, method_name: str):
        method_name = helpers.to_lower_camel(method_name)

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
    w1 = widgets.RadioButton("test")
    w2 = widgets.RadioButton("test")
    container = widgets.Splitter()
    container.add(w1)
    container.add(w2)
    delegator = SplitterDelegator([w1, w2], parent=container)
    container.show()
    print(delegator.getRange())
    app.main_loop()
