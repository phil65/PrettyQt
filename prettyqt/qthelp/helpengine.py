from __future__ import annotations

from prettyqt import qthelp


class HelpEngine(qthelp.HelpEngineCoreMixin, qthelp.QHelpEngine):
    """Access to contents and indices of the help engine."""

    def get_content_model(self) -> qthelp.HelpContentModel:
        return qthelp.HelpContentModel(self.contentModel())


if __name__ == "__main__":
    engine = HelpEngine("")
    engine.get_files("a", "b")
