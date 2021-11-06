import os
import time
import unittest

import json
from pprint import pprint

import grpc
import protobuf.graphPainter_pb2_grpc as pb2_grpc
import protobuf.graphPainter_pb2 as pb2
from tests.test_elements import EXAMPLE_JSON_COLLECTION_SINGLE_TRADE_POINT, EXAMPLE_TOKEN_INFO, \
    EXAMPLE_JSON_GRAPH_OPTIONS_DARK_TEXT, EXAMPLE_JSON_COLLECTION_OHCL, EXAMPLE_JSON_GRAPH_OPTIONS_DARK_NO_TEXT_ABOVE
from tests.test_utils import read_image

SECRETS_PATH = os.environ.get('SECRETS_PATH')

with open(SECRETS_PATH + "graph-painter/config.json") as f:
    config = json.load(f)


class GraphPainterTest(unittest.TestCase):

    host = 'localhost'
    server_port = config['grpc']['port']
    channel = grpc.insecure_channel('{}:{}'.format(host, server_port))
    stub = pb2_grpc.GraphPainterServiceStub(channel)

    def test_greet_message(self):
        message = pb2.SayHelloMessage(message='Hello there.')
        res = self.stub.Greet(message)
        pprint(res)

    def test_chart(self):
        req = pb2.ChartRequest(datas=EXAMPLE_JSON_COLLECTION_SINGLE_TRADE_POINT,
                               tokenInfo=EXAMPLE_TOKEN_INFO.json(),
                               options=EXAMPLE_JSON_GRAPH_OPTIONS_DARK_TEXT)
        res = self.stub.PaintChart(req)
        img = read_image(res.image)
        img.show()

    def test_candlestick(self):
        req = pb2.ChartRequest(datas=EXAMPLE_JSON_COLLECTION_OHCL,
                               tokenInfo=EXAMPLE_TOKEN_INFO.json(),
                               options=EXAMPLE_JSON_GRAPH_OPTIONS_DARK_TEXT)
        res = self.stub.PaintCandlestick(req)
        img = read_image(res.image)
        img.show()

    def test_speed(self):
        req = pb2.ChartRequest(datas=EXAMPLE_JSON_COLLECTION_OHCL,
                               tokenInfo=EXAMPLE_TOKEN_INFO.json(),
                               options=EXAMPLE_JSON_GRAPH_OPTIONS_DARK_NO_TEXT_ABOVE)
        for i in range(1, 10):
            t0 = time.time()
            res = self.stub.PaintCandlestick(req)
            # read_image(res.image)
            t1 = time.time()
            pprint(f"Run {i} took {t1 - t0}s")

