from src.utils.logger import log


def test_log_output(capsys):
    log("hello", level="DEBUG")
    captured = capsys.readouterr()
    assert "DEBUG" in captured.out
    assert "hello" in captured.out
