from pathlib import Path
from pyeio.internal.types import FilePath


def open_text(path: FilePath) -> str:
    """
    Open a file as text data.

    Args:
        path (FilePath): _description_

    Returns:
        str: The data in the file.

    Raises:
        FileNotFoundError: Raised when file path not found.
    """
    with open(path) as file:
        data = file.read()
    file.close()
    return data


def open_text_lines(): ...


def open_text_chars(): ...


def open_text_blocks(path: FilePath, delimiter: str) -> list[str]:
    """_summary_

    Args:
        path (FilePath): _description_
        delimiter (str): regex match to split text on

    Returns:
        list[str]: _description_
    """
    ...


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


# def save_text_lines(): ...


# def read_text(): ...


# def read_text_lines(): ...


# def read_text_chars(): ...


# def read_text_segments():
#     """set start and end delimiters and stream the text between these"""
#     ...


def append_text(): ...


def prepend_text(): ...


def insert_text(): ...


def delete_text(): ...


def append_text_line(): ...


def append_text_lines(): ...


def prepend_text_line(): ...


def prepend_text_lines(): ...


def insert_text_line(): ...


def insert_text_lines(): ...


def delete_text_line(): ...


def delete_text_lines(): ...


# # def load_binary(): ...


# def save_binary(): ...


# todo: add append and prepend data functions
# todo: add binary functions
# todo: add analogous web functions (load, stream)
