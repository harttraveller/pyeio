from pathlib import Path
from typing import Literal, get_args

PathLike = str | Path

FileExtension = Literal[
    "json",
    "jsonl",
]

file_extensions = get_args(FileExtension)
