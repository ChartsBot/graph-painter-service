import grpc
import os
from concurrent import futures
import protobuf.graphPainter_pb2_grpc as pb2_grpc
from service.grpc_server import GraphPainterGrpcServer

import json
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

SECRETS_PATH = os.environ.get('SECRETS_PATH')

with open(SECRETS_PATH + "graph-painter/config.json") as f:
    config = json.load(f)


def serve():
    logging.info("Starting grpc server")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    pb2_grpc.add_GraphPainterServiceServicer_to_server(GraphPainterGrpcServer(), server)
    server.add_insecure_port(f"[::]:{config['grpc']['port']}")
    server.start()
    logging.info("Started")
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
