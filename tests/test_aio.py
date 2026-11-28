"""Tests for signal hooks and unified asyncio integration."""

import asyncio
import contextvars
import gc
import weakref

import pytest

from prettyqt import core, widgets
from prettyqt.utils import signalhooks


class _Emitter(core.Object):
    ping = core.Signal()
    value_changed = core.Signal(int)
    pair_changed = core.Signal(str, int)


class _CountingHook:
    def __init__(self) -> None:
        self.calls: list[tuple[str, tuple]] = []
        self.emits: list[tuple[str, tuple]] = []

    def wrap_slot(self, signal_info, slot):
        def _invoke(target, args):
            self.calls.append((signal_info.name, args))
            return target(*args)

        return signalhooks.make_safe_slot_wrapper(slot, _invoke)

    def on_emit(self, signal_info, args):
        self.emits.append((signal_info.name, args))


def test_signal_hook_arg_trimming_and_disconnect(qapp):
    manager = signalhooks.get_hook_manager()
    hook = _CountingHook()
    manager.register(hook)
    try:
        assert manager.active
        emitter = _Emitter()
        received_zero: list[str] = []
        received_one: list[int] = []
        received_var: list[tuple] = []

        def zero_arg():
            received_zero.append("ok")

        def one_arg(val):
            received_one.append(val)

        def var_args(*args):
            received_var.append(args)

        emitter.value_changed.connect(zero_arg)
        emitter.value_changed.connect(one_arg)
        emitter.pair_changed.connect(var_args)

        emitter.value_changed.emit(42)
        emitter.pair_changed.emit("a", 1)

        assert received_zero == ["ok"]
        assert received_one == [42]
        assert received_var == [("a", 1)]
        assert ("value_changed", ()) in hook.calls
        assert ("value_changed", (42,)) in hook.calls
        assert ("pair_changed", ("a", 1)) in hook.calls
        assert ("value_changed", (42,)) in hook.emits

        # Disconnecting the original function still works.
        emitter.value_changed.disconnect(zero_arg)
        emitter.value_changed.emit(99)
        assert received_zero == ["ok"]
        assert received_one == [42, 99]
    finally:
        manager.unregister(hook)
    assert not manager.active


def test_signal_hook_bound_method_disconnect_and_gc(qapp):
    manager = signalhooks.get_hook_manager()
    hook = _CountingHook()
    manager.register(hook)
    try:
        emitter = _Emitter()
        calls: list[int] = []

        class Receiver(core.Object):
            def on_val(self, v: int) -> None:
                calls.append(v)

        recv = Receiver()
        emitter.value_changed.connect(recv.on_val)
        emitter.value_changed.emit(7)
        assert calls == [7]

        # Bound method disconnect works even when `recv.on_val` is a fresh method obj.
        emitter.value_changed.disconnect(recv.on_val)
        emitter.value_changed.emit(8)
        assert calls == [7]

        # Reconnect and ensure QObject receiver can still be garbage-collected.
        emitter.value_changed.connect(recv.on_val)
        wref = weakref.ref(recv)
        del recv
        gc.collect()
        assert wref() is None
        emitter.value_changed.emit(9)
        assert calls == [7]
    finally:
        manager.unregister(hook)


def test_signal_hook_skips_cpp_slots_and_signal_chaining(qapp):
    manager = signalhooks.get_hook_manager()
    hook = _CountingHook()
    manager.register(hook)
    try:
        e1 = _Emitter()
        e2 = _Emitter()
        seen: list[int] = []
        e1.value_changed.connect(e2.value_changed)
        e2.value_changed.connect(seen.append)
        e1.objectNameChanged.connect(e2.setObjectName)  # C++ builtin slot

        e1.value_changed.emit(123)
        e1.setObjectName("named")

        assert seen == [123]
        assert e2.objectName() == "named"
    finally:
        manager.unregister(hook)


