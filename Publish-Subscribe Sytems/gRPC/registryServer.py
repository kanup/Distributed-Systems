import pubsub_pb2
import pubsub_pb2_grpc
import grpc
import time 
from concurrent import futures 
import uuid

class RegistryServerServices(pubsub_pb2_grpc.RegistryServerServicesServicer):
    
    def __init__(self):
        self.maxServers = 2
        self.activeServers = {}

    def RegisterServer(self, request, context):
        print("JOIN REQUEST FROM LOCALHOST: " + request.port)
        if len(self.activeServers) >= self.maxServers:
            print("Registry-Server full")
            return pubsub_pb2.RegisterServerResponse(message="FAILURE")
        server_name = request.name
        self.activeServers[server_name] = ('localhost:'+request.port)
        print(type(self.activeServers))
        print(self.activeServers)
        return pubsub_pb2.RegisterServerResponse(message="SUCCESS")

    def GetServerList(self, request, context):
        print("SERVER LIST REQUEST FROM: " + request.address)
        listofservers = []
        count = 0
        for items in self.activeServers.items():
            listofservers.append(str(count) + ". " + items[0] + ":" + items[1])    
        return pubsub_pb2.ServerListResponse(listOfServers=listofservers)


def serve():
    port = '50051'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pubsub_pb2_grpc.add_RegistryServerServicesServicer_to_server(RegistryServerServices(), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()
    

if __name__ == '__main__':
    serve()
