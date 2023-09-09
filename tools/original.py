from typing import Iterable, Tuple
from pathlib import Path

def _get_source_dir() -> Path:
    return Path(__file__).resolve().parent

def get_original_files() -> Iterable[Path]:
    files = (_get_source_dir() / "../original").glob("*.bmp")
    yield from sorted(files)
