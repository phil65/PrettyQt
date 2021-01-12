from __future__ import annotations

import functools
from typing import Callable, Dict, Iterable, List, Optional, Tuple, Union

from prettyqt import core
from prettyqt.prettyqtest.exceptions import TimeoutError
from prettyqt.qt import QtCore


class _AbstractSignalBlocker:
    """Base class for :class:`SignalBlocker` and :class:`MultiSignalBlocker`.

    Provides :meth:`wait` and a context manager protocol, but no means to add
    new signals and to detect when the signals should be considered "done".
    This needs to be implemented by subclasses.

    Subclasses also need to provide ``self._signals`` which should evaluate to
    ``False`` if no signals were configured.

    """

    def __init__(self, timeout: int = 1000, raising: bool = True):
        self._loop = core.EventLoop()
        self.timeout = timeout
        self.signal_triggered = False
        self.raising = raising
        # will be initialized by inheriting implementations
        self._signals: List[QtCore.Signal] = []
        self._timeout_message = ""
        if timeout is None or timeout == 0:
            self._timer = None
        else:
            self._timer = core.Timer(self._loop)
            self._timer.setSingleShot(True)
            self._timer.setInterval(timeout)

    def wait(self):
        """Wait until either a connected signal is triggered or timeout is reached.

        :raise ValueError: if no signals are connected and timeout is None; in
            this case it would wait forever.
        """
        __tracebackhide__ = True
        if self.signal_triggered:
            return
        if self.timeout is None and not self._signals:
            raise ValueError("No signals or timeout specified.")
        if self._timer is not None:
            self._timer.timeout.connect(self._quit_loop_by_timeout)
            self._timer.start()

        if self.timeout != 0:
            self._loop.exec_()

        if not self.signal_triggered and self.raising:
            raise TimeoutError(self._timeout_message)

    def _quit_loop_by_timeout(self):
        try:
            self._cleanup()
        finally:
            self._loop.quit()

    def _cleanup(self):
        # store timeout message before the data to construct it is lost
        self._timeout_message = self._get_timeout_error_message()
        if self._timer is not None:
            _silent_disconnect(self._timer.timeout, self._quit_loop_by_timeout)
            self._timer.stop()
            self._timer = None

    def _get_timeout_error_message(self):
        """Abstract, return an appropriate error message for a TimeoutError."""
        raise NotImplementedError  # pragma: no cover

    def _extract_pyqt_signal_name(self, potential_pyqt_signal):
        signal_name = potential_pyqt_signal.signal  # type: str
        if not isinstance(signal_name, str):
            raise TypeError(
                "Invalid 'signal' attribute in {}. "
                "Expected str but got {}".format(signal_name, type(signal_name))
            )
        # strip magic number "2" that PyQt prepends to the signal names
        signal_name = signal_name.lstrip("2")
        return signal_name

    def _extract_signal_from_signal_tuple(self, potential_signal_tuple):
        if isinstance(potential_signal_tuple, tuple):
            if len(potential_signal_tuple) != 2:
                raise ValueError(
                    "Signal tuple must have length of 2 (first element is the signal, "
                    "the second element is the signal's name)."
                )
            signal_tuple = potential_signal_tuple
            signal_name = signal_tuple[1]
            if not isinstance(signal_name, str):
                raise TypeError(
                    "Invalid type for provided signal name, "
                    "expected str but got {}".format(type(signal_name))
                )
            if not signal_name:
                raise ValueError("The provided signal name may not be empty")
            return signal_name
        return ""

    def determine_signal_name(self, potential_signal_tuple) -> str:
        """Attempts to determine the signal's name.

        If the user provided the signal name as 2nd value of the tuple, this
        name has preference. Bad values cause a ``ValueError``.
        Otherwise it attempts to get the signal from the ``signal`` attribute of
        ``signal`` (which only exists for PyQt signals).
        :returns: str name of the signal, an empty string if no signal name can be
        determined, or raises an error if the user provided an invalid signal name.
        """
        signal_name = self._extract_signal_from_signal_tuple(potential_signal_tuple)

        if not signal_name:
            try:
                signal_name = self._extract_pyqt_signal_name(potential_signal_tuple)
            except AttributeError:
                # not a PyQt signal
                # -> no signal name could be determined
                signal_name = ""

        return signal_name

    def get_callback_name(self, callback: Callable) -> str:
        """Attempt to extract the name of the callback. Return empty string on failure."""
        try:
            return callback.__name__
        except AttributeError:
            try:
                return callback.func.__name__  # type: ignore
                # e.g. for callbacks wrapped with functools.partial()
            except AttributeError:
                return ""

    @staticmethod
    def get_signal_from_potential_signal_tuple(
        signal_tuple: Union[QtCore.Signal, Tuple[QtCore.Signal, str]]
    ):
        if isinstance(signal_tuple, tuple):
            return signal_tuple[0]
        return signal_tuple

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        __tracebackhide__ = True
        if value is None:
            # only wait if no exception happened inside the "with" block
            self.wait()


