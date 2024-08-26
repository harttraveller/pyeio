from pyeio.core.types import FilePath


# text
def load_text(path: FilePath) -> str:
    with open(path) as file:
        data = file.read()
    file.close()
    return data


def save_text(): ...


def load_text_lines(): ...


def save_text_lines(): ...


def stream_text(): ...


def stream_text_lines(): ...


def stream_text_segments():
    """set start and end delimiters and stream the text between these"""
    ...


# binary
def load_binary(): ...


def save_binary(): ...
