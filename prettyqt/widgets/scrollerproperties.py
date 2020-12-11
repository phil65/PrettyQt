from typing import Any

from qtpy import QtWidgets

from prettyqt.utils import bidict, InvalidParamError

QScrollerProperties = QtWidgets.QScrollerProperties

FRAME_RATES = bidict(
    fps_60=QScrollerProperties.Fps60,
    fps_30=QScrollerProperties.Fps30,
    fps_20=QScrollerProperties.Fps20,
    standard=QScrollerProperties.Standard,
)

OVERSHOOT_POLICY = bidict(
    when_scrollable=QScrollerProperties.OvershootWhenScrollable,
    always_off=QScrollerProperties.OvershootAlwaysOff,
    always_on=QScrollerProperties.OvershootAlwaysOn,
)

SCROLL_METRIC = bidict(
    mouse_press_event_delay=QScrollerProperties.MousePressEventDelay,
    drag_start_distance=QScrollerProperties.DragStartDistance,
    drag_velocity_smoothing_factor=QScrollerProperties.DragVelocitySmoothingFactor,
    axis_lock_threshold=QScrollerProperties.AxisLockThreshold,
    scrolling_curve=QScrollerProperties.ScrollingCurve,
    deceleration_factor=QScrollerProperties.DecelerationFactor,
    minimum_velocity=QScrollerProperties.MinimumVelocity,
    maximum_velocity=QScrollerProperties.MaximumVelocity,
    maximum_click_through_velocity=QScrollerProperties.MaximumClickThroughVelocity,
    accelerating_flick_maximum_time=QScrollerProperties.AcceleratingFlickMaximumTime,
    accelerating_flick_speedup_factor=QScrollerProperties.AcceleratingFlickSpeedupFactor,
    snap_position_ratio=QScrollerProperties.SnapPositionRatio,
    snap_time=QScrollerProperties.SnapTime,
    overshoot_drag_resistance_factor=QScrollerProperties.OvershootDragResistanceFactor,
    overshoot_drag_distance_factor=QScrollerProperties.OvershootDragDistanceFactor,
    overshoot_scroll_distance_factor=QScrollerProperties.OvershootScrollDistanceFactor,
    overshoot_scroll_time=QScrollerProperties.OvershootScrollTime,
    horizontal_overshoot_policy=QScrollerProperties.HorizontalOvershootPolicy,
    vertical_overshoot_policy=QScrollerProperties.VerticalOvershootPolicy,
    frame_rate=QScrollerProperties.FrameRate,
    scroll_metric_count=QScrollerProperties.ScrollMetricCount,
)


class ScrollerProperties(QtWidgets.QScrollerProperties):
    def __getitem__(self, metric: str):
        return self.get_scroll_metric(metric)

    def __setitem__(self, metric: str, value: Any):
        self.set_scroll_metric(metric, value)

    def set_scroll_metric(self, metric: str, value: Any):
        """Set scroll metric.

        Possible values: "mouse_press_event_delay", "drag_start_distance",
                         "drag_velocity_smoothing_factor", "axis_lock_threshold",
                         "scrolling_curve", "deceleration_factor", "minimum_velocity",
                         "maximum_velocity", "maximum_click_through_velocity",
                         "accelerating_flick_maximum_time",
                         "accelerating_flick_speedup_factor", "snap_position_ratio",
                         "snap_time", "overshoot_drag_resistance_factor",
                         "overshoot_drag_distance_factor",
                         "overshoot_scroll_distance_factor", "overshoot_scroll_time",
                         "horizontal_overshoot_policy", "vertical_overshoot_policy",
                         "frame_rate", "scroll_metric_count"

        Args:
            metric: Scroll metric to set
            value: Value to set

        Raises:
            InvalidParamError: metric does not exist

        """
        if metric not in SCROLL_METRIC:
            raise InvalidParamError(metric, SCROLL_METRIC)
        self.setScrollMetric(SCROLL_METRIC[metric], value)

    def get_scroll_metric(self, metric: str) -> Any:
        """Return scroll metric.

        Possible values: "mouse_press_event_delay", "drag_start_distance",
                         "drag_velocity_smoothing_factor", "axis_lock_threshold",
                         "scrolling_curve", "deceleration_factor", "minimum_velocity",
                         "maximum_velocity", "maximum_click_through_velocity",
                         "accelerating_flick_maximum_time",
                         "accelerating_flick_speedup_factor", "snap_position_ratio",
                         "snap_time", "overshoot_drag_resistance_factor",
                         "overshoot_drag_distance_factor",
                         "overshoot_scroll_distance_factor", "overshoot_scroll_time",
                         "horizontal_overshoot_policy", "vertical_overshoot_policy",
                         "frame_rate", "scroll_metric_count"

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
