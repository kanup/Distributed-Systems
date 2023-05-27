import sys
import unittest
from multiprocessing import Process
import uuid
import os
import time
import grpc
import grpc
import quorum_pb2
import quorum_pb2_grpc


mappings = {}

names = ['ca1', 'ca2', 'ca3']
ports = ['4001', '4002', '4003']
n = 3
n_r = 2
n_w = 2

def run_registry():
    os.system(f'python registryServer.py {n} {n_r} {n_w}')
    time.sleep(3)
    # time.sleep(2)
    # os.system('3')
    # time.sleep(2)
    # os.system('2')
    # time.sleep(2)
    # os.system('2')


def run_server(name, port):
    os.system(f'python server.py {name} {port}')
    time.sleep(3)
   


def readRequest(inp_name):
    response = None
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = quorum_pb2_grpc.RegistryServerServicesStub(channel)
        response = stub.GetReadReplicas(quorum_pb2.Empty())
        
    channel.close()
    try:
        inp_id = mappings.get(inp_name)
    except:
        print("You are trying to access a file that does not exist")
        return    
    response_list = []
    inp_id = mappings.get(inp_name)
    for replica in response.replica_list:
        with grpc.insecure_channel(replica) as channel:
            stub = quorum_pb2_grpc.ReplicaServerServicesStub(channel)
            response = stub.ReadFile(quorum_pb2.ReadReplicaRequest(file_uuid=inp_id))
            response_list.append(response)
            
    
    response_list.sort(key=lambda x: x.version.seconds, reverse=True)
    return response_list[0]
    




def writeRequest_here(inp_name, inp_content):
    response = None
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = quorum_pb2_grpc.RegistryServerServicesStub(channel)
        response = stub.GetWriteReplicas(quorum_pb2.Empty()).replica_list
      
    channel.close()
   
    inp_id = None
    if inp_name in mappings:
        inp_id = mappings.get(inp_name)
    else:
        inp_id = str(uuid.uuid1())
        mappings[inp_name] = inp_id
    
    response_list = []
    for replica in response:
        with grpc.insecure_channel(replica) as channel:
            stub = quorum_pb2_grpc.ReplicaServerServicesStub(channel)
            response = stub.WriteFile(quorum_pb2.WriteReplicaRequest(file_uuid=inp_id, file_name=inp_name, file_content=inp_content))
            response_list.append(response)
            
    
    response_list.sort(key=lambda x: x.version.seconds, reverse=True)
    return response_list[0]

def deleteRequest_here(inp_name):
    response = None
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = quorum_pb2_grpc.RegistryServerServicesStub(channel)
        response = stub.GetDeleteReplicas(quorum_pb2.Empty()).replica_list
       
    channel.close()
   
    inp_id = None
    if inp_name in mappings:
        inp_id = mappings.get(inp_name)
        # client.idfilename_mapping.pop(inp_name)
    else:
        print("You are trying to access a file that does not exist")
        return
    # print("updated idfilename_mapping: " + str(client.idfilename_mapping))
    response_list = []
    for replica in response:
        with grpc.insecure_channel(replica) as channel:
            stub = quorum_pb2_grpc.ReplicaServerServicesStub(channel)
            response = stub.DeleteFile(quorum_pb2.DeleteReplicaRequest(file_uuid=inp_id))
            response_list.append(response)
            # print("Delete response from "+ replica + ":")
            # print(response.status)
            # print("---end---")

    response_list.sort(key=lambda x: x.status, reverse=True)
    return response_list[0]

def listAllReplicas_here( client):
    response = None
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = quorum_pb2_grpc.RegistryServerServicesStub(channel)
        response = stub.GetAllReplicas(quorum_pb2.Empty())
    
       
    channel.close()
    return response.replica_list


class TestSystem(unittest.TestCase):
    def test1(self):
        res_write = writeRequest_here('hello.txt', 'Hello World')
        time.sleep(2)
        self.assertEqual(res_write.status, 'NEW FILE CREATED', "WRITE OPERATION FAILED")

    def test2(self):
        res_read = readRequest('hello.txt')
        time.sleep(1)
        self.assertEqual(res_read.status, 'SUCCESS', "READ OPERATION FAILED")

    def test3(self):
        res_write = writeRequest_here('bye.txt', 'World Bye')
        time.sleep(2)
        self.assertEqual(res_write.status, 'NEW FILE CREATED', "WRITE OPERATION FAILED")

    def test4(self):
        res_write = readRequest('bye.txt')
        time.sleep(2)
        self.assertEqual(res_write.status, 'SUCCESS', "READ OPERATION FAILED")
    
    def test5(self):
        res_delete = deleteRequest_here('bye.txt')
        time.sleep(2)
        self.assertEqual(res_delete.status, 'SUCCESS', "DELETE OPERATION FAILED")

    def test6(self):
        res_read_again = readRequest('bye.txt')
        time.sleep(2)
        self.assertEqual(res_read_again.status, 'FILE ALREADY DELETED', "READ OPERATION FAILED")


def main():
    p = Process(target=run_registry)
    p.start()
    time.sleep(3)

    for i in range(3):
        p = Process(target=run_server, args=(names[i], ports[i]))
        p.start()
        time.sleep(3)
        

    time.sleep(1)
    unittest.main()


if __name__ == '__main__':
    main()
