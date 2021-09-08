from concurrent import futures
import time
import cv2
import grpc
import base64
import numpy as np
import processService_pb2
import processService_pb2_grpc

# from main import *
# from people_counter import *

_ONE_DAY_IN_SECONDS = 0


def np_to_proto_bbox(array):
    return processService_pb2.Bbox(xmin=array[0],
                                   ymin=array[1],
                                   boxwidth=array[2],
                                   boxheight=array[3])


class Greeter(processService_pb2_grpc.ProcessServiceServicer):
    ttt = 0

    def Detect(self, request, context):
        frame = np.frombuffer(request.img, dtype=np.uint8)
        frame = frame.reshape((1080, 1920, 3))
        # frame = np.array(frame, dtype=np.uint8)
        # cv2.imshow('Processed Image', frame)
        # cv2.waitKey(1)
        #input()
        print('time diff= ' + str(time.time() - self.ttt))
        bbox = [np.asarray([185, 186, 50, 12]), np.asarray([185, 186, 50, 12])]
        bbox = map(np_to_proto_bbox, bbox)
        self.ttt = time.time()
        return processService_pb2.MsgReply(reply=bbox)


def serve():
    channel_opt = [('grpc.max_send_message_length', 3 * 1080 * 2000),
                   ('grpc.max_receive_message_length', 3 * 1080 * 2000)]

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10), options=channel_opt)
    processService_pb2_grpc.add_ProcessServiceServicer_to_server(Greeter(), server)
    server.add_insecure_port('localhost:50051')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
