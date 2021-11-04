from dataclasses import dataclass
from typing import Optional, Any

import pydantic

from models.themes import GraphTheme, DarkTheme, WhiteTheme


# noinspection PyTypeChecker
class GraphOption(pydantic.BaseModel):
    theme_name: str = 'dark'
    chain_name: str = 'eth'
    theme: GraphTheme = None
    boillinger_bands: bool = False
    fibonnaci_bands: bool = False
    rsi: bool = False
    average: bool = False
    finance: bool = False
    upper_part_text: Optional[str] = None
    watermark: Optional[str] = None

    def __init__(self, **data: Any):
        super().__init__(**data)
        self.theme = WhiteTheme if self.theme_name.lower() == 'white' else DarkTheme

    def generate_watermark(self):
        """Generates a watermark to add on the graph if requested"""
        if self.watermark is None:
            return []
        else:
            return [dict(name='watermark',
                    font=dict(color=self.theme.watermark_color, size=50),
                    text=self.watermark,
                    xref="paper",
                    yref="paper",
                    x=0.5,
                    y=0.5,
                    showarrow=False,
                    textangle=-30,
                    opacity=0.1, )]
