# Installation

## Requirements

**System**

The package has only been tested on MacOS, specifically a machine with an ARM chipset. I imagine it would work on other machines too. If you run into any bugs, feel free to submit a GitHub Issue.

**Software**

Both Git and miniconda are strongly recommended. I recommend configuring a Python environment on your machine and installing `pyeio` inside of it.

**Python Version**

The package requires Python 3.10 or above. 

**Python Packages**

The required python dependencies can be found in the `setup.py` file in the repository. The developer python dependencies are listed in the `requirements.txt` file in the repository.


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

**SSH**

```bash
git clone git@github.com:cephalon-intelligence/pyeio.git
```

**HTTPS**

```bash
git clone https://github.com/cephalon-intelligence/pyeio.git
```

Next install the package with `pip`. The `setup.py` package contains the requirements for basic functionality, however the `requirements.txt` file also includes requirements for testing and using the notebooks.

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

## Testing

The package uses `pytest` for testing. You can learn more about pytest on their [homepage](https://pytest.org/). To run the tests, you can run the following command.

```bash
pytest pyeio
```