def test_async_bridge_submit_and_contextvars_roundtrip(qapp, qtbot):
    var: contextvars.ContextVar[str] = contextvars.ContextVar("test_var", default="none")
    observed: dict[str, object] = {}

    with core.AsyncBridge() as bridge:
        token = var.set("from-gui")
        try:

            async def work() -> str:
                observed["in_async_thread"] = var.get()
                await asyncio.sleep(0.01)

                def on_gui() -> tuple[str, bool]:
                    return var.get(), core.QThread.currentThread() == qapp.thread()

                gui_val, is_main = await bridge.call_in_gui_thread(on_gui)
                observed["in_gui_callback"] = gui_val
                observed["is_main_thread"] = is_main
                return f"done:{gui_val}"

            fut = bridge.submit(work())
        finally:
            var.reset(token)

        qtbot.waitUntil(fut.done, timeout=3000)
        assert fut.result() == "done:from-gui"
        assert observed == {
            "in_async_thread": "from-gui",
            "in_gui_callback": "from-gui",
            "is_main_thread": True,
        }


def test_wait_for_signal_zero_one_multi_and_timeout(qapp, qtbot):
    emitter = _Emitter()
    silent = _Emitter()

    with core.AsyncBridge() as bridge:
        fut_zero = bridge.submit(core.wait_for_signal(emitter.ping, timeout=2.0))
        fut_one = bridge.submit(core.wait_for_signal(emitter.value_changed, timeout=2.0))
        fut_pair = bridge.submit(core.wait_for_signal(emitter.pair_changed, timeout=2.0))
        fut_timeout = bridge.submit(core.wait_for_signal(silent.ping, timeout=0.03))

        # Let the bridge thread register its connections before emitting.
        qtbot.wait(50)
        expected_val = 55
        emitter.ping.emit()
        emitter.value_changed.emit(expected_val)
        emitter.pair_changed.emit("hello", 9)

        qtbot.waitUntil(
            lambda: all(f.done() for f in (fut_zero, fut_one, fut_pair, fut_timeout)),
            timeout=3000,
        )
        assert fut_zero.result() is None
        assert fut_one.result() == expected_val
        assert fut_pair.result() == ("hello", 9)
        with pytest.raises(TimeoutError):
            fut_timeout.result()


def test_enable_async_slots_and_disconnect(qapp, qtbot):
    emitter = _Emitter()
    done: list[str] = []

    async def on_value() -> None:  # 0-arg slot on 1-arg signal (arg trimming!)
        await asyncio.sleep(0.01)
        val = await core.run_in_gui_thread(lambda: "gui-ok")
        done.append(val)

    try:
        with core.async_slots_enabled():
            emitter.value_changed.connect(on_value)
            emitter.value_changed.emit(1)
            qtbot.waitUntil(lambda: len(done) == 1, timeout=3000)
            assert done == ["gui-ok"]

            emitter.value_changed.disconnect(on_value)
            emitter.value_changed.emit(2)
            qtbot.wait(50)
            assert done == ["gui-ok"]
    finally:
        core.aio.stop_async_bridge()


def test_core_slot_decorator_async(qapp, qtbot):
    results: list[int] = []

    class Handler(core.Object):
        @core.Slot(int)
        async def handle(self, value: int) -> None:
            await asyncio.sleep(0.01)
            results.append(value * 2)

    emitter = _Emitter()
    handler = Handler()
    emitter.value_changed.connect(handler.handle)
    try:
        emitter.value_changed.emit(21)
        qtbot.waitUntil(lambda: results == [42], timeout=3000)
    finally:
        core.aio.stop_async_bridge()


def test_run_async_bridge_backend(qapp):
    completed: list[str] = []

    async def main_coro() -> None:
        await asyncio.sleep(0.01)
        label = await core.run_in_gui_thread(lambda: widgets.Label("hi").text())
        completed.append(label)

    exit_code = core.CoreApplication.run_async(
        main_coro(),
        backend="bridge",
        keep_running=False,
    )
    assert exit_code == 0
    assert completed == ["hi"]
