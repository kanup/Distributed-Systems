import quorum_pb2
import quorum_pb2_grpc
import grpc
import time
from concurrent import futures
import uuid
import random
import sys

class RegistryServerServices(quorum_pb2_grpc.RegistryServerServicesServicer):
    def __init__(self, N, N_r, N_w):
        self.registry = []
        self.N = N
        self.N_r = N_r
        self.N_w = N_w

    def RegisterReplica(self, request, context):
        print( "Registering replica: " + request.replica_ip + ":" + request.replica_port)
        self.registry.append(request.replica_ip + ":" + request.replica_port)
        return quorum_pb2.RegisterReplicaResponse(msg="Replica registered successfully")
    
    def GetAllReplicas(self, request, context):
        listofreplicas = []
        for items in self.registry:
            listofreplicas.append(items)

        return quorum_pb2.GetAllReplicasResponse(replica_list=listofreplicas)
    
    def GetReadReplicas(self,request, context):
        read_set = set()
        while len(read_set) < self.N_r:
            read_set.add(self.registry[random.randint(0, self.N-1)])
        
        return quorum_pb2.GetReadReplicasResponse(replica_list=list(read_set))
    
    def GetWriteReplicas(self,request, context):
        write_set = set()
        while len(write_set) < self.N_w:
            write_set.add(self.registry[random.randint(0, self.N-1)])
        
        return quorum_pb2.GetWriteReplicasResponse(replica_list=list(write_set))

    def GetDeleteReplicas(self,request, context):
        delete_set = set()
        while len(delete_set) < self.N_w:
            delete_set.add(self.registry[random.randint(0, self.N-1)])
        
        return quorum_pb2.GetDeleteReplicasResponse(replica_list=list(delete_set))
    
    
def serve( n, n_r, n_w):
    port = '50051'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    while True:
        # n, n_r, n_w = input("Enter n, n_r, n_w : ").split()

        # n_r = int(input("Enter the number of read replicas: "))
        # n_w = int(input("Enter the number of write replicas: "))
        if (int(n_r) + int(n_w)) <= int(n) or int(n_w) <= (int(n)/2):
            print("Invalid input. Please try again.")
        else:
            break
    quorum_pb2_grpc.add_RegistryServerServicesServicer_to_server(RegistryServerServices(int(n), int(n_r), int(n_w)), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    print("Registry server started on port " + port)
    server.wait_for_termination()

if __name__ == '__main__':
    n = sys.argv[1]
    n_r = sys.argv[2]
    n_w = sys.argv[3]
    serve(int(n), int(n_r), int(n_w))