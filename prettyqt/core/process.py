# -*- coding: utf-8 -*-

from qtpy import QtCore

from prettyqt import core
from prettyqt.utils import bidict, InvalidParamError


EXIT_STATUS = bidict(normal=QtCore.QProcess.NormalExit, crash=QtCore.QProcess.CrashExit)

INPUT_CHANNEL_MODES = bidict(
    managed=QtCore.QProcess.ManagedInputChannel,
    forwarded=QtCore.QProcess.ForwardedInputChannel,
)

PROCESS_CHANNELS = bidict(
    standard=QtCore.QProcess.StandardOutput, error=QtCore.QProcess.StandardError
)

PROCESS_CHANNEL_MODES = bidict(
    separate=QtCore.QProcess.SeparateChannels,
    merged=QtCore.QProcess.MergedChannels,
    forwarded=QtCore.QProcess.ForwardedChannels,
    forwarded_error=QtCore.QProcess.ForwardedErrorChannel,
    forwarded_output=QtCore.QProcess.ForwardedOutputChannel,
)

PROCESS_ERRORS = bidict(
    failed_to_start=QtCore.QProcess.FailedToStart,
    crashed=QtCore.QProcess.Crashed,
    timed_out=QtCore.QProcess.Timedout,
    write=QtCore.QProcess.WriteError,
    read_error=QtCore.QProcess.ReadError,
    unknown_error=QtCore.QProcess.UnknownError,
)

PROCESS_STATES = bidict(
    not_running=QtCore.QProcess.NotRunning,
    starting=QtCore.QProcess.Starting,
    running=QtCore.QProcess.Running,
)


QtCore.QProcess.__bases__ = (core.IODevice,)


class Process(QtCore.QProcess):
    def set_read_channel(self, channel: str):
        """Set the input channel channel.

        possible values are "managed", "forwarded"

        Args:
            channel: channel to set

        Raises:
            InvalidParamError: invalid channel
        """
        if channel not in PROCESS_CHANNELS:
            raise InvalidParamError(channel, PROCESS_CHANNELS)
        self.setReadChannel(PROCESS_CHANNELS[channel])

    def get_read_channel(self) -> str:
        return PROCESS_CHANNELS.inv[self.readChannel()]

    def close_read_channel(self, channel: str):
        self.closeReadChannel(PROCESS_CHANNELS[channel])

    def set_input_channel_mode(self, mode: str):
        """Set the input channel mode.

        possible values are "managed", "forward"

        Args:
            mode: mode to set

        Raises:
            InvalidParamError: invalid mode
        """
        if mode not in INPUT_CHANNEL_MODES:
            raise InvalidParamError(mode, INPUT_CHANNEL_MODES)
        self.setInputChannelMode(INPUT_CHANNEL_MODES[mode])

    def get_input_channel_mode(self) -> str:
        return INPUT_CHANNEL_MODES.inv[self.inputChannelMode()]

    def set_process_channel_mode(self, mode: str):
        """Set the process channel mode.

        possible values are "separate", "merged", "forwarded", "forwarded_error",
        "forwarded_output"

        Args:
            mode: mode to set

        Raises:
            InvalidParamError: invalid mode
        """
        if mode not in PROCESS_CHANNEL_MODES:
            raise InvalidParamError(mode, PROCESS_CHANNEL_MODES)
        self.setProcessChannelMode(PROCESS_CHANNEL_MODES[mode])

    def get_process_channel_mode(self) -> str:
        return PROCESS_CHANNEL_MODES.inv[self.processChannelMode()]

    def set_state(self, state: str):
        """Set the process state.

        possible values are "not_running", "starting", "running"

        Args:
            state: state to set

        Raises:
            InvalidParamError: invalid state
        """
        if state not in PROCESS_STATES:
            raise InvalidParamError(state, PROCESS_STATES)
        self.setProcessState(PROCESS_STATES[state])

    def get_state(self) -> str:
        return PROCESS_STATES.inv[self.state()]

    def get_error(self) -> str:
        return PROCESS_ERRORS.inv[self.error()]

    def get_exit_status(self) -> str:
        return EXIT_STATUS.inv[self.exitStatus()]
