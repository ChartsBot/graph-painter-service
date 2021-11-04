from abc import ABC
from dataclasses import dataclass

import pydantic


@dataclass(frozen=True)
class ChainTheme(ABC, pydantic.BaseModel):
    main_color: str
    secondary_color: str


@dataclass(frozen=True)
class ChainInfo(ABC):
    name: str
    nickname: str
    logo: str
    theme: ChainTheme
