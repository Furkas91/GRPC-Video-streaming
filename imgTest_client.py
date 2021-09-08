from __future__ import print_function

import grpc
import cv2
import numpy as np

import imageTest_pb2
import imageTest_pb2_grpc
import skvideo.io

URL = "D:\\Data\\video\\vid_0_2021-08-30T16-41-36-070547.mp4"


def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = imageTest_pb2_grpc.ImageTestStub(channel)
    # temp = cv2.imread('/home/nirvan/img_one.png')
    # for response in stub.Analyse(generateRequests()):
    #     print(np.frombuffer(response.reply, dtype=np.int32))
    UnaryStream(stub)


def generateRequests():
    cap = cv2.VideoCapture("rtsp://admin:1qaz2wsx@192.168.1.17:554/cam/realmonitor?channel=1&subtype=0")
    i = 0
    if cap.isOpened():
        print("the connection is established")
    else:
        print("connection error")
    cnt = 1
    while cap.isOpened():

        _, frame = cap.read()
        print(frame.shape)
        # print(frame.dtype)
        # frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        frame = bytes(frame)
        yield imageTest_pb2.MsgRequest(img=frame)


def UnaryStream(stub):
    cap = cv2.VideoCapture("rtsp://admin:1qaz2wsx@192.168.1.17:554/cam/realmonitor?channel=1&subtype=0")
    i = 0
    if cap.isOpened():
        print("the connection is established")
    else:
        print("connection error")
    cnt = 1
    while cap.isOpened():

        _, frame = cap.read()
        print(frame.shape)
        # frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        frame = bytes(frame)
        res = stub.UnaryAnalyse(imageTest_pb2.MsgRequest(img=frame))
        print(np.frombuffer(res.reply, dtype=np.int32))


if __name__ == '__main__':
    run()