class SignalBlocker(_AbstractSignalBlocker):
    """Returned by :meth:`pytestqt.qtbot.QtBot.waitSignal` method.

    :ivar int timeout: maximum time to wait for a signal to be triggered. Can
        be changed before :meth:`wait` is called.

    :ivar bool signal_triggered: set to ``True`` if a signal (or all signals in
        case of :class:`MultipleSignalBlocker`) was triggered, or
        ``False`` if timeout was reached instead. Until :meth:`wait` is called,
        this is set to ``None``.

    :ivar bool raising:
        If :class:`TimeoutError` should be raised if a timeout occurred.

        .. note:: contrary to the parameter of same name in
            :meth:`pytestqt.qtbot.QtBot.waitSignal`, this parameter does not
            consider the :ref:`qt_default_raising` option.

    :ivar list args:
        The arguments which were emitted by the signal, or None if the signal
        wasn't emitted at all.

    .. versionadded:: 1.10
       The *args* attribute.

    .. automethod:: wait
    .. automethod:: connect
    """

    def __init__(
        self,
        timeout: int = 1000,
        raising: bool = True,
        check_params_cb: Optional[Callable] = None,
    ):
        super().__init__(timeout, raising=raising)
        self._signals: List[QtCore.Signal] = []
        self.args: Optional[Iterable] = None
        self.all_args: List[tuple] = []
        self.check_params_callback = check_params_cb
        self.signal_name = ""

    def connect(self, signal: Union[QtCore.Signal, Tuple[QtCore.Signal, str]]):
        """Connect to given signal, making `wait()` return once this signal is emitted.

        More than one signal can be connected, in which case **any** one of
        them will make ``wait()`` return.

        :param signal: QtCore.Signal or tuple (QtCore.Signal, str)
        """
        self.signal_name = self.determine_signal_name(potential_signal_tuple=signal)
        actual_signal = self.get_signal_from_potential_signal_tuple(signal)
        actual_signal.connect(self._quit_loop_by_signal)
        self._signals.append(actual_signal)

    def _quit_loop_by_signal(self, *args):
        """Quit the event loop and marks that we finished because of a signal."""
        if self.check_params_callback:
            self.all_args.append(args)
            if not self.check_params_callback(*args):
                return  # parameter check did not pass
        try:
            self.signal_triggered = True
            self.args = list(args)
            self._cleanup()
        finally:
            self._loop.quit()

    def _cleanup(self):
        super()._cleanup()
        for signal in self._signals:
            _silent_disconnect(signal, self._quit_loop_by_signal)
        self._signals = []

    def get_params_as_str(self) -> str:
        if not self.all_args:
            return ""

        if len(self.all_args[0]) == 1:
            # we have a list of tuples with 1 element each (i.e. the signal has
            # 1 parameter), it doesn't make sense
            # to return something like "[(someParam,), (someParam,)]", it's just ugly.
            # Instead return something like "[someParam, someParam]"
            args_list = [arg[0] for arg in self.all_args]
        else:
            args_list = self.all_args

        return str(args_list)

    def _get_timeout_error_message(self) -> str:
        if self.check_params_callback is not None:
            param_str = self.get_params_as_str()
            return (
                f"Signal {self.signal_name} emitted with parameters {param_str} "
                f"within {self.timeout} ms, but did not satisfy "
                f"the {self.get_callback_name(self.check_params_callback)} callback"
            )
        else:
            return f"Signal {self.signal_name} not emitted after {self.timeout} ms"


class SignalAndArgs:
    def __init__(self, signal_name, args):
        self.signal_name = signal_name
        self.args = args

    def _get_readable_signal_with_optional_args(self) -> str:
        args = repr(self.args) if self.args else ""

        # remove signal parameter signature, e.g. turn "some_signal(str,int)" to
        # "some_signal", because we're adding
        # the actual parameters anyways
        signal_name = self.signal_name
        signal_name = signal_name.partition("(")[0]

        return signal_name + args

    def __str__(self):
        return self._get_readable_signal_with_optional_args()

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False


# Returns e.g. "3rd" for 3, or "21st" for 21
def get_ordinal_str(n) -> str:
    return "%d%s" % (n, {1: "st", 2: "nd", 3: "rd"}.get(n if n < 20 else n % 10, "th"))


