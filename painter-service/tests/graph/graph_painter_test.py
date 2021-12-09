from pprint import pprint

import time
import unittest
import json
import os

from PIL import Image

from graph.graph_painter import GraphPainter
from models.graph_options import GraphOption
from models.price_point import CollectionSingleTradePoint, CollectionOhcl
from models.token_info import TokenInfo
from tests.test_elements import EXAMPLE_JSON_COLLECTION_SINGLE_TRADE_POINT, EXAMPLE_JSON_COLLECTION_OHCL, \
    EXAMPLE_TOKEN_INFO, EXAMPLE_JSON_COLLECTION_OHCL_CRO, EXAMPLE_JSON_COLLECTION_SINGLE_TRADE_POINT_VOLUME


class GraphPainterTest(unittest.TestCase):
    json_coll_single_points_class = json.loads(EXAMPLE_JSON_COLLECTION_SINGLE_TRADE_POINT)
    coll_single_trade_point = CollectionSingleTradePoint(**json_coll_single_points_class)

    json_coll_single_points_class_vol = json.loads(EXAMPLE_JSON_COLLECTION_SINGLE_TRADE_POINT_VOLUME)
    coll_single_trade_point_volume = CollectionSingleTradePoint(**json_coll_single_points_class_vol)

    json_coll_ohcl = json.loads(EXAMPLE_JSON_COLLECTION_OHCL)
    coll_ohcl = CollectionOhcl(**json_coll_ohcl)

    json_coll_ohcl_cro = json.loads(EXAMPLE_JSON_COLLECTION_OHCL_CRO)
    coll_ohcl_cro = CollectionOhcl(**json_coll_ohcl_cro)

    ti: TokenInfo = EXAMPLE_TOKEN_INFO

    file_path = os.path.dirname(os.path.realpath(__file__)) + '/img.png'

    def test_painting_collection_single_points(self):
        opt = GraphOption()
        gp = GraphPainter(datas=self.coll_single_trade_point,
                          token_info=self.ti,
                          options=opt)

        res = gp._generate_chart()
        chart_img = Image.open(res)
        # chart_img.show()
        chart_img.save(self.file_path)

    def test_painting_collection_single_points_with_volume(self):
        opt = GraphOption()
        gp = GraphPainter(datas=self.coll_single_trade_point_volume,
                          token_info=self.ti,
                          options=opt)

        res = gp._generate_chart()
        chart_img = Image.open(res)
        # chart_img.show()
        chart_img.save(self.file_path)

    def test_painting_with_watermark(self):
        """Is there a watermark on the painting?"""
        opt = GraphOption(watermark='TESTTESTTEST')
        gp = GraphPainter(datas=self.coll_single_trade_point,
                          token_info=self.ti,
                          options=opt)
        res = gp._generate_chart()
        chart_img = Image.open(res)
        chart_img.save(self.file_path)

    def test_painting_collection_ohcl(self):
        opt = GraphOption()
        gp = GraphPainter(datas=self.coll_ohcl,
                          token_info=self.ti,
                          options=opt)
        res = gp._generate_candlestick()
        chart_img = Image.open(res)
        chart_img.save(self.file_path)

    def test_paint_full_simple_chart(self):
        opt = GraphOption(upper_part_text='This is a test')
        gp = GraphPainter(datas=self.coll_single_trade_point,
                          token_info=self.ti,
                          options=opt)
        chart_img = gp.paint_simple_chart()
        chart_img.save(self.file_path)

    def test_paint_full_candlestick(self):
        opt = GraphOption(upper_part_text='This is a test')
        gp = GraphPainter(datas=self.coll_ohcl,
                          token_info=self.ti,
                          options=opt)
        chart_img = gp.paint_candlestick()
        chart_img.save(self.file_path)

    def test_with_options_avg_chart_simple(self):
        opt = GraphOption(upper_part_text='This is a test',
                          fibonacci_bands=True)
        gp = GraphPainter(datas=self.coll_single_trade_point,
                          token_info=self.ti,
                          options=opt)
        chart_img = gp.paint_simple_chart()
        chart_img.save(self.file_path)

    def test_with_options_rsi(self):
        opt = GraphOption(upper_part_text='This is a test',
                          rsi=True)
        gp = GraphPainter(datas=self.coll_ohcl,
                          token_info=self.ti,
                          options=opt)
        chart_img = gp.paint_candlestick()
        chart_img.save(self.file_path)

    def test_with_options_bb(self):
        opt = GraphOption(upper_part_text='This is a test',
                          bollinger_bands=True)
        gp = GraphPainter(datas=self.coll_ohcl,
                          token_info=self.ti,
                          options=opt)
        chart_img = gp.paint_candlestick()
        chart_img.save(self.file_path)

    def test_with_options_fibo(self):
        opt = GraphOption(upper_part_text='This is a test',
                          fibonacci_bands=True)
        gp = GraphPainter(datas=self.coll_ohcl,
                          token_info=self.ti,
                          options=opt)
        chart_img = gp.paint_candlestick()
        chart_img.save(self.file_path)

    def test_with_options_average(self):
        opt = GraphOption(upper_part_text='This is a test',
                          average=True)
        gp = GraphPainter(datas=self.coll_ohcl,
                          token_info=self.ti,
                          options=opt)
        chart_img = gp.paint_candlestick()
        chart_img.save(self.file_path)

    def test_with_options_finance(self):
        opt = GraphOption(upper_part_text='This is a test',
                          finance=True)
        gp = GraphPainter(datas=self.coll_ohcl,
                          token_info=self.ti,
                          options=opt)
        chart_img = gp.paint_candlestick()
        chart_img.save(self.file_path)

    def test_with_options_all(self):
        opt = GraphOption(upper_part_text='This is a test',
                          bollinger_bands=True,
                          fibonacci_bands=True,
                          rsi=True,
                          average=True,
                          finance=True)
        gp = GraphPainter(datas=self.coll_ohcl,
                          token_info=self.ti,
                          options=opt)
        chart_img = gp.paint_candlestick()
        chart_img.save(self.file_path)

    def test_if_speed_gets_better(self):
        """Just checking that the first time that we cast a GraphOption() object is slower than the other times."""
        for i in range(1, 10):
            t0 = time.time()
            opt = GraphOption()
            gp = GraphPainter(datas=self.coll_ohcl,
                              token_info=self.ti,
                              options=opt)
            res = gp._generate_candlestick()
            chart_img = Image.open(res)
            t1 = time.time()
            pprint(f"Elapsed time for run {i}: {t1 - t0}")

    def test_paint_candlestick_repetition(self):
        """Paint a full candlestick"""
        for i in range(1, 10):
            opt = GraphOption(upper_part_text="Hello")
            gp = GraphPainter(datas=self.coll_ohcl,
                              token_info=self.ti,
                              options=opt)
            t0 = time.time()
            res = gp.paint_candlestick()
            t1 = time.time()
            pprint(f"Elapsed time for run {i}: {t1 - t0}")

    def test_painting_from_cro(self):
        opt = GraphOption(upper_part_text="Hello")
        gp = GraphPainter(datas=self.coll_ohcl_cro,
                          token_info=self.ti,
                          options=opt)
        res = gp.paint_candlestick()
        res.show()
