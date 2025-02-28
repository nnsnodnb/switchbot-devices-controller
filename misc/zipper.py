import zipfile
from collections.abc import Generator
from pathlib import Path

IGNORE_PATHS = [
    ".pytest_cache",
    ".ruff_cache",
    "tests",
    "__pycache__",
    ".venv",
    ".git",
    "cloudformation",
    ".idea",
    ".env",
    ".DS_Store",
]


def _walk(src: Path) -> Generator[Path]:
    for item in src.iterdir():
        if item.name in IGNORE_PATHS or item.name.endswith(".zip"):
            continue

        if item.is_dir():
            yield from _walk(item)
        else:
            yield item


def zip_folder(src: Path, dest: Path) -> Path:
    dest.mkdir(exist_ok=True)
    dist = dest / "switchbot-devices-controller.zip"
    if dist.exists():
        dist.unlink()

    with zipfile.ZipFile(dist, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for target in _walk(src=src):
            if target == dist or target == dest:
                continue
            filename = target.relative_to(src)
            zf.write(filename=target, arcname=filename)

    return dist
