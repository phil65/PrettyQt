from __future__ import annotations

from collections.abc import Iterator
from typing import Any, Literal

from prettyqt.qt import QtWidgets
from prettyqt.utils import bidict


mod = QtWidgets.QScrollerProperties

FrameRateStr = Literal["fps_60", "fps_30", "fps_20", "standard"]

FRAME_RATES: bidict[FrameRateStr, mod.FrameRates] = bidict(
    fps_60=mod.FrameRates.Fps60,
    fps_30=mod.FrameRates.Fps30,
    fps_20=mod.FrameRates.Fps20,
    standard=mod.FrameRates.Standard,
)

OvershootPolicyStr = Literal["when_scrollable", "always_off", "always_on"]

OVERSHOOT_POLICY: bidict[OvershootPolicyStr, mod.OvershootPolicy] = bidict(
    when_scrollable=mod.OvershootPolicy.OvershootWhenScrollable,
    always_off=mod.OvershootPolicy.OvershootAlwaysOff,
    always_on=mod.OvershootPolicy.OvershootAlwaysOn,
)

ScrollmetricStr = Literal[
    "mouse_press_event_delay",
    "drag_start_distance",
    "drag_velocity_smoothing_factor",
    "axis_lock_threshold",
    "scrolling_curve",
    "deceleration_factor",
    "minimum_velocity",
    "maximum_velocity",
    "maximum_click_through_velocity",
    "accelerating_flick_maximum_time",
    "accelerating_flick_speedup_factor",
    "snap_position_ratio",
    "snap_time",
    "overshoot_drag_resistance_factor",
    "overshoot_drag_distance_factor",
    "overshoot_scroll_distance_factor",
    "overshoot_scroll_time",
    "horizontal_overshoot_policy",
    "vertical_overshoot_policy",
    "frame_rate",
    "scroll_metric_count",
]

SCROLL_METRIC: bidict[ScrollmetricStr, mod.ScrollMetric] = bidict(
    mouse_press_event_delay=mod.ScrollMetric.MousePressEventDelay,
    drag_start_distance=mod.ScrollMetric.DragStartDistance,
    drag_velocity_smoothing_factor=mod.ScrollMetric.DragVelocitySmoothingFactor,
    axis_lock_threshold=mod.ScrollMetric.AxisLockThreshold,
    scrolling_curve=mod.ScrollMetric.ScrollingCurve,
    deceleration_factor=mod.ScrollMetric.DecelerationFactor,
    minimum_velocity=mod.ScrollMetric.MinimumVelocity,
    maximum_velocity=mod.ScrollMetric.MaximumVelocity,
    maximum_click_through_velocity=mod.ScrollMetric.MaximumClickThroughVelocity,
    accelerating_flick_maximum_time=mod.ScrollMetric.AcceleratingFlickMaximumTime,
    accelerating_flick_speedup_factor=mod.ScrollMetric.AcceleratingFlickSpeedupFactor,
    snap_position_ratio=mod.ScrollMetric.SnapPositionRatio,
    snap_time=mod.ScrollMetric.SnapTime,
    overshoot_drag_resistance_factor=mod.ScrollMetric.OvershootDragResistanceFactor,
    overshoot_drag_distance_factor=mod.ScrollMetric.OvershootDragDistanceFactor,
    overshoot_scroll_distance_factor=mod.ScrollMetric.OvershootScrollDistanceFactor,
    overshoot_scroll_time=mod.ScrollMetric.OvershootScrollTime,
    horizontal_overshoot_policy=mod.ScrollMetric.HorizontalOvershootPolicy,
    vertical_overshoot_policy=mod.ScrollMetric.VerticalOvershootPolicy,
    frame_rate=mod.ScrollMetric.FrameRate,
    scroll_metric_count=mod.ScrollMetric.ScrollMetricCount,
)


class ScrollerProperties(QtWidgets.QScrollerProperties):
    def __getitem__(self, metric: ScrollmetricStr | mod.ScrollMetric):
        return self.get_scroll_metric(metric)

    def __setitem__(self, metric: ScrollmetricStr | mod.ScrollMetric, value: Any):
        self.set_scroll_metric(metric, value)

    def keys(self) -> ScrollmetricStr:
        return SCROLL_METRIC.keys()

    def __iter__(self) -> Iterator[ScrollmetricStr]:
        return iter(SCROLL_METRIC.keys())

    def set_scroll_metric(self, metric: ScrollmetricStr | mod.ScrollMetric, value: Any):
        """Set scroll metric.

        Args:
            metric: Scroll metric to set
            value: Value to set
        """
        self.setScrollMetric(SCROLL_METRIC.get_enum_value(metric), value)

    def get_scroll_metric(self, metric: ScrollmetricStr | mod.ScrollMetric) -> Any:
        """Return scroll metric.

        Args:
            metric: Scroll metric to get

        Returns:
            state
        """
        return self.scrollMetric(SCROLL_METRIC.get_enum_value(metric))

    def get_scroll_metrics(self) -> dict[ScrollmetricStr, Any]:
        return {i: self.get_scroll_metric(i) for i in SCROLL_METRIC}


if __name__ == "__main__":
    props = ScrollerProperties()
