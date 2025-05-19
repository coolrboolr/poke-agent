from src.utils.logger import log


def test_log_output(capsys):
    log("hello", level="INFO", tag="test")
    captured = capsys.readouterr()
    assert "[INFO][test]" in captured.out
    assert "hello" in captured.out
