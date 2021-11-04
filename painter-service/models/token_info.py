from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True, unsafe_hash=True)
class TokenInfo:
    name: str
    ticker: Optional[str] = None
    address: Optional[str] = None
    holders: Optional[int] = None
    decimal: Optional[int] = None
    total_supply: Optional[int] = None
    market_cap: Optional[int] = None
    picture_link: Optional[str] = None
