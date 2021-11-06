import logging

import protobuf.graphPainter_pb2 as pb2
import protobuf.graphPainter_pb2_grpc as pb2_grpc
from controllers.grpc_controller import process_chart_request
from models.painting_types import PaintingType

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class GraphPainterGrpcServer(pb2_grpc.GraphPainterServiceServicer):

    def __init__(self, *args, **kwargs):
        pass

    def Greet(self, request, context):
        """Echoes back the greeting message sent by the client."""
        message = request.message
        logging.info(f"Received Greet message: {message}, sending message back.")
        return pb2.SayHelloMessage(message=message)

    def PaintCandlestick(self, request, context):
        """Returns a candlestick."""
        logging.info("Painting a candlestick.")
        img_raw = process_chart_request(request, PaintingType.CANDLESTICK)
        return pb2.ChartResponse(image=img_raw)

    def PaintChart(self, request, context):
        """Returns a simple chart."""
        logging.info("Painting a chart.")
        img_raw = process_chart_request(request, PaintingType.CHART)
        return pb2.ChartResponse(image=img_raw)


