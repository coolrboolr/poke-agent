import importlib

from src.utils.logger import log


def test_emulator_import_and_log():
    module = importlib.import_module("src.emulator")
    assert module is not None
    log("emulator imported")
