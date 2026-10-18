from pathlib import Path
import os
import py_compile
import sys

from repoguard.tools import RepoTools

def test_list_and_search(tmp_path: Path):
    (tmp_path / "hello.py").write_text("def greet():\n    return 'hello'\n", encoding="utf-8")
    tools = RepoTools(tmp_path)
    assert "hello.py" in tools.list_files()
    hits = tools.search_text("greet")
    assert hits[0]["path"] == "hello.py"


def test_test_runner_ignores_stale_timestamp_bytecode(tmp_path: Path):
    target = tmp_path / "app.py"
    target.write_text("value = 1\n", encoding="utf-8")
    original_stat = target.stat()
    py_compile.compile(
        str(target), doraise=True,
        invalidation_mode=py_compile.PycInvalidationMode.TIMESTAMP,
    )
    # Deliberately preserve size and mtime so the old bytecode appears valid.
    target.write_text("value = 2\n", encoding="utf-8")
    os.utime(target, ns=(original_stat.st_atime_ns, original_stat.st_mtime_ns))
    result = RepoTools(tmp_path).run_tests([
        sys.executable, "-c", "import app; assert app.value == 2, app.value"
    ])
    assert result["returncode"] == 0, result


def test_test_runner_uses_current_interpreter_and_preserves_parent_environment(tmp_path: Path):
    (tmp_path / "test_example.py").write_text("def test_example():\n    assert True\n", encoding="utf-8")
    before = os.environ.get("PYTHONPYCACHEPREFIX")
    result = RepoTools(tmp_path).run_tests()
    assert result["command"][0] == sys.executable
    assert result["returncode"] == 0, result
    assert os.environ.get("PYTHONPYCACHEPREFIX") == before
