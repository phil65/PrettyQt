import pathlib
from typing import Callable, List, Optional, Union

from qtpy import QtCore

from prettyqt import constants, core
from prettyqt.utils import InvalidParamError


QtCore.QCoreApplication.__bases__ = (core.Object,)


class CoreApplication(QtCore.QCoreApplication):
    @classmethod
    def call_on_exit(cls, func: Callable):
        cls.instance().aboutToQuit.connect(func)

    @classmethod
    def get_application_file_path(cls) -> pathlib.Path:
        return pathlib.Path(cls.applicationFilePath())

    @classmethod
    def get_application_dir_path(cls) -> pathlib.Path:
        return pathlib.Path(cls.applicationDirPath())

    @classmethod
    def add_library_path(cls, path: Union[pathlib.Path, str]):
        cls.addLibraryPath(str(path))

    @classmethod
    def get_library_paths(cls) -> List[pathlib.Path]:
        return [pathlib.Path(i) for i in cls.libraryPaths()]

    @classmethod
    def use_hdpi_bitmaps(cls, state: bool = True):
        cls.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, state)

    @classmethod
    def disable_window_help_button(cls, state: bool = True):
        cls.setAttribute(QtCore.Qt.AA_DisableWindowContextHelpButton, state)

    def set_metadata(
        self,
        app_name: Optional[str] = None,
        app_version: Optional[str] = None,
        org_name: Optional[str] = None,
        org_domain: Optional[str] = None,
    ):
        if app_name is not None:
            self.setApplicationName(app_name)
        if app_version is not None:
            self.setApplicationVersion(app_name)
        if org_name is not None:
            self.setOrganizationName(org_name)
        if org_domain is not None:
            self.setOrganizationDomain(org_domain)
        # import ctypes
        # myappid = 'mycompany.myproduct.subproduct.version' # arbitrary string
        # ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    def load_language_file(self, file: Union[pathlib.Path, str]) -> core.Translator:
        translator = core.Translator(self)
        if file in ["de", "fr"]:
            path = pathlib.Path(__file__).parent.parent
            file = path / "localization" / f"qtbase_{file}.ts"
        translator.load(str(file))
        self.installTranslator(translator)
        return translator

    def post_event(
        self,
        obj: QtCore.QObject,
        event: QtCore.QEvent,
        priority: Union[int, constants.EventPriorityStr] = "normal",
    ):
        if isinstance(priority, str):
            if priority not in constants.EVENT_PRIORITY:
                raise InvalidParamError(priority, constants.EVENT_PRIORITY)
            priority = constants.EVENT_PRIORITY[priority]
        return self.postEvent(obj, event, priority)

    def main_loop(self) -> int:
        return self.exec_()
