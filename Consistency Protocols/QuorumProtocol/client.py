import quorum_pb2
import quorum_pb2_grpc
import grpc
import time
from concurrent import futures
import uuid
import datetime
import os.path
from google.protobuf.timestamp_pb2 import Timestamp

class ClientServices( quorum_pb2_grpc.ClientServicesServicer):
    def __init__(self):
        self.idfilename_mapping = {}

def run():
    client = ClientServices()
    port = input("Enter a port number: ")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    quorum_pb2_grpc.add_ClientServicesServicer_to_server(client, server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    print("Client started on port " + port)
    while True:
        print("1. Read request")
        print("2. Write request")
        print("3. Delete request")
        print("4. List of all replicas")
        print("5. Exit")
        print("6. Run the test script")
        input1 = input("Enter your choice: ")
        if(input1 == '1'):
            readRequest(port, client)
        elif(input1 == '2'):
            writeRequest(port, client)
        elif(input1 == '3'):
            deleteRequest(port, client)
        elif(input1 == '4'):
            listAllReplicas(port, client)
        elif(input1 == '5'):
            server.stop(0)
            print("Client stopped")
            break
        else:
            os.system('python test.py')

def readRequest(port, client):
    response = None
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = quorum_pb2_grpc.RegistryServerServicesStub(channel)
        response = stub.GetReadReplicas(quorum_pb2.Empty())
        print("Read replicas:")
        print(response.replica_list)
        print("---end---")
    channel.close()
    print("Choose a file: ")
    for fnames in client.idfilename_mapping.values():
        print(fnames)
    # print("or enter a new one: ")
    inp_name = input("File name: ")
    try:
        inp_id = client.idfilename_mapping.get(inp_name)
    except:
        print("You are trying to access a file that does not exist")
        return    
    # will always be an existing file
    print("updated idfilename_mapping:" + str(client.idfilename_mapping))
    response_list = []
    inp_id = client.idfilename_mapping.get(inp_name)
    for replica in response.replica_list:
        with grpc.insecure_channel(replica) as channel:
            stub = quorum_pb2_grpc.ReplicaServerServicesStub(channel)
            response = stub.ReadFile(quorum_pb2.ReadReplicaRequest(file_uuid=inp_id))
            response_list.append(response)
            print("Read response from "+ replica + ":")
            print(response.status)
            print(response.file_name)
            print(response.file_content)
            print(response.version)
            print("---end---")
    
    response_list.sort(key=lambda x: x.version.seconds, reverse=True)
    print("Sorted response list:")
    for item in response_list:
        print(item.status)
        print(item.file_name)
        print(item.file_content)
        print(item.version)
        print("---end---")
        #sucess + loop sort
    # print(response_list[0].status)
    # print(response_list[0].file_name)
    # print(response_list[0].file_content)
    # print(response_list[0].version)
    # print("---end---")




def writeRequest(port, client):
    response = None
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = quorum_pb2_grpc.RegistryServerServicesStub(channel)
        response = stub.GetWriteReplicas(quorum_pb2.Empty()).replica_list
        print("Write replicas:")
        print(response)
        print("---end---")
    channel.close()
    print("Enter a file name: ")
    for fnames in client.idfilename_mapping.values():
        print(fnames)
    print("or enter a new one: ")
    inp_name = input("File name: ")
    inp_id = None
    if inp_name in client.idfilename_mapping:
        inp_id = client.idfilename_mapping.get(inp_name)
    else:
        inp_id = str(uuid.uuid1())
        client.idfilename_mapping[inp_name] = inp_id
    print("updated idfilename_mapping:" + str(client.idfilename_mapping))
    inp_content = input("File content: ")
    response_list = []
    for replica in response:
        with grpc.insecure_channel(replica) as channel:
            stub = quorum_pb2_grpc.ReplicaServerServicesStub(channel)
            response = stub.WriteFile(quorum_pb2.WriteReplicaRequest(file_uuid=inp_id, file_name=inp_name, file_content=inp_content))
            response_list.append(response)
            print("Write response from "+ replica + ":")
            print(response.status)
            print(response.file_uuid)
            print(response.version)
            print("---end---")
    
    response_list.sort(key=lambda x: x.version.seconds, reverse=True)
    print("Sorted response list:")
    for item in response_list:
        print(item.status)
        print(item.file_uuid)
        print(item.version)
        print("---end---")

def deleteRequest(port, client):
    response = None
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = quorum_pb2_grpc.RegistryServerServicesStub(channel)
        response = stub.GetDeleteReplicas(quorum_pb2.Empty()).replica_list
        print("Delete replicas:")
        print(response)
        print("---end---")
    channel.close()
    print("Choose a file name from: ")
    for fnames in client.idfilename_mapping.values():
        print(fnames)
    inp_name = input("File name: ")
    inp_id = None
    if inp_name in client.idfilename_mapping:
        inp_id = client.idfilename_mapping.get(inp_name)
        # client.idfilename_mapping.pop(inp_name)
    else:
        print("You are trying to access a file that does not exist")
        return
    print("updated idfilename_mapping: " + str(client.idfilename_mapping))
    response_list = []
    for replica in response:
        with grpc.insecure_channel(replica) as channel:
            stub = quorum_pb2_grpc.ReplicaServerServicesStub(channel)
            response = stub.DeleteFile(quorum_pb2.DeleteReplicaRequest(file_uuid=inp_id))
            response_list.append(response)
            print("Delete response from "+ replica + ":")
            print(response.status)
            print("---end---")
    
    # response_list.sort(key=lambda x: x.version.seconds, reverse=True)
    # print("Sorted response list:")
    # for item in response_list:
    #     print(item.status)
    #     print("---end---")

def listAllReplicas(port, client):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = quorum_pb2_grpc.RegistryServerServicesStub(channel)
        response = stub.GetAllReplicas(quorum_pb2.Empty())
        print("All replicas:")
        print(response.replica_list)
        print("---end---")
    channel.close()


if __name__ == '__main__':
    run()