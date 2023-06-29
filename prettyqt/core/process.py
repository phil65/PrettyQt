from __future__ import annotations

import contextlib
from typing import Literal

from prettyqt import core
from prettyqt.utils import bidict


ExitStatusStr = Literal["normal", "crash"]

EXIT_STATUS: bidict[ExitStatusStr, core.QProcess.ExitStatus] = bidict(
    normal=core.QProcess.ExitStatus.NormalExit,
    crash=core.QProcess.ExitStatus.CrashExit,
)

InputChannelModeStr = Literal["managed", "forwarded"]

INPUT_CHANNEL_MODES: bidict[InputChannelModeStr, core.QProcess.InputChannelMode] = bidict(
    managed=core.QProcess.InputChannelMode.ManagedInputChannel,
    forwarded=core.QProcess.InputChannelMode.ForwardedInputChannel,
)

ProcessChannelStr = Literal["standard", "error"]

PROCESS_CHANNELS: bidict[ProcessChannelStr, core.QProcess.ProcessChannel] = bidict(
    standard=core.QProcess.ProcessChannel.StandardOutput,
    error=core.QProcess.ProcessChannel.StandardError,
)

ProcessChannelModeStr = Literal[
    "separate", "merged", "forwarded", "forwarded_error", "forwarded_output"
]

PROCESS_CHANNEL_MODES: bidict[
    ProcessChannelModeStr, core.QProcess.ProcessChannelMode
] = bidict(
    separate=core.QProcess.ProcessChannelMode.SeparateChannels,
    merged=core.QProcess.ProcessChannelMode.MergedChannels,
    forwarded=core.QProcess.ProcessChannelMode.ForwardedChannels,
    forwarded_error=core.QProcess.ProcessChannelMode.ForwardedErrorChannel,
    forwarded_output=core.QProcess.ProcessChannelMode.ForwardedOutputChannel,
)

ProcessErrorStr = Literal[
    "failed_to_start", "crashed", "timed_out", "write", "read_error", "unknown_error"
]

PROCESS_ERRORS: bidict[ProcessErrorStr, core.QProcess.ProcessError] = bidict(
    failed_to_start=core.QProcess.ProcessError.FailedToStart,
    crashed=core.QProcess.ProcessError.Crashed,
    timed_out=core.QProcess.ProcessError.Timedout,
    write=core.QProcess.ProcessError.WriteError,
    read_error=core.QProcess.ProcessError.ReadError,
    unknown_error=core.QProcess.ProcessError.UnknownError,
)


ProcessStateStr = Literal["not_running", "starting", "running"]

PROCESS_STATES: bidict[ProcessStateStr, core.QProcess.ProcessState] = bidict(
    not_running=core.QProcess.ProcessState.NotRunning,
    starting=core.QProcess.ProcessState.Starting,
    running=core.QProcess.ProcessState.Running,
)


class Process(core.IODeviceMixin, core.QProcess):
    def set_read_channel(
        self, channel: ProcessChannelStr | core.QProcess.ProcessChannelMode
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
        self, mode: InputChannelModeStr | core.QProcess.InputChannelMode
    ):
        """Set the input channel mode.

        Args:
            mode: mode to set
        """
        self.setInputChannelMode(INPUT_CHANNEL_MODES.get_enum_value(mode))

    def get_input_channel_mode(self) -> InputChannelModeStr:
        return INPUT_CHANNEL_MODES.inverse[self.inputChannelMode()]

    def set_process_channel_mode(
        self, mode: ProcessChannelModeStr | core.QProcess.ProcessChannelMode
    ):
        """Set the process channel mode.

        Args:
            mode: mode to set
        """
        self.setProcessChannelMode(PROCESS_CHANNEL_MODES.get_enum_value(mode))

    def get_process_channel_mode(self) -> ProcessChannelModeStr:
        return PROCESS_CHANNEL_MODES.inverse[self.processChannelMode()]

    def set_state(self, state: ProcessStateStr | core.QProcess.ProcessState):
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
