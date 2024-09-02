# pyeio

This is a python library for data input/output operations. This library prioritizes developer experience, standardization, and global interoperability/format support over speed. For instance, if you want something faster than [orjson](https://github.com/ijl/orjson) for handling JSON data, you should something like [msgspec](https://jcristharif.com/msgspec/).

## TLDR

To install the package, run `pip install 'pyeio[<formats>]'` where the formats you want to be able to handle are comma delimited. For instance, installing `pyeio` with JSON and TOML support looks like:

```sh
pip install 'pyeio[json,toml]'
```

The reason you have to specify a specific format is because this library aims to maximally cover as many possible formats, so installing all the dependencies will be excessive for most use cases. If you want to install them all though, you can with:

```sh
pip install 'pyeio[all]'
```

!!! note
    Support for some formats is included by proxy in others. For instance, support for JSONL is included in JSON, and vice versa.

## Getting Started


## Details

By default, all modules imported directly from pyeio



## General Methods

The following methods are standard across all file format modules.

### `parse`

This parses data from a string or byte string.

### `load`

### `read`

### `parse`

### `save`

### `dump`

### `stream`

### `download`





## Formats

## Targets

- Native python data structures
- Dataframes
- Numpy arrays
- Specialized classes




