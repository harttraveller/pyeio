from typing import Optional


def expected_extension(
    inp: str,
    exp: str,
    msg: Optional[str] = None,
) -> None:
    """Validates expected extension."""
    if inp != exp:
        raise Exception  # todo add custom
