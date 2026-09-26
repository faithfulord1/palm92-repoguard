"""Package the declarative Kaggle ADK submission without model weights."""
from __future__ import annotations

from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import argparse

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "competition" / "adk_submission"
ALLOWED = {".yaml", ".yml", ".md", ".txt", ".py", ".json", ".safetensors"}


def build(destination: Path) -> None:
    files = sorted(p for p in SOURCE.rglob("*") if p.is_file())
    if not (SOURCE / "agent.yaml").is_file():
        raise ValueError("Missing root agent.yaml")
    if any(p.is_symlink() or p.suffix not in ALLOWED for p in files):
        raise ValueError("Unsupported extension or symlink in submission")
    if sum(p.stat().st_size for p in files) >= 3 * 1024**3:
        raise ValueError("Submission exceeds 3 GiB unpacked")
    destination.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(destination, "w", ZIP_DEFLATED) as archive:
        for path in files:
            archive.write(path, path.relative_to(SOURCE).as_posix())
    with ZipFile(destination) as archive:
        names = archive.namelist()
        if names.count("agent.yaml") != 1 or len(names) != len(set(names)):
            raise ValueError("Invalid submission archive structure")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=ROOT / "submission.zip")
    args = parser.parse_args()
    build(args.output)
    print(args.output)
