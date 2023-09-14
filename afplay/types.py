from pathlib import Path
from typing import Literal, Union

File = Union[str, Path]
IntStr = Union[int, str]
Quality = Union[Literal["0"], Literal["1"], Literal["HIGH"], Literal["LOW"]]
