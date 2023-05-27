
import datetime
import time
from anyio import sleep
import zmq
import pubsub_pb2 as pb
import threading
import base64
def getRequestFromStr(requestStr):
    request=pb.Request()
    requestStr=base64.b64decode(requestStr)
    request.ParseFromString(requestStr)
    body=base64.b64decode(request.body)
    return request,body


def getResponseFromStr(responseStr):
    response=pb.Response()
    # bytesResponse=bytes(responseStr,'utf-8')
    responseStr=base64.b64decode(responseStr)
    response.ParseFromString(responseStr)
    body=base64.b64decode(response.body)
    return response,body

def sendResponse(socket,realResponse):
    response=pb.Response()
    # bytesResponse=bytes(realResponse,'utf-8')
    realResponse=base64.b64encode(realResponse).decode('utf-8')
    response.body=realResponse
    response=base64.b64encode(response.SerializeToString()).decode('utf-8')
    socket.send_string(response)

def sendRequest(socket,method,body):
    request=pb.Request()
    body=base64.b64encode(body).decode('utf-8')
    request.body=body
    request.method=method
    request=base64.b64encode(request.SerializeToString()).decode('utf-8')
    socket.send_string(request)