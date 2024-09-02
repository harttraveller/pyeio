from typing import Optional
from pyeio.types import file_extensions


class UnexpectedError(Exception):
    """Raised when something unexpected happens."""

    def __init__(
        self,
        message: Optional[str] = None,
    ) -> None:
        self.message = "This was unexpected! Please submit a GitHub issue with the code that generated this error."
        if message:
            self.message += f"\n{message}"
        super().__init__(self.message)


class InvalidFileExtensionError(Exception):
    """Raised when the provided extension does not match the expected extension(s)."""

    def __init__(
        self,
        extension: str,
        expected: str | set[str],
    ) -> None:
        self.extension = extension
        self.expected = expected
        self.message = f"Extension '{self.extension}' should be '{self.expected}'"
        super().__init__(self.message)


class UnknownExtensionError(Exception):
    """Raised when the provided extension is not known/supported yet."""

    def __init__(
        self,
        extension: str,
    ) -> None:
        self.extension = extension
        self.message = (
            f"Unknown extension '{extension}'."
            f"\nAvailable extensions are: '{file_extensions}'."
        )
        super().__init__(self.message)
