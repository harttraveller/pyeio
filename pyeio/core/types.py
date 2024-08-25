from pathlib import Path
from typing import Literal, get_args

PathLike = str | Path

FileExtension = Literal[
    "json",
    "jsonl",
    "toml",
    "yaml",
    "xml",
    "md",
    "jpeg",
    "zst",
]

file_extensions: tuple[str, ...] = get_args(FileExtension)


VariantFileExtension = Literal[
    "ndjson",
    "jsonlines",
    "jpg",
    "yml",
    "markdown",
]


variant_file_extensions: tuple[str, ...] = get_args(VariantFileExtension)


variant_to_standard: dict[VariantFileExtension, FileExtension] = {
    "ndjson": "jsonl",
    "jsonlines": "jsonl",
    "jpg": "jpeg",
    "yml": "yaml",
    "markdown": "md",
}
