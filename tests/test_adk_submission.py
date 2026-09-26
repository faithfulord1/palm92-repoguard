from pathlib import Path
from zipfile import ZipFile
import importlib.util


def test_adk_archive_has_only_declared_files(tmp_path: Path):
    source = Path(__file__).resolve().parents[1] / "scripts" / "build_adk_submission.py"
    spec = importlib.util.spec_from_file_location("build_adk_submission", source)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    archive = tmp_path / "submission.zip"
    module.build(archive)
    with ZipFile(archive) as z:
        assert set(z.namelist()) == {"agent.yaml", "eval_config.yaml", "prompts/system.md"}
        config = z.read("agent.yaml").decode()
        assert "gemma-4-31b-it-qat-w4a16-ct" in config
        assert "submit_patch" in config
        assert "{problem_description}" in z.read("prompts/system.md").decode()
