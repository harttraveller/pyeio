# ruff: noqa


import orjson
from functools import lru_cache


@lru_cache(maxsize=8)
def compute_orjson_opt_code(
    append_newline: bool = False,
    indent_two_spaces: bool = False,
    coerce_keys_to_str: bool = True,
    coerce_dataclasses: bool = True,
    coerce_datetimes: bool = True,
    coerce_subclasses: bool = True,
    coerce_numpy_arrays: bool = True,
    sort_keys: bool = False,
) -> int:
    """
    This computes the orjson opt code, for more info, see:
    https://github.com/ijl/orjson

    Args:
        append_newline (bool): _description_
        indent_two_spaces (bool): _description_
        coerce_keys_to_str (bool): _description_
        coerce_dataclasses (bool): _description_
        coerce_datetimes (bool): _description_
        coerce_subclasses (bool): _description_
        coerce_numpy_arrays (bool): _description_
        sort_keys (bool): _description_

    Returns:
        int: The OPT code.
    """
    return (
        (append_newline * orjson.OPT_APPEND_NEWLINE)
        | (indent_two_spaces * orjson.OPT_INDENT_2)
        | orjson.OPT_NAIVE_UTC
        | (coerce_keys_to_str * orjson.OPT_NON_STR_KEYS)
        | orjson.OPT_OMIT_MICROSECONDS
        | (not coerce_dataclasses * orjson.OPT_PASSTHROUGH_DATACLASS)
        | (not coerce_datetimes * orjson.OPT_PASSTHROUGH_DATETIME)
        | (not coerce_subclasses * orjson.OPT_PASSTHROUGH_SUBCLASS)
        | (coerce_numpy_arrays * orjson.OPT_SERIALIZE_NUMPY)
        | (sort_keys * orjson.OPT_SORT_KEYS)
    )


def serialize_orjson(): ...


def serialize_pydantic(): ...


def write_orjson(): ...


def write_pydantic(): ...


def serialize(): ...


def write(): ...


def parse(): ...


def read(): ...
