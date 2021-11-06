from typing import Optional

import pydantic


class TokenInfo(pydantic.BaseModel):
    name: str
    currency_against: str = '$'
    ticker: Optional[str] = None
    address: Optional[str] = None
    holders: Optional[int] = None
    decimal: Optional[int] = None
    total_supply: Optional[int] = None
    market_cap: Optional[int] = None
    picture_link: Optional[str] = None
