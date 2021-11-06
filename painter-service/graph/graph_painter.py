import io
from dataclasses import dataclass
from typing import Union

import plotly.graph_objects as go
import plotly.io as pio
from PIL import Image, ImageDraw, ImageOps
from graph.finance_util import fibonnaci_bands, bollinger_bands, moving_average, calculate_rsi
from models.graph_options import GraphOption
from models.price_point import CollectionSingleTradePoint, CollectionOhcl
from models.token_info import TokenInfo


@dataclass
class GraphPainter:
    datas: Union[CollectionOhcl, CollectionSingleTradePoint]
    token_info: TokenInfo
    options: GraphOption

    def paint_candlestick(self) -> Image:
        """Method that paints a candlestick chart based on a collection of OHCL, token info, and graph options."""
        actual_candlestick = self._generate_candlestick()
        candlestick_img = Image.open(actual_candlestick)
        candlestick_img = self._add_text(candlestick_img)
        border_color = self._pick_border_color(self.datas.first_value().v_close, self.datas.last_value().v_open)
        img_final = self._add_border(candlestick_img, color=border_color)
        return img_final

    def paint_simple_chart(self) -> Image:
        """Similar to get_candlestick, but prints a simple chart"""
        actual_chart = self._generate_chart()
        chart_img = Image.open(actual_chart)
        chart_img = self._add_text(chart_img)
        border_color = self._pick_border_color(self.datas.first_value().value, self.datas.last_value().value)
        img_final = self._add_border(chart_img, color=border_color)
        return img_final

    def _generate_chart(self) -> io.BytesIO:
        """Generates a simple chart of a collection of single trade point.
        The theme will follow the one given in the graph options."""
        chart = go.Figure()

        # chart.add_scatter(x=datas.dates(), y=datas.values(), yaxis='y2', line=go.scatter.Line(color='#636EFA'))
        chart.add_scatter(x=self.datas.dates(), y=self.datas.values(), yaxis='y2', line=go.scatter.Line(color='#8246e5'))
        chart.update_layout(template=self.options.theme.layout_template,
                            annotations=self.options.generate_watermark(),
                            plot_bgcolor=None,
                            autosize=False,
                            width=1600,
                            height=900,
                            xaxis=dict(rangeslider=dict(visible=False)),
                            yaxis2=dict(domain=[0.0, 1],
                                        title=f"{self.token_info.name} price ({self.token_info.currency_against})",
                                        side='right'),
                            showlegend=False,
                            margin=dict(t=15, b=15, r=15, l=15))
        chart = self._process_options(chart)
        img = pio.to_image(fig=chart, scale=2)
        return io.BytesIO(img)

    def _generate_candlestick(self) -> io.BytesIO:
        chart = go.Figure()

        chart.add_candlestick(
            open=self.datas.opens(),
            high=self.datas.highs(),
            low=self.datas.lows(),
            close=self.datas.closes(),
            x=self.datas.dates(),
            yaxis='y2',
            name='OHCL',
            increasing=dict(line=dict(color=self.options.theme.increasing_color)),
            decreasing=dict(line=dict(color=self.options.theme.decreasing_color)),
        )

        colors_volume = [self.options.theme.decreasing_color]

        for i in range(1, len(self.datas.closes())):
            if self.datas.closes()[i] > self.datas.closes()[i - 1]:
                colors_volume.append(self.options.theme.increasing_color)
            else:
                colors_volume.append(self.options.theme.decreasing_color)

        chart.add_bar(
            x=self.datas.dates(),
            y=self.datas.volumes(),
            marker=dict(color=colors_volume),
            yaxis='y',
            name='Volume'
        )

        chart.update_layout(
            template=self.options.theme.layout_template,
            plot_bgcolor=None,
            autosize=False,
            width=1600,
            height=900,
            xaxis=dict(
                rangeslider=dict(visible=False)),
            yaxis=dict(
                domain=[0, 0.19],
                showticklabels=True,
                title=f"Volume ({self.token_info.volume_currency}])",
                side='right'),
            yaxis2=dict(
                domain=[0.2, 1],
                title=f"{self.token_info.name}  price ({self.token_info.currency_against})",
                side='right'),
            showlegend=False,
            margin=dict(
                t=15,
                b=15,
                r=15,
                l=15)
        )
        chart = self._process_options(chart)
        img = pio.to_image(fig=chart, scale=2)
        return io.BytesIO(img)

    def _generate_text_banner(self, width: int = 3200, height: int = 100) -> Image:
        """Generates a text banner of the given width and height. It is assumed that there's a text in the graph
        options. The graph will have the theme of the one passed in the graph options"""
        font = self.options.theme.upper_part_font
        txt = self.options.upper_part_text

        bounding_box = [0, 0, width, height]
        x1, y1, x2, y2 = bounding_box  # For easy reading

        img = Image.new('RGB', (x2, y2), color=self.options.theme.upper_barrier_img_color)

        d = ImageDraw.Draw(img)

        # Calculate the width and height of the text to be drawn, given font size
        w, h = d.textsize(txt, font=font)

        # Calculate the mid points and offset by the upper left corner of the bounding box
        x = (x2 - x1 - w) / 2 + x1
        y = (y2 - y1 - h) / 2 + y1

        # Write the text to the image, where (x,y) is the top left corner of the text
        d.text((x, y), txt, align='center', font=font, fill=self.options.theme.upper_barrier_txt_color)

        return img  # returning raw img

    def _concatenate_two_images(self, im1: Image, im2: Image) -> Image:
        """
        Concatenate two images into one.
        im1 will be put above im2.
        Both images need to have the same width.
        """
        dst = Image.new('RGB', (im1.width, im1.height + im2.height))
        dst.paste(im1, (0, 0))
        dst.paste(im2, (0, im1.height))
        return dst

    def _add_border(self, img, color, border_size: int = 10) -> Image:
        """Add a border of the desired color to the graph"""
        return ImageOps.expand(img, border=border_size, fill=color)

    def _pick_border_color(self, first_value, last_value) -> str:
        """
        Returns a color for the border of the graph based on two values
        """
        if last_value > first_value:
            return self.options.theme.increase_color_img_border
        else:
            return self.options.theme.decrease_color_img_border

    def _add_text(self, image) -> Image:
        """Add a text above an image"""
        if self.options.upper_part_text:
            img_up = self._generate_text_banner()
            return self._concatenate_two_images(img_up, image)
        return image

    def _process_options(self, chart):
        """Adds the options passed in the graph options."""
        if self.options.bollinger_bands:
            bbs = bollinger_bands(self.datas.highs(), self.datas.lows(), self.datas.closes())
            chart.update_layout(showlegend=True)
            for bb in bbs:
                chart.add_scatter(x=self.datas.dates(), y=bb[0][0].to_list(), type='scatter', yaxis='y2',
                                  line=bb[1], name=bb[3],
                                  marker=dict(color='#ccc'), hoverinfo='none',
                                  legendgroup='Bollinger Bands', showlegend=bb[2])

        if self.options.fibonacci_bands:
            annotations = []
            match self.datas:
                case CollectionOhcl():
                    fibo_bands = fibonnaci_bands(self.datas.closes())
                case CollectionSingleTradePoint():
                    fibo_bands = fibonnaci_bands(self.datas.values())
            # fig['layout']['showlegend'] = True
            for res in fibo_bands:
                chart.add_scatter(x=self.datas.dates(), y=res[0][0].to_list(), type='scatter', yaxis='y2',
                                  line=res[1], name=res[2],
                                  marker=dict(color='#ccc'), hoverinfo='none',
                                  legendgroup='Fibo Bands', showlegend=False)
                annotations.append(dict(xref='paper', x=0.0, y=res[0][0].to_list()[0],
                                        xanchor='right', yanchor='middle', yref='y2',
                                        text=res[2],
                                        font=dict(family='Arial',
                                                  size=16),
                                        showarrow=False))
            chart.update_layout(margin=dict(t=15, b=15, r=15, l=100),
                                annotations=annotations)

        if self.options.rsi:
            rsis, lower, upper = calculate_rsi(self.datas.closes())
            chart.update_layout(yaxis=dict(domain=[0, 0.14], title='Volume ($)', side='right'),
                                yaxis3=dict(domain=[0.15, 0.29], showticklabels=True, title='RSI', side='right'),
                                yaxis2=dict(domain=[0.3, 1], title=f"{self.token_info.name} price ({self.token_info.currency_against})", side='right'))
            chart.add_scatter(x=self.datas.dates(), y=rsis, mode='lines',
                              marker=dict(color='#E377C2'),
                              yaxis='y3', name='RSI')
            chart.add_scatter(x=self.datas.dates(), y=lower, mode='lines',
                              marker=dict(color='rgba(13, 55, 13, 0.9)'),
                              yaxis='y3', name='RSI')
            chart.add_scatter(x=self.datas.dates(), y=upper, mode='lines',
                              marker=dict(color='rgba(100, 0, 0, 0.9)'),
                              yaxis='y3', name='RSI')
        if self.options.average:
            mv_y = moving_average(self.datas.closes())
            mv_x = list(self.datas.dates())

            # Clip the ends
            mv_x = mv_x[5:-5]
            mv_y = mv_y[5:-5]

            chart.add_scatter(x=mv_x, y=mv_y, mode='lines',
                              line=dict(width=2),
                              marker=dict(color='#E377C2'),
                              yaxis='y2', name='Moving Average')

        if self.options.finance:
            chart.update_layout(xaxis=dict(rangeslider=dict(visible=False), type='category', dtick=6,
                                           tickformat="%b-%d-%H-%M"))

        return chart
