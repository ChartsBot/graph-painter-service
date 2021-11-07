import io
import logging

import time
import unittest

import json
import pydantic
from PIL import Image
from controllers.grpc_controller import process_chart_request
from models.graph_options import GraphOption
from models.painting_types import PaintingType
from tests.test_elements import EXAMPLE_JSON_COLLECTION_SINGLE_TRADE_POINT, EXAMPLE_JSON_COLLECTION_OHCL, \
    EXAMPLE_TOKEN_INFO, EXAMPLE_JSON_GRAPH_OPTIONS_DARK_TEXT
from tests.test_utils import StubRequest, read_image


class GrpcControllerTest(unittest.TestCase):

    def test_grpc_chart(self):
        request = StubRequest(datas=EXAMPLE_JSON_COLLECTION_SINGLE_TRADE_POINT,
                              tokenInfo=EXAMPLE_TOKEN_INFO.json(),
                              options=EXAMPLE_JSON_GRAPH_OPTIONS_DARK_TEXT)
        res = process_chart_request(request, PaintingType.CHART)
        img = read_image(res)
        img.show()

    def test_grpc_candlestick(self):
        request = StubRequest(datas=EXAMPLE_JSON_COLLECTION_OHCL,
                              tokenInfo=EXAMPLE_TOKEN_INFO.json(),
                              options=EXAMPLE_JSON_GRAPH_OPTIONS_DARK_TEXT)
        res = process_chart_request(request, PaintingType.CANDLESTICK)
        img = read_image(res)
        img.show()

    def test_repetition(self):
        for i in range(0, 10):
            request = StubRequest(datas=EXAMPLE_JSON_COLLECTION_OHCL,
                                  tokenInfo=EXAMPLE_TOKEN_INFO.json(),
                                  options=EXAMPLE_JSON_GRAPH_OPTIONS_DARK_TEXT)
            res = process_chart_request(request, PaintingType.CANDLESTICK)

    def test_repetition_multiple_save_type(self):
        """Comparing time taken to cast the image as a PNG vs jpeg"""
        request = StubRequest(datas=EXAMPLE_JSON_COLLECTION_OHCL,
                              tokenInfo=EXAMPLE_TOKEN_INFO.json(),
                              options=EXAMPLE_JSON_GRAPH_OPTIONS_DARK_TEXT)
        res = process_chart_request(request, PaintingType.CANDLESTICK)  # processing it once so that the module can initialize without impacting the test
        t0 = time.time()
        for i in range(0, 11):
            res = process_chart_request(request, PaintingType.CANDLESTICK)
        time_jpeg = (time.time() - t0) / 10
        request = StubRequest(datas=EXAMPLE_JSON_COLLECTION_OHCL,
                              tokenInfo=EXAMPLE_TOKEN_INFO.json(),
                              options=EXAMPLE_JSON_GRAPH_OPTIONS_DARK_TEXT.replace('JPEG', 'PNG'))
        t0 = time.time()
        for i in range(0, 11):
            res = process_chart_request(request, PaintingType.CANDLESTICK)
        time_png = (time.time() - t0) / 10
        logging.info(f"Took average time of {time_jpeg} for jpeg")
        logging.info(f"Took average time of {time_png} for png")