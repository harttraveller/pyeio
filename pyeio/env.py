TRANSFORM_DICT = {
    "json": {
        "list": list,
        "dict": dict,
        "pandas.core.series.Series": list,
        "pandas.core.frame.DataFrame": lambda x: x.to_dict(orient="list"),
    }
}
