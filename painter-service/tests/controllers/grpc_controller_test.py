import io
import unittest

import pydantic
from PIL import Image
from controllers.grpc_controller import process_chart_request
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

