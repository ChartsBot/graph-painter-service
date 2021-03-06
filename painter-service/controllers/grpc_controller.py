"""Helper to analyse and process a grpc based request"""
import io

import json
import logging

import time

from graph.graph_painter import GraphPainter
from models.graph_options import GraphOption
from models.painting_types import PaintingType
from models.price_point import CollectionSingleTradePoint, CollectionOhcl, AbsCollection
from models.token_info import TokenInfo

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def process_chart_request(request, req_type: PaintingType):
    """Process a chart request based on the painting type required.
    Returns the image as a byte array representing a png"""
    t0 = time.time()
    datas, token_info, options = _analyse_chart_request(request, req_type)
    gp = GraphPainter(datas, token_info, options)
    match req_type:
        case PaintingType.CANDLESTICK:
            img = gp.paint_candlestick()
        case PaintingType.CHART:
            img = gp.paint_simple_chart()
    logging.debug(f"Took {time.time() - t0}s to paint the chart.")

    with io.BytesIO() as output:
        img.save(output, options.export_type)
        data = output.getvalue()
    logging.info(f"Took {time.time() - t0}s to process the chart.")
    return data


def _analyse_chart_request(request, req_type: PaintingType) -> (AbsCollection, TokenInfo, GraphOption):
    """Analyses a chart request and returns the casted classes"""
    json_class_collection = json.loads(request.datas)
    json_class_token_info = json.loads(request.tokenInfo)
    json_class_options = json.loads(request.options)
    match req_type:
        case PaintingType.CHART:
            datas = CollectionSingleTradePoint(**json_class_collection)
        case PaintingType.CANDLESTICK:
            datas = CollectionOhcl(**json_class_collection)
    token_info = TokenInfo(**json_class_token_info)
    options = GraphOption(**json_class_options)
    return datas, token_info, options
