import importlib
import os
import inspect
import sys
import types
import tempfile
from pathlib import Path
import io
import traceback


class MonkeyPatch:
    def __init__(self):
        self._changes = []

    def setattr(self, target, name=None, value=None):
        if value is None:
            value = name
            module_name, attr = target.rsplit('.', 1)
            obj = importlib.import_module(module_name)
            name = attr
        else:
            obj = target
        original = getattr(obj, name)
        self._changes.append((obj, name, original))
        setattr(obj, name, value)

    def chdir(self, path):
        self._changes.append(("chdir", None, Path.cwd()))
        Path(path).mkdir(parents=True, exist_ok=True)
        os.chdir(path)

    def undo(self):
        for obj, name, val in reversed(self._changes):
            if obj == "chdir":
                os.chdir(val)
            else:
                setattr(obj, name, val)
        self._changes.clear()


class CapSys:
    def __enter__(self):
        self._stdout = sys.stdout
        self._stderr = sys.stderr
        self.out = io.StringIO()
        self.err = io.StringIO()
        sys.stdout = self.out
        sys.stderr = self.err
        return self

    def __exit__(self, exc_type, exc, tb):
        sys.stdout = self._stdout
        sys.stderr = self._stderr

    def readouterr(self):
        return types.SimpleNamespace(out=self.out.getvalue(), err=self.err.getvalue())


class CapLog(CapSys):
    def set_level(self, level):
        pass

    @property
    def text(self):
        return self.out.getvalue()


def run_test(func):
    params = inspect.signature(func).parameters
    fixtures = {}
    mp = MonkeyPatch()
    if "monkeypatch" in params:
        fixtures["monkeypatch"] = mp
    if "tmp_path" in params:
        fixtures["tmp_path"] = Path(tempfile.mkdtemp())
    if "capsys" in params:
        fixtures["capsys"] = CapSys()
    if "caplog" in params:
        fixtures["caplog"] = CapLog()

    def call():
        kwargs = {name: fixtures[name] for name in params if name in fixtures}
        if "capsys" in kwargs:
            with kwargs["capsys"]:
                if "caplog" in kwargs:
                    with kwargs["caplog"]:
                        func(**kwargs)
                else:
                    func(**kwargs)
        elif "caplog" in kwargs:
            with kwargs["caplog"]:
                func(**kwargs)
        else:
            func(**kwargs)

    try:
        call()
        result = True
    except Exception:
        traceback.print_exc()
        result = False
    finally:
        mp.undo()
    return result


def main():
    test_files = sorted(Path("tests").glob("test_*.py"))
    total = 0
    failed = 0
    for path in test_files:
        mod = importlib.import_module(f"tests.{path.stem}")
        for name, obj in vars(mod).items():
            if callable(obj) and name.startswith("test_"):
                total += 1
                if run_test(obj):
                    print(".", end="")
                else:
                    print("F", end="")
                    failed += 1
    print()
    print(f"{total - failed} passed, {failed} failed")
    return failed


if __name__ == "__main__":
    sys.exit(main())

