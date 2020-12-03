import os


def get_hook_dirs():
    return [os.path.dirname(__file__)]
    # return [str(pathlib.Path(__file__).parent)]
