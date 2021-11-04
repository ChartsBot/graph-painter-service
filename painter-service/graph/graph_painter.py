import io
from dataclasses import dataclass
from typing import List

from models.graph_options import GraphOption
from models.price_point import CollectionSingleTradePoint, CollectionOhcl
from models.token_info import TokenInfo

import plotly.io as pio
import plotly.express as px
from PIL import Image, ImageDraw, ImageFont, ImageOps
import pandas as pd
import plotly.graph_objects as go


@dataclass
class GraphPainter:

    def get_candlestick(self, ohcls: CollectionOhcl, token_info: TokenInfo, options: GraphOption):
        pass

    def get_simple_chart(self, datas: CollectionSingleTradePoint, token_info: TokenInfo, options: GraphOption):
        pass

    def _generate_chart(self, datas: CollectionSingleTradePoint, token_info: TokenInfo,
                        options: GraphOption) -> io.BytesIO:
        chart = go.Figure()

        # chart.add_scatter(x=datas.dates(), y=datas.values(), yaxis='y2', line=go.scatter.Line(color='#636EFA'))
        chart.add_scatter(x=datas.dates(), y=datas.values(), yaxis='y2', line=go.scatter.Line(color='#8246e5'))
        chart.update_layout(template=options.theme.layout_template,
                            annotations=options.generate_watermark(),
                            plot_bgcolor=None,
                            autosize=False,
                            width=1600,
                            height=900,
                            xaxis=dict(rangeslider=dict(visible=False)),
                            yaxis2=dict(domain=[0.0, 1], title=token_info.name + ' price ($)', side='right'),
                            showlegend=False,
                            margin=dict(t=15, b=15, r=15, l=15))

        img = pio.to_image(fig=chart, scale=2)
        return io.BytesIO(img)

    def _generate_candlestick(self, ohcls: CollectionOhcl, token_info: TokenInfo, options: GraphOption):
        data = [dict(
            type='candlestick',
            open=ohcls.opens(),
            high=ohcls.highs(),
            low=ohcls.lows(),
            close=ohcls.closes(),
            x=ohcls.dates(),
            yaxis='y2',
            name='OHLC',
            increasing=dict(line=dict(color=options.theme.increasing_color)),
            decreasing=dict(line=dict(color=options.theme.decreasing_color)),
        )]
        layout = {}

        fig = dict(data=data, layout=layout)

        fig['layout'] = {
            'plot_bgcolor': None,
            'template': 'plotly_dark',
            'autosize': False,
            'width': 1600,
            'height': 900,
            'xaxis': dict(rangeslider=dict(visible=False)),
            'yaxis': dict(
                domain=[0, 0.19],
                showticklabels=True,
                title='Volume ($)',
                side='right',
            ),
            'yaxis2': dict(
                domain=[0.2, 1],
                title=token_info.name + ' price ($)',
                side='right'
            ),
            'showlegend': False,
            'margin': dict(
                t=15,
                b=15,
                r=15,
                l=15
            )
        }

        colors_volume = []

        for i in range(len(ohcls.closes())):
            if i == 0:
                colors_volume.append(options.theme.decreasing_color)

            elif ohcls.closes()[i] > ohcls.closes()[i - 1]:
                colors_volume.append(options.theme.increasing_color)
            else:
                colors_volume.append(options.theme.decreasing_color)
        fig['data'].append(dict(x=ohcls.dates(), y=ohcls.volumes(),
                                marker=dict(color=colors_volume),
                                type='bar', yaxis='y', name='Volume'))

        img = pio.to_image(fig=fig, scale=2)
        return io.BytesIO(img)

    def _generate_upper_part(self, options: GraphOption, width=3200) -> Image:
        """Generates the upper part given a text. It is assumed that there's a text in the graph options"""
        font = options.theme.upper_part_font
        txt = options.upper_part_text

        bounding_box = [0, 0, width, 100]
        x1, y1, x2, y2 = bounding_box  # For easy reading

        img = Image.new('RGB', (x2, y2), color=options.theme.upper_barrier_img_color)

        d = ImageDraw.Draw(img)

        # Calculate the width and height of the text to be drawn, given font size
        w, h = d.textsize(txt, font=font)

        # Calculate the mid points and offset by the upper left corner of the bounding box
        x = (x2 - x1 - w) / 2 + x1
        y = (y2 - y1 - h) / 2 + y1

        # Write the text to the image, where (x,y) is the top left corner of the text
        d.text((x, y), txt, align='center', font=font, fill=options.theme.upper_barrier_txt_color)

        return img  # returning raw img

    def _concatenate_two_images(self, im1, im2):
        """
        Concatenate two images into one.
        im1 will be put above im2.
        Both images need to have the same width.
        """
        dst = Image.new('RGB', (im1.width, im1.height + im2.height))
        dst.paste(im1, (0, 0))
        dst.paste(im2, (0, im1.height))
        return dst
