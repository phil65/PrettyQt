from __future__ import annotations

import datetime
import logging

from prettyqt import constants, core, itemmodels


logger = logging.getLogger(__name__)


class SliceDisplayTextProxyModel(itemmodels.SliceIdentityProxyModel):
    """Proxy model to convert and format non-str values for the DisplayRole.

    Usually, formatting of numbers etc is done by the ItemDelegate.
    By moving the formatting into a proxy layer instead, we can keep the ItemDelegate
    spot free for other stuff.

    Information about string formatting:

    https://docs.python.org/3/library/string.html#format-specification-mini-language

    !!! note
        This is a slice proxy and can be selectively applied to a model.

    ### Example

    ```py
    model = MyModel()
    table = widgets.TableView()
    table.set_model(model)
    table[:, :3].proxify.format_text(int_format="{:0>2d}")
    table.show()
    # or
    indexer = (slice(None), slice(None, 3))
    proxy = SliceDisplayTextProxyModel(indexer=indexer, float_format="{:.4f}")
    proxy.set_source_model(model)
    table.set_model(proxy)
    table.show()
    ```
    """

    def __init__(self, *args, **kwargs):
        self._int_format = "{:.4f}"
        self._float_format = "{:.4f}"
        self._datetime_format = "%m/%d/%Y, %H:%M:%S"
        self._date_format = "%m/%d/%Y"
        self._time_format = "%H:%M:%S"
        # self._force_override = False
        super().__init__(*args, **kwargs)

    def data(
        self,
        index: core.ModelIndex,
        role: constants.ItemDataRole = constants.DISPLAY_ROLE,
    ):
        if not self.indexer_contains(index) or role != constants.DISPLAY_ROLE:
            return super().data(index, role)
        data = index.data()
        match data:
            case int():
                return self._int_format.format(data)
            case float():
                return self._float_format.format(data)
            case core.QDateTime():
                return data.toString(self._datetime_format)
            case datetime.datetime():
                return data.strftime(self._datetime_format)
            case core.QTime():
                return data.toString(self._time_format)
            case datetime.time():
                return data.strftime(self._time_format)
            case core.QDate():
                return data.toString(self._date_format)
            case datetime.date():
                return data.strftime(self._date_format)
            case _:
                return super().data(index, role)

    def set_int_format(self, fmt: str):
        self._int_format = fmt

    def get_int_format(self) -> str:
        return self._int_format

    def set_float_format(self, fmt: str):
        self._float_format = fmt

    def get_float_format(self) -> str:
        return self._float_format

    def set_datetime_format(self, fmt: str):
        self._datetime_format = fmt

    def get_datetime_format(self, fmt) -> str:
        return self._datetime_format

    def set_date_format(self, fmt: str):
        self._date_format = fmt

    def get_date_format(self, fmt) -> str:
        return self._date_format

    def set_time_format(self, fmt: str):
        self._time_format = fmt

    def get_time_format(self, fmt) -> str:
        return self._time_format

    int_format = core.Property(str, get_int_format, set_int_format)
    float_format = core.Property(str, get_float_format, set_float_format)
    datetime_format = core.Property(str, get_datetime_format, set_datetime_format)
    date_format = core.Property(str, get_date_format, set_date_format)
    time_format = core.Property(str, get_time_format, set_time_format)


if __name__ == "__main__":
    from prettyqt import debugging, widgets

    app = widgets.app()

    table = debugging.example_table()
    table.proxifier[1:4, :].set_format()
    table.show()
    with app.debug_mode():
        app.exec()
