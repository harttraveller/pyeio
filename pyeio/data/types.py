from pathlib import Path
from typing import Literal, get_args

PathLike = str | Path

FileExtension = Literal[
    "json",
    "jsonl",
    "zst",
]

file_extensions: tuple[str, ...] = get_args(FileExtension)

StandardFileExtension = Literal[
    "json",
    "jsonl",
    "toml",
    "xml",
    "md",
    "jpeg",
]

standard_file_extensions: tuple[str, ...] = get_args(StandardFileExtension)

VariantFileExtension = Literal[
    "ndjson",
    "jsonlines",
]


variant_file_extensions: tuple[str, ...] = get_args(VariantFileExtension)
