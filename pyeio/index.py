from typing import get_args
from .types import FileExtension, VariantFileExtension

file_extensions: tuple[str, ...] = get_args(FileExtension)

variant_file_extensions: tuple[str, ...] = get_args(VariantFileExtension)
variant_to_standard: dict[VariantFileExtension, FileExtension] = {
    "ndjson": "jsonl",
    "jsonlines": "jsonl",
    # "jpg": "jpeg",
    # "yml": "yaml",
    # "markdown": "md",
}
