from abc import ABC
from dataclasses import dataclass
from typing import List, Tuple

import pydantic
from PIL import ImageFont


@dataclass(frozen=True)
class GraphTheme(ABC):
    chain_theme: ChainTheme
    upper_barrier_img_color: Tuple[int, int, int]
    upper_barrier_txt_color: Tuple[int, int, int]
    plot_bgcolor: str
    layout_template: str
    increasing_color = '#228B22'
    decreasing_color = '#FF0000'
    upper_part_font_size = 40
    watermark_color: str = 'white'
    upper_part_font = ImageFont.truetype("DejaVuSans.ttf", upper_part_font_size, encoding="unic")


@dataclass(frozen=True)
class DarkTheme(GraphTheme):
    upper_barrier_img_color = (36, 36, 36)
    upper_barrier_txt_color = (255, 255, 255)
    plot_bgcolor = None
    layout_template = 'plotly_dark'
    watermark_color = 'white'


@dataclass(frozen=True)
class WhiteTheme(GraphTheme):
    upper_barrier_img_color = (255, 255, 255)
    upper_barrier_txt_color = (0, 0, 0)
    plot_bgcolor = None
    layout_template = 'rgb(250, 250, 250)'
    watermark_color = 'dark'
    watermark = [dict(name='watermark',
                      font=dict(color="dark", size=50),
                      text="THEFOMOBOT.COM",
                      xref="paper",
                      yref="paper",
                      x=0.5,
                      y=0.5,
                      showarrow=False,
                      textangle=-30,
                      opacity=0.1, )]

