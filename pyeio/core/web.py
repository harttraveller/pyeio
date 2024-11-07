import httpx
from io import BytesIO
from pathlib import Path
from tqdm import tqdm


def check_if_remote_accepts_byte_range(
    url: str,
    follow_redirects: bool = True,
) -> bool:
    """
    Check if a remote server accepts byte range requests.

    This function sends a HEAD request to the specified URL with a 'Range' header
    to determine if the server supports partial content requests.

    Args:
        url (str): The URL to check for byte range support.
        follow_redirects (bool, optional): Whether to follow redirects. Defaults to True.

    Returns:
        bool: True if the server accepts byte range requests, False otherwise.
    """
    headers = {"Range": "bytes=0-8"}
    response = httpx.head(url=url, headers=headers, follow_redirects=follow_redirects)
    response.raise_for_status()
    return response.status_code == 206


def stream_resource_chunk(
    url: str,
    start: int,
    end: int,
    follow_redirects: bool = True,
) -> bytes:
    """
    Read a specific byte range from a remote resource.

    This function sends a GET request to the specified URL with a 'Range'
    header to retrieve a specific chunk of the resource.

    Args:
        url (str): The URL of the remote resource.
        start (int): The starting byte position of the chunk.
        end (int): The ending byte position of the chunk.
        follow_redirects (bool, optional): Whether to follow redirects. Defaults to True.

    Returns:
        bytes: The requested chunk of the resource as bytes.

    Raises:
        Exception: If the remote server does not accept byte range requests.
    """
    headers = {"Range": f"bytes={start}-{end}"}
    buffer = BytesIO()
    response = httpx.get(url, headers=headers, follow_redirects=follow_redirects)
    response.raise_for_status()
    if response.status_code != 206:
        raise Exception("The remote server does not accept byte range requests.")
    buffer.write(response.content)
    buffer.seek(0)
    return buffer.read()


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