class NoMatchingIndexFoundError(Exception):
    pass


class MultiSignalBlocker(_AbstractSignalBlocker):
    """Returned by :meth:`pytestqt.qtbot.QtBot.waitSignals` method.

    Blocks until all signals connected to it are triggered or the timeout is reached.

    Variables identical to :class:`SignalBlocker`:
        - ``timeout``
        - ``signal_triggered``
        - ``raising``

    .. automethod:: wait
    """

    def __init__(
        self,
        timeout: int = 1000,
        raising: bool = True,
        check_params_cbs=None,
        order="none",
    ):
        super().__init__(timeout, raising=raising)
        self._order = order
        self._check_params_callbacks = check_params_cbs
        self._signals_emitted: List[bool] = []
        # list of booleans, indicates whether the signal was already emitted
        self._signals_map: Dict[QtCore.Signal, List[int]] = {}
        # maps from a unique Signal to a list of indices where to expect signal emits
        self._signals: List[QtCore.Signal] = []
        # list of all Signals (for compatibility with _AbstractSignalBlocker)
        self._slots: List[Callable] = []  # list of slot functions
        self._signal_expected_index = 0  # only used when forcing order
        self._strict_order_violated = False
        self._actual_signal_and_args_at_violation: Optional[SignalAndArgs] = None
        self._signal_names: Dict[QtCore.Signal, str] = {}
        # maps from the unique Signal to the name of the signal (as string)
        self.all_signals_and_args: List[SignalAndArgs] = []  # SignalAndArgs instances

    def add_signals(self, signals):
        """Add the given signal to the list of signals which :meth:`wait()` waits for.

        :param list signals: list of QtCore.Signal`s or tuples (QtCore.Signal, str)
        """
        self._determine_unique_signals(signals)
        self._create_signal_emitted_indices(signals)
        self._connect_unique_signals()

    def _get_timeout_error_message(self) -> str:
        if not self._are_signal_names_available():
            return self._get_degenerate_error_message()
        error_message = self._get_expected_and_actual_signals_message()
        if self._strict_order_violated:
            error_message = self._get_order_violation_message() + error_message
        return error_message

    def _determine_unique_signals(self, signals):
        # create a map that maps from a unique signal to a list of indices
        # (positions) where this signal is expected (in case order matters)
        signals_as_str = [
            str(self.get_signal_from_potential_signal_tuple(signal)) for signal in signals
        ]
        # maps from a signal-string to one of the signal instances (the first one found)
        signal_str_to_unique_signal: Dict[str, QtCore.Signal] = {}
        for index, signal_str in enumerate(signals_as_str):
            signal = self.get_signal_from_potential_signal_tuple(signals[index])
            potential_tuple = signals[index]
            if signal_str not in signal_str_to_unique_signal:
                unique_signal_tuple = potential_tuple
                signal_str_to_unique_signal[signal_str] = signal
                self._signals_map[signal] = [index]  # create a new list
            else:
                # append to existing list
                unique_signal = signal_str_to_unique_signal[signal_str]
                self._signals_map[unique_signal].append(index)
                unique_signal_tuple = signals[index]

            self._determine_and_save_signal_name(unique_signal_tuple)

    def _determine_and_save_signal_name(self, unique_signal_tuple):
        signal_name = self.determine_signal_name(unique_signal_tuple)
        if signal_name:  # might be an empty string if no name could be determined
            unique_signal = self.get_signal_from_potential_signal_tuple(
                unique_signal_tuple
            )
            self._signal_names[unique_signal] = signal_name

    def _create_signal_emitted_indices(self, signals):
        for signal in signals:
            self._signals_emitted.append(False)

    def _connect_unique_signals(self):
        for unique_signal in self._signals_map:
            slot = functools.partial(self._unique_signal_emitted, unique_signal)
            self._slots.append(slot)
            unique_signal.connect(slot)
            self._signals.append(unique_signal)

    def _unique_signal_emitted(self, unique_signal, *args):
        """Called when a given signal is emitted.

        If all expected signals have been emitted, quits the event loop and
        marks that we finished because signals.
        """
        self._record_emitted_signal_if_possible(unique_signal, *args)

        self._check_signal_match(unique_signal, *args)

        if self._all_signals_emitted():
            self.signal_triggered = True
            try:
                self._cleanup()
            finally:
                self._loop.quit()

    def _record_emitted_signal_if_possible(self, unique_signal, *args):
        if self._are_signal_names_available():
            self.all_signals_and_args.append(
                SignalAndArgs(signal_name=self._signal_names[unique_signal], args=args)
            )

    def _check_signal_match(self, unique_signal, *args):
        if self._order == "none":
            # perform test for every matching index (stop after the first matching one)
            try:
                successful_index = self._get_first_matching_index(unique_signal, *args)
                self._signals_emitted[successful_index] = True
            except NoMatchingIndexFoundError:  # none found
                pass
        elif self._order == "simple":
            if self._check_signal_matches_expected_index(unique_signal, *args):
                self._signals_emitted[self._signal_expected_index] = True
                self._signal_expected_index += 1
        else:  # self.order == "strict"
            if not self._strict_order_violated:
                # only do the check if the strict order has not been violated yet
                # assume the order has been violated this time
                self._strict_order_violated = True
                if self._check_signal_matches_expected_index(unique_signal, *args):
                    self._signals_emitted[self._signal_expected_index] = True
                    self._signal_expected_index += 1
                    self._strict_order_violated = (
                        False  # order has not been violated after all!
                    )
                else:
                    if self._are_signal_names_available():
                        self._actual_signal_and_args_at_violation = SignalAndArgs(
                            signal_name=self._signal_names[unique_signal], args=args
                        )

    def _all_signals_emitted(self):
        return not self._strict_order_violated and all(self._signals_emitted)

    def _get_first_matching_index(self, unique_signal, *args):
        successfully_emitted = False
        successful_index = -1
        potential_indices = self._get_unemitted_signal_indices(unique_signal)
        for potential_index in potential_indices:
            if not self._violates_callback_at_index(potential_index, *args):
                successful_index = potential_index
                successfully_emitted = True
                break
        if not successfully_emitted:
            raise NoMatchingIndexFoundError

        return successful_index

    def _check_signal_matches_expected_index(self, unique_signal, *args):
        potential_indices = self._get_unemitted_signal_indices(unique_signal)
        if potential_indices:
            if self._signal_expected_index == potential_indices[0]:
                if not self._violates_callback_at_index(
                    self._signal_expected_index, *args
                ):
                    return True
        return False

    def _violates_callback_at_index(self, index, *args):
        """Check callback at the provided index that is violated due to invalid params.

        Returns False if there is no callback for that index, or if a callback exists
        but it wasn't violated (returned True). Returns True otherwise.
        """
        if self._check_params_callbacks:
            callback_func = self._check_params_callbacks[index]
            if callback_func:
                if not callback_func(*args):
                    return True
        return False

    def _get_unemitted_signal_indices(self, signal):
        """Return indices for provided signal for which NO signal has been emitted yet."""
        return [
            index
            for index in self._signals_map[signal]
            if not self._signals_emitted[index]
        ]

    def _are_signal_names_available(self) -> bool:
        return bool(self._signal_names)

    def _get_degenerate_error_message(self) -> str:
        received_signals = sum(self._signals_emitted)
        total_signals = len(self._signals_emitted)
        return (
            f"Received {received_signals} of the {total_signals} expected signals. "
            "To improve this error message, provide the names of the signals "
            "in the waitSignals() call."
        )

    def _get_expected_and_actual_signals_message(self) -> str:
        if not self.all_signals_and_args:
            emitted_signals = "None"
        else:
            emitted_signal_string_list = [str(_) for _ in self.all_signals_and_args]
            emitted_signals = self._format_as_array(emitted_signal_string_list)

        missing_signal_strings = []
        for missing_signal_index in self._get_missing_signal_indices():
            missing_signal_strings.append(
                self._get_signal_string_representation_for_index(missing_signal_index)
            )
        missing_signals = self._format_as_array(missing_signal_strings)

        return f"Emitted signals: {emitted_signals}. Missing: {missing_signals}"

    @staticmethod
    def _format_as_array(list_of_strings) -> str:
        return "[{}]".format(", ".join(list_of_strings))

    def _get_order_violation_message(self) -> str:
        expected_signal_as_str = self._get_signal_string_representation_for_index(
            self._signal_expected_index
        )
        actual_signal_as_str = str(self._actual_signal_and_args_at_violation)
        return (
            "Signal order violated! Expected {expected} as {ordinal} signal, "
            "but received {actual} instead. "
        ).format(
            expected=expected_signal_as_str,
            ordinal=get_ordinal_str(self._signal_expected_index + 1),
            actual=actual_signal_as_str,
        )

    def _get_missing_signal_indices(self) -> List[int]:
        return [
            index
            for index, value in enumerate(self._signals_emitted)
            if not self._signals_emitted[index]
        ]

    def _get_signal_string_representation_for_index(self, index: int) -> str:
        """Return something like <name_of_signal> (callback: <name_of_callback>)."""
        signal = self._get_signal_for_index(index)
        signal_str_repr = self._signal_names[signal]

        if self._check_params_callbacks:
            potential_callback = self._check_params_callbacks[index]
            if potential_callback:
                callback_name = self.get_callback_name(potential_callback)
                if callback_name:
                    signal_str_repr += f" (callback: {callback_name})"

        return signal_str_repr

    def _get_signal_for_index(self, index: int):
        for signal in self._signals_map:
            if index in self._signals_map[signal]:
                return signal

    def _cleanup(self):
        super()._cleanup()
        for i in range(len(self._signals)):
            signal = self._signals[i]
            slot = self._slots[i]
            _silent_disconnect(signal, slot)
        del self._signals_emitted[:]
        self._signals_map.clear()
        del self._slots[:]


