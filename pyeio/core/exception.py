from typing import Optional


class InvalidExtensionError(Exception):
    """Raised when the provided extension does not match the expected extension."""

    def __init__(
        self,
        provided: str,
        expected: str,
        message: Optional[str] = None,
    ) -> None:
        self.provided = provided
        self.expected = expected
        self.message = f"Expected extension '{expected}', but got '{provided}'."
        if message:
            self.message += f"\n{message}"
        super().__init__(self.message)
