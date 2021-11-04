import unittest
import json

from PIL import Image

from graph.graph_painter import GraphPainter
from models.graph_options import GraphOption
from models.price_point import CollectionSingleTradePoint
from models.token_info import TokenInfo
from tests.test_elements import EXAMPLE_JSON_COLLECTION_SINGLE_TRADE_POINT


class GraphPainterTest(unittest.TestCase):
    json_class = json.loads(EXAMPLE_JSON_COLLECTION_SINGLE_TRADE_POINT)
    coll_single_trade_point = CollectionSingleTradePoint(**json_class)
    ti: TokenInfo = TokenInfo(name='Bitscoin')
    file_path = "/home/ben/Crypto/tg-bots/graph-painter-service/painter-service/tests/tmp/img.png"

    def test_painting(self):
        gp = GraphPainter()

        opt = GraphOption()
        res = gp._generate_chart(datas=self.coll_single_trade_point,
                                 token_info=self.ti,
                                 options=opt)
        chart_img = Image.open(res)
        # chart_img.show()
        chart_img.save(self.file_path)

    def test_painting_with_watermark(self):
        gp = GraphPainter()
        opt = GraphOption(watermark='TESTTESTTEST')
        res = gp._generate_chart(datas=self.coll_single_trade_point,
                                 token_info=self.ti,
                                 options=opt)
        chart_img = Image.open(res)
        chart_img.save(self.file_path)
