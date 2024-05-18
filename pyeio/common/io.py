from pathlib import Path


# text
def load_text(path: str | Path) -> str: ...


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
