from __future__ import annotations

from prettyqt import core
from prettyqt.qt import QtDesigner, QtWidgets


class PyDesignerCustomWidgetPlugin(
    core.ObjectMixin, QtDesigner.QPyDesignerCustomWidgetPlugin
):
    def name(self):
        return "Hallo"

    def icon(self):
        return "icon"

    def group(self):
        return "group"

    def includeFile(self):
        return "includeFile"

    def isContainer(self):
        return True

    def toolTip(self):
        return "toolTip"

    def whatsThis(self):
        return "whatsThis"

    def initialize(self, interface: QtDesigner.QDesignerFormEditorInterface):
        return super().initialize(interface)

    def get_code_template(self):
        return self.codeTemplate()

    def create_widget(self, parent: QtWidgets.QWidget):
        return self.createWidget(parent)

    def get_dom_xml(self):
        return self.domXml()


if __name__ == "__main__":
    plg = PyDesignerCustomWidgetPlugin()
    print(plg.toolTip())
    new = dir(PyDesignerCustomWidgetPlugin())
    bie = dir(core.Object())
    c = [x for x in new if x not in bie]
    print(c)
