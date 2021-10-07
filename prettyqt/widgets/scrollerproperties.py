from __future__ import annotations

from typing import Any, Literal

from prettyqt.qt import QtWidgets
from prettyqt.utils import InvalidParamError, bidict


mod = QtWidgets.QScrollerProperties

FRAME_RATES = bidict(
    fps_60=mod.FrameRates.Fps60,
    fps_30=mod.FrameRates.Fps30,
    fps_20=mod.FrameRates.Fps20,
    standard=mod.FrameRates.Standard,
)

FrameRateStr = Literal["fps_60", "fps_30", "fps_20", "standard"]

OVERSHOOT_POLICY = bidict(
    when_scrollable=mod.OvershootPolicy.OvershootWhenScrollable,
    always_off=mod.OvershootPolicy.OvershootAlwaysOff,
    always_on=mod.OvershootPolicy.OvershootAlwaysOn,
)

OvershootPolicyStr = Literal["when_scrollable", "always_off", "always_on"]

SCROLL_METRIC = bidict(
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


class ScrollerProperties(QtWidgets.QScrollerProperties):
    def __getitem__(self, metric: ScrollmetricStr):
        return self.get_scroll_metric(metric)

    def __setitem__(self, metric: ScrollmetricStr, value: Any):
        self.set_scroll_metric(metric, value)

    def set_scroll_metric(self, metric: ScrollmetricStr, value: Any):
        """Set scroll metric.

        Args:
            metric: Scroll metric to set
            value: Value to set

        Raises:
            InvalidParamError: metric does not exist

        """
        if metric not in SCROLL_METRIC:
            raise InvalidParamError(metric, SCROLL_METRIC)
        self.setScrollMetric(SCROLL_METRIC[metric], value)

    def get_scroll_metric(self, metric: ScrollmetricStr) -> Any:
        """Return scroll metric.

        Args:
            metric: Scroll metric to get

        Raises:
            InvalidParamError: metric does not exist

        Returns:
            state
        """
        if metric not in SCROLL_METRIC:
            raise InvalidParamError(metric, SCROLL_METRIC)
        return self.scrollMetric(SCROLL_METRIC[metric])
