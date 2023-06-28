from __future__ import annotations

from typing import Literal

from prettyqt import constants, core, widgets
from prettyqt.utils import bidict


area = widgets.QAbstractScrollArea

SizeAdjustPolicyStr = Literal["content", "first_show", "ignored"]

SIZE_ADJUST_POLICY: bidict[SizeAdjustPolicyStr, area.SizeAdjustPolicy] = bidict(
    content=area.SizeAdjustPolicy.AdjustToContents,
    first_show=area.SizeAdjustPolicy.AdjustToContentsOnFirstShow,
    ignored=area.SizeAdjustPolicy.AdjustIgnored,
)


class AbstractScrollAreaMixin(widgets.FrameMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setHorizontalScrollBar(widgets.ScrollBar(parent=self))
        self.setVerticalScrollBar(widgets.ScrollBar(parent=self))

    def _get_map(self):
        maps = super()._get_map()
        maps |= {
            "horizontalScrollBarPolicy": constants.SCROLLBAR_POLICY,
            "sizeAdjustPolicy": SIZE_ADJUST_POLICY,
            "verticalScrollBarPolicy": constants.SCROLLBAR_POLICY,
        }
        return maps

    @property
    def h_scrollbar(self) -> widgets.ScrollBar:
        return self.horizontalScrollBar()

    @h_scrollbar.setter
    def h_scrollbar(self, scrollbar: widgets.ScrollBar):
        self.setHorizontalScrollBar(scrollbar)

    @property
    def v_scrollbar(self) -> widgets.ScrollBar:
        return self.verticalScrollBar()

    @v_scrollbar.setter
    def v_scrollbar(self, scrollbar: widgets.ScrollBar):
        self.setVerticalScrollBar(scrollbar)

    def scroll_by_pixels(self, x: int = 0, y: int = 0):
        new_x = self.h_scrollbar.value() + x
        x_val = max(min(new_x, self.h_scrollbar.maximum()), self.h_scrollbar.minimum())
        new_y = self.h_scrollbar.value() + y
        y_val = max(min(new_y, self.v_scrollbar.maximum()), self.v_scrollbar.minimum())
        self.h_scrollbar.setValue(x_val)
        self.v_scrollbar.setValue(y_val)

    def set_size_adjust_policy(self, policy: SizeAdjustPolicyStr | area.SizeAdjustPolicy):
        """Set size adjust policy.

        Args:
            policy: size adjust policy to use
        """
        self.setSizeAdjustPolicy(SIZE_ADJUST_POLICY.get_enum_value(policy))

    def get_size_adjust_policy(self) -> SizeAdjustPolicyStr:
        """Return size adjust policy.

        Returns:
            size adjust policy
        """
        return SIZE_ADJUST_POLICY.inverse[self.sizeAdjustPolicy()]

    def set_scrollbar_smooth(
        self,
        value: bool = True,
        animation_duration: int = 500,
        easing: core.easingcurve.TypeStr | core.QEasingCurve.Type = "out_cubic",
    ):
        if value:
            self.h_scrollbar = widgets.SmoothScrollBar(
                "horizontal",
                parent=self,
                animation_duration=animation_duration,
                easing=easing,
            )
            self.v_scrollbar = widgets.SmoothScrollBar(
                "vertical",
                parent=self,
                animation_duration=animation_duration,
                easing=easing,
            )
        else:
            self.h_scrollbar = widgets.ScrollBar(parent=self)
            self.v_scrollbar = widgets.ScrollBar(parent=self)

    def set_scrollbar_policy(
        self, mode: constants.ScrollBarPolicyStr | constants.ScrollBarPolicy
    ):
        """Set the policy for both scrollbars.

        Args:
            mode: visibilty to set
        """
        self.setHorizontalScrollBarPolicy(constants.SCROLLBAR_POLICY.get_enum_value(mode))
        self.setVerticalScrollBarPolicy(constants.SCROLLBAR_POLICY.get_enum_value(mode))

    def set_horizontal_scrollbar_policy(
        self, mode: constants.ScrollBarPolicyStr | constants.ScrollBarPolicy
    ):
        """Set the horizontal scrollbar visibility.

        Args:
            mode: visibilty to set
        """
        self.setHorizontalScrollBarPolicy(constants.SCROLLBAR_POLICY[mode])

    def get_horizontal_scrollbar_policy(self) -> constants.ScrollBarPolicyStr:
        return constants.SCROLLBAR_POLICY.inverse[self.horizontalScrollBarPolicy()]

    def set_vertical_scrollbar_policy(
        self, mode: constants.ScrollBarPolicyStr | constants.ScrollBarPolicy
    ):
        """Set the vertical scrollbar visibility.

        Args:
            mode: visibilty to set
        """
        self.setVerticalScrollBarPolicy(constants.SCROLLBAR_POLICY.get_enum_value(mode))

    def get_vertical_scrollbar_policy(self) -> constants.ScrollBarPolicyStr:
        return constants.SCROLLBAR_POLICY.inverse[self.verticalScrollBarPolicy()]

    def set_scrollbar_width(self, width: int):
        """Set the width for both scrollbars.

        Args:
            width: width in pixels
        """
        self.set_horizontal_scrollbar_width(width)
        self.set_vertical_scrollbar_width(width)

    def set_horizontal_scrollbar_width(self, width: int):
        """Set the horizontal scrollbar width.

        Args:
            width: width in pixels
        """
        with self.h_scrollbar.edit_stylesheet() as ss:
            ss.QScrollBar.horizontal.height.setValue(f"{width}px")

    def set_vertical_scrollbar_width(self, width: int):
        """Set the vertical scrollbar width.

        Args:
            width: width in pixels
        """
        with self.v_scrollbar.edit_stylesheet() as ss:
            ss.QScrollBar.horizontal.height.setValue(f"{width}px")

    def scroll_to_top(self):
        """Scroll to the top of the scroll area."""
        self.verticalScrollBar().scroll_to_min()

    def scroll_to_bottom(self):
        """Scroll to the bottom of the scroll area."""
        self.verticalScrollBar().scroll_to_max()

    def set_viewport_margins(self, margins: int):
        self.setViewportMargins(margins, margins, margins, margins)

    def add_scrollbar_widget(
        self,
        widget: widgets.QWidget,
        alignment: constants.AlignmentStr | constants.AlignmentFlag,
    ):
        alignment = constants.ALIGNMENTS.get_enum_value(alignment)
        self.addScrollBarWidget(widget, alignment)


class AbstractScrollArea(AbstractScrollAreaMixin, widgets.QAbstractScrollArea):
    pass


if __name__ == "__main__":
    app = widgets.app()
    widget = widgets.PlainTextEdit()
    widget.show()
    app.exec()
