from pathlib import Path
from pyeio.base.types import FilePath


def open_text(path: FilePath) -> str:
    with open(path) as file:
        # * file.read already covers non-existing file error
        data = file.read()
    file.close()
    return data


def save_text(
    data: str,
    path: str | Path,
    overwrite: bool = False,
) -> None:
    path = Path(path)
    if path.exists() and (not overwrite):
        raise FileExistsError(str(path))
    with open(path, "w") as file:
        file.write(data)
    file.close()


# def open_text_lines(): ...


# def save_text_lines(): ...


# def read_text(): ...


# def read_text_lines(): ...


# def read_text_chars(): ...


# def read_text_segments():
#     """set start and end delimiters and stream the text between these"""
#     ...


# # def load_binary(): ...


# def save_binary(): ...


# todo: add append and prepend data functions
# todo: add binary functions
# todo: add analogous web functions (load, stream)
