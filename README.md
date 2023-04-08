# afplay-py

A python wrapper around the macOS tool `afplay` (audio-file player).

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

Play an audio file:

```python
from afplay import afplay

afplay("path/to/file.mp3", volume=2, time=100, leaks=True)
```

Check if `afplay` is installed:

```python
from afplay import is_installed

print(is_installed())
```
