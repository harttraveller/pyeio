import httpx
from io import BytesIO
from pathlib import Path
from tqdm import tqdm


def get(url: str, progress: bool = False) -> bytes:
    """_summary_

    Args:
        url (str): _description_
        progress (bool, optional): _description_. Defaults to False.

    Returns:
        bytes: _description_
    """
    ...


def download(url: str, path: str | Path, progress: bool = False) -> None:
    """_summary_

    Args:
        url (str): _description_
        path (str | Path): _description_
        progress (bool, optional): _description_. Defaults to False.
    """
    ...
