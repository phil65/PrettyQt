"""Tests for `prettyqt` package."""

# import regex as re

import pytest

from prettyqt import custom_models, widgets
import prettyqt.qt


def test_transposeproxymodel():
    source = widgets.FileSystemModel()
    model = custom_models.TransposeProxyModel(source)
    idx = model.index(0, 0)
    model.data(idx)
    model.columnCount()
    model.rowCount()


def test_regexmatchesmodel(qttester):
    # comp = re.compile("[0-9]")
    # text = "aa356aa356"
    matches = []  # list(comp.finditer(text))
    model = custom_models.RegexMatchesModel(matches)
    qttester.test_model(model, force_py=True)


@pytest.mark.skipif(prettyqt.qt.API.endswith("6"), reason="Only supported in Qt5")
def test_playlistmodel(qttester):
    from prettyqt import multimedia

    model = custom_models.PlaylistModel()
    qttester.test_model(model, force_py=True)
    playlist = multimedia.MediaPlaylist()
    model.set_playlist(playlist)
    assert model.get_playlist() is playlist


def test_importlibdistributionmodel(qttester):
    model = custom_models.ImportlibDistributionModel([])
    qttester.test_model(model, force_py=True)
    custom_models.ImportlibDistributionModel.from_package("prettyqt")
    custom_models.ImportlibDistributionModel.from_system()
