from __future__ import annotations

import logging

from prettyqt import core, eventfilters, itemmodels, widgets


logger = logging.getLogger(__name__)


class QObjectPropertiesTableView(widgets.TableView):
    def __init__(self, *args, **kwargs):
        self.event_catcher = None
        self._handles: list[core.QMetaObject.Connection] = []
        super().__init__(*args, **kwargs)
        self.set_icon("mdi.folder")
        self.set_selection_behavior("rows")
        self.setEditTriggers(self.EditTrigger.AllEditTriggers)
        self.set_delegate("editor", column=1)

    def set_qobject(
        self,
        qobject: core.QObject,
        update_on_event: bool = True,
        update_on_signal_emission: bool = True,
    ):
        prev_model = self.get_model(skip_proxies=True)
        if prev_model is not None and prev_model._qobject:
            self.unhook()
        model = itemmodels.QObjectPropertiesModel(qobject, parent=self)
        # model.dataChanged.connect(self.repaint)
        self.set_model(model)
        if update_on_event:
            self.event_catcher = eventfilters.EventCatcher(
                include=["resize", "move"], parent=qobject
            )
            logger.debug(f"Connected {qobject!r} to {model!r}")
            self.event_catcher.caught.connect(model.force_layoutchange)
            qobject.installEventFilter(self.event_catcher)
        if update_on_signal_emission:
            metaobj = core.MetaObject(qobject.metaObject())
            self._handles = metaobj.connect_signals(
                qobject, model.force_layoutchange, only_notifiers=True
            )

    def unhook(self):
        model = self.get_model(skip_proxies=True)
        for handle in self._handles:
            model._qobject.disconnect(handle)
        model._qobject.removeEventFilter(self.event_catcher)
        logger.debug(f"Disconnected {model._qobject!r} from {self!r}")


if __name__ == "__main__":
    app = widgets.app()
    with app.debug_mode():
        w = QObjectPropertiesTableView()
        w.set_qobject(app)
        w.show()
        app.exec()
