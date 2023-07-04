To allow for an easy switch, the API layer provided by PrettyQt should be consistent and predictable. When knowing the following guidelines, it should be easy to guess how PrettyQt can be used:

* Every Qt namespace has an equivalent module, named lowerase and with the "Qt"-prefix removed.

```py
from prettyqt import core, widgets, svg
```
*(There´s one exception: QtHelp becomes qthelp in order to not shadow the builtin "help" method.)*

* Every Qt class has an equivalent class with the Q-prefix removed, placed in the corresponding namespace mentioned above. This class derives from the Qt class and a mixin from this framework. The "original" Qt classes are still available in the same module.

```py
widget = widgets.Widget()  # our enriched class
qwidget = widgets.QWidget()  # the original Qt class
curve = core.EasingCurve()
qcurve = core.QEasingCurve()
```

* The Qt-inherited API should still work as-is. If any method is overriden by this framework (only very few cases where this happens), it should still be allowed to call it with the original Qt signature.

```py
widget = widgets.Widget()
widget.setMinimumSize(core.QSize(10, 10))
```


* Naming of the equivalent PrettyQt methods should follow a consistent scheme. Setters are lower-cased and snake-cased, getters are lower-cased, snake-cased and have a get_ prepended to avoid name clashes.
If any lower-cased, snake-cased method name is not provided by PrettyQt, it will call the original method via `__getattr__`. (The last point only applies to classes which inherit from QObject.)

```py
from prettyqt import constants, widgets

widget = widgets.Widget()
widget.set_modality("window")
# constants namespace contains, among other things, everything from QtCore.Qt
widget.set_modality(constants.WindowModality.WindowModal)
assert widget.get_modality() == "window"
assert widget.modality() == constants.WindowModality.WindowModal  # original method still available
```

* Using strings instead of Enums is also possible for setting properties via the constructor.

```py
widget = widgets.Widget(modality="window")
```

* The layer aims to be thin, with no significant overhead. Developers should still use common sense when it comes to using the subclasses vs the original Qt classes though. In loops which get called very often (like paintEvent), it probably still makes sense in lot of cases to not use any subclasses for performance reasons.
It should also be mentioned that Qt does not accept derived classes in some places. (for example as a return value for QAbstractItemModel.data())

* PrettyQt tries to align with Qt´s module hierarchy, meaning that `core` module does not import stuff from `QtGui / gui`, `gui` module does not import `QtWidgets / widgets` etc.
In cases where it is not possible,
