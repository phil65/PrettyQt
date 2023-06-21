from __future__ import annotations

from typing import TYPE_CHECKING, Any, SupportsIndex, TypeVar, Literal, overload

from collections.abc import Callable

from prettyqt.utils import helpers

if TYPE_CHECKING:
    from prettyqt.utils import fx

T = TypeVar("T")


class BaseListDelegator(list[T]):
    """Delegates method calls to all list members."""

    def __init__(self, *args, parent=None):
        self._parent = parent
        super().__init__(*args)

    @overload
    def __getitem__(self, index: str) -> BaseListDelegator[fx.AnimationWrapper]:
        ...

    @overload
    def __getitem__(self, index: slice) -> BaseListDelegator[T]:
        ...

    @overload
    def __getitem__(self, index: SupportsIndex) -> T:
        ...

    def __getitem__(
        self, index: str | SupportsIndex | slice
    ) -> BaseListDelegator[T] | T | BaseListDelegator[fx.AnimationWrapper]:
        match index:
            # for fx["prop"].
            # might be worth it to have delegators for the different classes
            # i.e. WidgetDelegator.
            case str():
                return BaseListDelegator(
                    [instance.__getitem__(index) for instance in self],
                    parent=self._parent,
                )
            case slice():
                return type(self)(super().__getitem__(index), parent=self._parent)
            case _:
                return super().__getitem__(index)

    @overload
    def __getattr__(self, method_name: Literal["fx"]) -> BaseListDelegator[fx.Fx]:
        ...

    @overload
    def __getattr__(self, method_name: str) -> Callable:
        ...

    def __getattr__(self, method_name: str) -> BaseListDelegator[fx.Fx] | Callable:
        # method_name = helpers.to_lower_camel(method_name)

        # TODO: should implement a general way to deal with properties.
        if method_name == "fx":
            return BaseListDelegator(
                [instance.fx for instance in self], parent=self._parent
            )

        def delegator(*args, **kwargs) -> list[Any]:
            results = []
            for instance in self:
                result = getattr(instance, method_name)(*args, **kwargs)
                results.append(result)
            return results

        return delegator


# class WidgetDelegator(BaseListDelegator[T]):
#     """Delegates method calls to all widgets of the list."""

#     def __init__(self, *args, parent=None):
#         self._parent = parent
#         super().__init__(*args)

#     @overload
#     def __getitem__(self, index: str) -> BaseListDelegator[fx.AnimationWrapper]:
#         ...

#     def __getitem__(
#         self, index: str | SupportsIndex | slice
#     ) -> BaseListDelegator[T] | T | BaseListDelegator[fx.AnimationWrapper]:
#         match index:
#             # for fx["prop"].
#             # might be worth it to have delegators for the different classes
#             # i.e. WidgetDelegator.
#             case str():
#                 return BaseListDelegator(
#                     [instance.__getitem__(index) for instance in self],
#                     parent=self._parent,
#                 )
#             case slice():
#                 return type(self)(super().__getitem__(index), parent=self._parent)
#             case _:
#                 return super().__getitem__(index)

#     @overload
#     def __getattr__(self, method_name: Literal["fx"]) -> BaseListDelegator[fx.Fx]:
#         ...

#     @overload
#     def __getattr__(self, method_name: str) -> Callable:
#         ...

#     def __getattr__(self, method_name: str) -> BaseListDelegator[fx.Fx] | Callable:
#         # method_name = helpers.to_lower_camel(method_name)

#         # TODO: should implement a general way to deal with properties.
#         if method_name == "fx":
#             return BaseListDelegator(
#                 [instance.fx for instance in self], parent=self._parent
#             )

#         return super().__getattr__(method_name)

# class SplitterDelegator(WidgetDelegator[T]):
#     ...


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
        app.exec()
