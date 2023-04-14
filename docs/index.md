---
hide:
- navigation
---

# Introduction

Python Easy Input Output is a Python library meant to simplify file IO processes. It provides the ability to load and save different file formats with just the `load` and `save` methods. The required python dependencies can be found in the [setup.py](https://github.com/harttraveller/pyeio/blob/main/setup.py) file, and the developer dependencies are listed in the [requirements.txt](https://github.com/harttraveller/pyeio/blob/main/requirements.txt) file in the repository.

<br>

<div align="center">
<a href="https://github.com/harttraveller/pyeio" target="_blank">
<img src="assets/github.png" width=20 style="position: relative; left: 0px;">
</a>
<a href="https://pypi.org/project/pyeio/" target="_blank">
<img src="https://img.shields.io/pypi/v/pyeio" height=20 style="position: relative;">
</a>
<a href="https://github.com/harttraveller/pyeio/blob/main/LICENSE" target="_blank">
<img src="https://img.shields.io/badge/license-MIT-blue" height=20 style="position: relative;">
</a>
<a href="https://www.python.org/downloads" target="_blank">
<img src="https://img.shields.io/badge/python-3.10-blue" height=20 style="position: relative;">
</a>
<a href="https://github.com/psf/black" target="_blank">
<img src="https://img.shields.io/badge/code%20style-black-black" height=20 style="position: relative;">
</a>
</div>

## User Installation

Install the current version of `pyeio` with `pip`.

```bash
pip install pyeio
```

To upgrade to a newer release use the `--upgrade` flag.

```bash
pip install pyeio --upgrade
```

## Developer Installation

First clone the repository. You can do this using SSH, or HTTPS. I recommend SSH, as it's more secure.

=== "SSH"
    ```bash
    git clone git@github.com:harttraveller/pyeio.git
    ```
=== "HTTPS"
    ```bash
    git clone https://github.com/harttraveller/pyeio.git
    ```

Next, install the requirements and install the package locally with pip.

```bash
cd pyeio
pip install -r requirements.txt
pip install -e . # (1)!
```

1. The `-e` flag installs the package in editable mode.

You can update `pyeio` by running the following command in the same directory. There may be new requirements added.

```bash
git pull origin main
pip install -r requirements.txt
pip install -e . --upgrade
```

## Running Tests

The package uses `pytest` for testing. You can learn more about pytest on their [homepage](https://pytest.org/). To run the tests, you can run the following command.

```bash
pytest pyeio
```

## Support

If you run into any bugs, please submit an [issue]() on GitHub.