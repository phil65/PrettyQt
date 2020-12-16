from typing import Literal

from qtpy import QtCore

from prettyqt import core
from prettyqt.utils import InvalidParamError, bidict


EXIT_STATUS = bidict(normal=QtCore.QProcess.NormalExit, crash=QtCore.QProcess.CrashExit)

ExitStatusStr = Literal["normal", "crash"]

INPUT_CHANNEL_MODES = bidict(
    managed=QtCore.QProcess.ManagedInputChannel,
    forwarded=QtCore.QProcess.ForwardedInputChannel,
)

InputChannelModeStr = Literal["managed", "forwarded"]

PROCESS_CHANNELS = bidict(
    standard=QtCore.QProcess.StandardOutput, error=QtCore.QProcess.StandardError
)

ProcessChannelStr = Literal["standard", "error"]

PROCESS_CHANNEL_MODES = bidict(
    separate=QtCore.QProcess.SeparateChannels,
    merged=QtCore.QProcess.MergedChannels,
    forwarded=QtCore.QProcess.ForwardedChannels,
    forwarded_error=QtCore.QProcess.ForwardedErrorChannel,
    forwarded_output=QtCore.QProcess.ForwardedOutputChannel,
)

ProcessChannelModeStr = Literal[
    "separate", "merged", "forwarded", "forwarded_error", "forwarded_output"
]

PROCESS_ERRORS = bidict(
    failed_to_start=QtCore.QProcess.FailedToStart,
    crashed=QtCore.QProcess.Crashed,
    timed_out=QtCore.QProcess.Timedout,
    write=QtCore.QProcess.WriteError,
    read_error=QtCore.QProcess.ReadError,
    unknown_error=QtCore.QProcess.UnknownError,
)

ProcessErrorStr = Literal[
    "failed_to_start", "crashed", "timed_out", "write", "read_error", "unknown_error"
]

PROCESS_STATES = bidict(
    not_running=QtCore.QProcess.NotRunning,
    starting=QtCore.QProcess.Starting,
    running=QtCore.QProcess.Running,
)

ProcessStateStr = Literal["not_running", "starting", "running"]


QtCore.QProcess.__bases__ = (core.IODevice,)


class Process(QtCore.QProcess):
    def set_read_channel(self, channel: ProcessChannelStr):
        """Set the input channel channel.

        Args:
            channel: channel to set

        Raises:
            InvalidParamError: invalid channel
        """
        if channel not in PROCESS_CHANNELS:
            raise InvalidParamError(channel, PROCESS_CHANNELS)
        self.setReadChannel(PROCESS_CHANNELS[channel])

    def get_read_channel(self) -> ProcessChannelStr:
        return PROCESS_CHANNELS.inverse[self.readChannel()]

    def close_read_channel(self, channel: ProcessChannelStr):
        self.closeReadChannel(PROCESS_CHANNELS[channel])

    def set_input_channel_mode(self, mode: InputChannelModeStr):
        """Set the input channel mode.

        Args:
            mode: mode to set

        Raises:
            InvalidParamError: invalid mode
        """
        if mode not in INPUT_CHANNEL_MODES:
            raise InvalidParamError(mode, INPUT_CHANNEL_MODES)
        self.setInputChannelMode(INPUT_CHANNEL_MODES[mode])

    def get_input_channel_mode(self) -> InputChannelModeStr:
        return INPUT_CHANNEL_MODES.inverse[self.inputChannelMode()]

    def set_process_channel_mode(self, mode: ProcessChannelModeStr):
        """Set the process channel mode.

        Args:
            mode: mode to set

        Raises:
            InvalidParamError: invalid mode
        """
        if mode not in PROCESS_CHANNEL_MODES:
            raise InvalidParamError(mode, PROCESS_CHANNEL_MODES)
        self.setProcessChannelMode(PROCESS_CHANNEL_MODES[mode])

    def get_process_channel_mode(self) -> ProcessChannelModeStr:
        return PROCESS_CHANNEL_MODES.inverse[self.processChannelMode()]

    def set_state(self, state: ProcessStateStr):
        """Set the process state.

        Args:
            state: state to set

        Raises:
            InvalidParamError: invalid state
        """
        if state not in PROCESS_STATES:
            raise InvalidParamError(state, PROCESS_STATES)
        self.setProcessState(PROCESS_STATES[state])

    def get_state(self) -> ProcessStateStr:
        return PROCESS_STATES.inverse[self.state()]

    def get_error(self) -> ProcessErrorStr:
        return PROCESS_ERRORS.inverse[self.error()]

    def get_exit_status(self) -> ExitStatusStr:
        return EXIT_STATUS.inverse[self.exitStatus()]
