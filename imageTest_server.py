from concurrent import futures
import time
import cv2
import grpc
import base64
import numpy as np
import imageTest_pb2
import imageTest_pb2_grpc

# from main import *
# from people_counter import *

_ONE_DAY_IN_SECONDS = 0


class Greeter(imageTest_pb2_grpc.ImageTestServicer):
    ttt=0

    def Analyse(self, request_iterator, context):
        cnt = 1
        i = 0
        bg_subtractor = cv2.createBackgroundSubtractorMOG2()
        ppl_counter = None
        ttt = 0
        flag = 1  # -1 is skip. 1 is dont skip
        for req in request_iterator:
            frame = np.frombuffer(req.img, dtype=np.uint8)
            # print(frame.dtype)
            frame = frame.reshape( (1080, 1920, 3) )
            #frame = np.array(frame, dtype = np.uint8 )

            # if ppl_counter is None:
            #     ppl_counter = PeopleCounter(frame.shape[:2], DIVIDER1)
            input()
            # This line will currently not work as the people counting code is not there. Replace this line with whatever processing you want to do
            # do on the streamed video. 'processed' is the frame of the resulting video after processing.
            # processed, fg_mask = process_frame(frame, bg_subtractor,ppl_counter)

            # display processed video
            cv2.imshow('Processed Image', frame)
            cv2.waitKey(1)
            print('time diff= ' + str(time.time() - ttt))
            ttt = time.time()
            bbox = np.asarray([185, 186, 50, 12])
            print(bbox.dtype)
            # ppl_counter.people_count1 is the current count of people. Replace it with whatever value you want to continuosly send back to the client
            # This line will send a value back to the client for each frame.
            yield imageTest_pb2.MsgReply(reply=bbox.tobytes())

    def UnaryAnalyse(self, request, context):
        frame = np.frombuffer(request.img, dtype=np.uint8)
        frame = frame.reshape((1080, 1920, 3))
        # frame = np.array(frame, dtype=np.uint8)
        cv2.imshow('Processed Image', frame)
        cv2.waitKey(1)
        #input()
        print('time diff= ' + str(time.time() - self.ttt))
        bbox = np.asarray([185, 186, 50, 12])
        self.ttt = time.time()
        return imageTest_pb2.MsgReply(reply=bbox.tobytes())


def serve():
    channel_opt = [('grpc.max_send_message_length', 3 * 1080 * 2000),
                   ('grpc.max_receive_message_length', 3 * 1080 * 2000)]

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10), options=channel_opt)
    imageTest_pb2_grpc.add_ImageTestServicer_to_server(Greeter(), server)
    server.add_insecure_port('localhost:50051')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
