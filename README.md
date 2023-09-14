# afplay-py

A python wrapper and better CLI for the macOS tool `afplay` (audio-file player).

## Installation

From pip:

```shell
pip install afplay-py
```

From source (from the root project directory):

```shell
pip install .
```

## Quick Usage

### CLI

Play an audio file using the CLI:

```sh
afplay-py ~/path/to/file.mp3
```

**NOTE**: The intent is for this CLI to not have some of the problems the regular tool does.

### Python

Play an audio file using Python:

```python
from afplay import afplay

afplay("path/to/file.mp3", volume=2, time=100, leaks=True)
```

Check if `afplay` is installed:

```python
from afplay import is_installed

print(is_installed())
```
