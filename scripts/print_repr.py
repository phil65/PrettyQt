import inspect

from prettyqt import gui


if __name__ == "__main__":
    clsmembers = inspect.getmembers(gui, inspect.isclass)
    clsmembers = [tpl for tpl in clsmembers if not tpl[0].startswith("Abstract")]
    app = gui.app()
    for name, cls in clsmembers:
        try:
            item = cls()
        except Exception:
            continue
        print(repr(item), str(item))
