# cbpe-python

CBPE-Python is a framework to estimate continuous blood pressure using only
Photoplethysmogram signals.

# Pre-requisites

- [Python 3.8](https://www.python.org/downloads/release/python-380/)
- [pip](https://pip.pypa.io/en/stable/installing/)
- [venv](https://docs.python.org/3/library/venv.html)
- [Make](https://www.gnu.org/software/make/)

# Setup

In order to use this project it's necessary to install its dependencies, to simplify this process a `Makefile` was used.

## Installation

In order to use this project it's necessary to install it's dependencies and add the pre-commit hooks, to simplify this process a makefile was used. To bootstrap this project simply run:

```bash
$ make bootstrap
```

### Usage

In order to run the main script simply run:

```bash
$ make
```

### Clean

In order to clean the files created by venv, just run:

```bash
$ make clean
```