class SignalEmittedSpy:
    """An object which checks if a given signal has ever been emitted.

    Intended to be used as a context manager.
    """

    def __init__(self, signal):
        self.signal = signal
        self.emitted = False
        self.args = None

    def slot(self, *args):
        self.emitted = True
        self.args = args

    def __enter__(self):
        self.signal.connect(self.slot)

    def __exit__(self, type, value, traceback):
        self.signal.disconnect(self.slot)

    def assert_not_emitted(self):
        if self.emitted:
            if self.args:
                raise SignalEmittedError(
                    "Signal %r unexpectedly emitted with "
                    "arguments %r" % (self.signal, list(self.args))
                )
            else:
                raise SignalEmittedError(f"Signal {self.signal!r} unexpectedly emitted")


class CallbackBlocker:
    """An object which checks if the returned callback gets called.

    Intended to be used as a context manager.

    :ivar int timeout: maximum time to wait for the callback to be called.

    :ivar bool raising:
        If :class:`TimeoutError` should be raised if a timeout occured.

        .. note:: contrary to the parameter of same name in
            :meth:`pytestqt.qtbot.QtBot.waitCallback`, this parameter does not
            consider the :ref:`qt_default_raising` option.

    :ivar list args:
        The arguments with which the callback was called, or None if the
        callback wasn't called at all.

    :ivar dict kwargs:
        The keyword arguments with which the callback was called, or None if
        the callback wasn't called at all.
    """

    def __init__(self, timeout: int = 1000, raising: bool = True):
        self.timeout = timeout
        self.raising = raising
        self.args: Optional[list] = None
        self.kwargs: Optional[dict] = None
        self.called = False
        self._loop = core.EventLoop()
        self._timer: Optional[core.Timer] = None
        if timeout is not None:
            self._timer = core.Timer(self._loop)
            self._timer.setSingleShot(True)
            self._timer.setInterval(timeout)

    def wait(self):
        """Wait until either the returned callback is called or timeout is reached."""
        __tracebackhide__ = True
        if self.called:
            return
        if self._timer is not None:
            self._timer.timeout.connect(self._quit_loop_by_timeout)
            self._timer.start()
        self._loop.exec_()
        if not self.called and self.raising:
            raise TimeoutError("Callback wasn't called after %sms." % self.timeout)

    def assert_called_with(self, *args, **kwargs):
        """Check that the callback was called with the same arguments as this function."""
        assert self.called
        assert self.args == list(args)
        assert self.kwargs == kwargs

    def _quit_loop_by_timeout(self):
        try:
            self._cleanup()
        finally:
            self._loop.quit()

    def _cleanup(self):
        if self._timer is not None:
            _silent_disconnect(self._timer.timeout, self._quit_loop_by_timeout)
            self._timer.stop()
            self._timer = None

    def __call__(self, *args, **kwargs):
        # Not inside the try: block, as if self.called is True, we did quit the
        # loop already.
        if self.called:
            raise CallbackCalledTwiceError("Callback called twice")
        try:
            self.args = list(args)
            self.kwargs = kwargs
            self.called = True
            self._cleanup()
        finally:
            self._loop.quit()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        __tracebackhide__ = True
        if value is None:
            # only wait if no exception happened inside the "with" block
            self.wait()


class SignalEmittedError(Exception):
    """Thrown by QtBot.assertNotEmitted` if a signal was emitted unexpectedly."""

    pass


class CallbackCalledTwiceError(Exception):
    """Thrown by QtBot.waitCallback if a callback was called twice."""

    pass


def _silent_disconnect(signal, slot):
    """Disconnect a signal from a slot, ignoring errors.

    Sometimes Qt might disconnect a signal automatically for unknown reasons.
    """
    try:
        signal.disconnect(slot)
    except (TypeError, RuntimeError):  # pragma: no cover
        pass
