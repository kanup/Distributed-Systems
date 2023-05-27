
import time
import zmq
import pubsub_pb2 as pb
import base64
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://127.0.0.1:1111")
print("Registry server started at tcp://localhost:1111")
from utils import *
registryServer=pb.RegistryServer()

def RegisterServer(serverAddress):
    try:
        # registryServer.activeServers.index(serverAddress)
        registryServer.activeServers.append(serverAddress)
        return "SUCCESS"
    except:
        return "FAIL"


    

while True:
    #  Wait for next request from client
    message = socket.recv()
    # print("Received request: %s" % message)
    request,body=getRequestFromStr(message)

    if request.method=="RegisterServer":
        # print(address.port)
        address=pb.address()
        address.ParseFromString(body)
        print('Join Request from server localhost:'+str(address.port))
        message=RegisterServer(address)
        # response=pb.Response()
        # response.body
        message=bytes(message,'utf-8')
        sendResponse(socket,message)
        # socket.send(response.SerializeToString())
        # print('server registered')
    elif request.method=="GetServers":
        print('Sever List Request from '+str(body.decode('utf-8')))
        print(len(registryServer.activeServers))
        # response=pb.Response()
        addressListResponse=pb.addressListResponse()
        addressListResponse.addresses.extend(registryServer.activeServers)
        print(addressListResponse.addresses)
        # response.body=addressListResponse.SerializeToString()
        # socket.send(response.SerializeToString())
        sendResponse(socket,addressListResponse.SerializeToString())
        print('servers sent')
    else:
        sendResponse(socket,bytes('wrong method','utf-8'))
    