import inspect
import pathlib

from prettyqt import custom_widgets, widgets


module_dict = dict(custom_widgets=custom_widgets)
app = widgets.app()

for module in module_dict.values():
    clsmembers = inspect.getmembers(module, inspect.isclass)
    for _klass_name, Klass in clsmembers:
        widget = None
        match Klass:
            case _:
                try:
                    widget = Klass()
                    if not isinstance(widget, widgets.WidgetMixin):
                        continue
                    widget.show()
                    app.processEvents()
                    pixmap = widget.grab()
                    path = pathlib.Path().absolute() / "screenshots"
                    path.mkdir(parents=True, exist_ok=True)
                    filename = type(widget).__name__
                    pixmap.save(f"{path / filename}.png", "png")
                except Exception as e:
                    print(e)
                finally:
                    if hasattr(widget, "hide"):
                        widget.hide()
