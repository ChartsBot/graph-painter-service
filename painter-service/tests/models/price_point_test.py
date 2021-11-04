import json
import time
from datetime import datetime
import unittest
from pprint import pprint

from models.price_point import CollectionOhcl, CollectionSingleTradePoint, SingleTradePoint
from tests.test_elements import EXAMPLE_JSON_COLLECTION_SINGLE_TRADE_POINT


class PricePointsTest(unittest.TestCase):

    def test_casting_stuff(self):
        res = CollectionSingleTradePoint()
        pprint(res)
        stp = SingleTradePoint(date=datetime.fromtimestamp(int(time.time())),
                               value=100)
        res = CollectionSingleTradePoint(coll=[stp])
        pprint(res)
        pprint(res.dict())

    def test_casting_stuff_signle_trade_point_collection(self):
        json_class = json.loads(EXAMPLE_JSON_COLLECTION_SINGLE_TRADE_POINT)
        res = CollectionSingleTradePoint(**json_class)
        pprint(res)
        self.assertEqual(res.size(), 100)

