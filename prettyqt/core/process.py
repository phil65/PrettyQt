from __future__ import annotations

import contextlib
from typing import Literal

from prettyqt import core
from prettyqt.qt import QtCore
from prettyqt.utils import bidict


ExitStatusStr = Literal["normal", "crash"]

EXIT_STATUS: bidict[ExitStatusStr, QtCore.QProcess.ExitStatus] = bidict(
    normal=QtCore.QProcess.ExitStatus.NormalExit,
    crash=QtCore.QProcess.ExitStatus.CrashExit,
)

InputChannelModeStr = Literal["managed", "forwarded"]

INPUT_CHANNEL_MODES: bidict[
    InputChannelModeStr, QtCore.QProcess.InputChannelMode
] = bidict(
    managed=QtCore.QProcess.InputChannelMode.ManagedInputChannel,
    forwarded=QtCore.QProcess.InputChannelMode.ForwardedInputChannel,
)

ProcessChannelStr = Literal["standard", "error"]

PROCESS_CHANNELS: bidict[ProcessChannelStr, QtCore.QProcess.ProcessChannel] = bidict(
    standard=QtCore.QProcess.ProcessChannel.StandardOutput,
    error=QtCore.QProcess.ProcessChannel.StandardError,
)

ProcessChannelModeStr = Literal[
    "separate", "merged", "forwarded", "forwarded_error", "forwarded_output"
]

PROCESS_CHANNEL_MODES: bidict[
    ProcessChannelModeStr, QtCore.QProcess.ProcessChannelMode
] = bidict(
    separate=QtCore.QProcess.ProcessChannelMode.SeparateChannels,
    merged=QtCore.QProcess.ProcessChannelMode.MergedChannels,
    forwarded=QtCore.QProcess.ProcessChannelMode.ForwardedChannels,
    forwarded_error=QtCore.QProcess.ProcessChannelMode.ForwardedErrorChannel,
    forwarded_output=QtCore.QProcess.ProcessChannelMode.ForwardedOutputChannel,
)

ProcessErrorStr = Literal[
    "failed_to_start", "crashed", "timed_out", "write", "read_error", "unknown_error"
]

PROCESS_ERRORS: bidict[ProcessErrorStr, QtCore.QProcess.ProcessError] = bidict(
    failed_to_start=QtCore.QProcess.ProcessError.FailedToStart,
    crashed=QtCore.QProcess.ProcessError.Crashed,
    timed_out=QtCore.QProcess.ProcessError.Timedout,
    write=QtCore.QProcess.ProcessError.WriteError,
    read_error=QtCore.QProcess.ProcessError.ReadError,
    unknown_error=QtCore.QProcess.ProcessError.UnknownError,
)


ProcessStateStr = Literal["not_running", "starting", "running"]

PROCESS_STATES: bidict[ProcessStateStr, QtCore.QProcess.ProcessState] = bidict(
    not_running=QtCore.QProcess.ProcessState.NotRunning,
    starting=QtCore.QProcess.ProcessState.Starting,
    running=QtCore.QProcess.ProcessState.Running,
)


class Process(core.IODeviceMixin, QtCore.QProcess):
    def set_read_channel(
        self, channel: ProcessChannelStr | QtCore.QProcess.ProcessChannelMode
    ):
        """Set the input channel channel.

        Args:
            channel: channel to set
        """
        self.setReadChannel(PROCESS_CHANNELS.get_enum_value(channel))

    def get_read_channel(self) -> ProcessChannelStr:
        return PROCESS_CHANNELS.inverse[self.readChannel()]

    def close_read_channel(self, channel: ProcessChannelStr):
        self.closeReadChannel(PROCESS_CHANNELS[channel])

    def set_input_channel_mode(
        self, mode: InputChannelModeStr | QtCore.QProcess.InputChannelMode
    ):
        """Set the input channel mode.

        Args:
            mode: mode to set
        """
        self.setInputChannelMode(INPUT_CHANNEL_MODES.get_enum_value(mode))

    def get_input_channel_mode(self) -> InputChannelModeStr:
        return INPUT_CHANNEL_MODES.inverse[self.inputChannelMode()]

    def set_process_channel_mode(
        self, mode: ProcessChannelModeStr | QtCore.QProcess.ProcessChannelMode
    ):
        """Set the process channel mode.

        Args:
            mode: mode to set
        """
        self.setProcessChannelMode(PROCESS_CHANNEL_MODES.get_enum_value(mode))

    def get_process_channel_mode(self) -> ProcessChannelModeStr:
        return PROCESS_CHANNEL_MODES.inverse[self.processChannelMode()]

    def set_state(self, state: ProcessStateStr | QtCore.QProcess.ProcessState):
        """Set the process state.

        Args:
            state: state to set
        """
        self.setProcessState(PROCESS_STATES.get_enum_value(state))

    def get_state(self) -> ProcessStateStr:
        return PROCESS_STATES.inverse[self.state()]

    def get_error(self) -> ProcessErrorStr:
        return PROCESS_ERRORS.inverse[self.error()]

    def get_exit_status(self) -> ExitStatusStr:
        return EXIT_STATUS.inverse[self.exitStatus()]

    def get_process_environment(self) -> core.ProcessEnvironment:
        return core.ProcessEnvironment(self.processEnvironment())

    @contextlib.contextmanager
    def edit_process_environment(self):
        env = self.get_process_environment()
        yield env
        self.setProcessEnvironment(env)


if __name__ == "__main__":
    process = core.Process()
    env = process.get_process_environment()
    print(env.items())
