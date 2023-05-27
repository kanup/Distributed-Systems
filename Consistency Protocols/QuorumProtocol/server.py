import quorum_pb2
import quorum_pb2_grpc
import grpc
import time
from concurrent import futures
import uuid
import os.path
from google.protobuf import timestamp_pb2
from datetime import datetime
import sys



class ReplicaServerServices( quorum_pb2_grpc.ReplicaServerServicesServicer):
    def __init__(self, name):
        self.mapping = {}
        #{'file_uuid': (file_name, version)}
        self.name = name
    
    def ReadFile(self, request, context):
        if request.file_uuid in self.mapping:
            #file id exists in the mapping
            # print("file id exists in the mapping")
            file_content = ""
            # print(os.path.join(os.getcwd(), self.name, self.mapping.get(request.file_uuid)[0]))
            # print(os.path.exists(os.path.join(os.getcwd(), self.name, self.mapping.get(request.file_uuid)[0])))
            if os.path.exists(os.path.join(os.getcwd(), self.name, self.mapping.get(request.file_uuid)[0])):       
                #file also exists in the directory 
                # print("file also exists in the directory")
                f = open(os.path.join(os.getcwd(), self.name, self.mapping.get(request.file_uuid)[0]), 'r')
                while True:
                    line = f.readline()
                    file_content = file_content+ ' '+ line
                    if not line:
                        break
                f.close()
                return quorum_pb2.ReadReplicaResponse(status="SUCCESS", file_name=self.mapping.get(request.file_uuid)[0], file_content=file_content, version=self.mapping.get(request.file_uuid)[1])
            else:
                #file does not exist in the directory
                # print("file does not exist in the directory")
                return quorum_pb2.ReadReplicaResponse(status="FILE ALREADY DELETED", file_name="", file_content="", version=self.mapping.get(request.file_uuid)[1])
        else:
            #file id does not exist in the mapping
            # print("file id does not exist in the mapping")
            return quorum_pb2.ReadReplicaResponse(status="FILE DOES NOT EXIST", file_name="", file_content="", version=None)

    def WriteFile(self, request, context):
        if request.file_uuid in self.mapping:
            #file id exists in the mapping
            # print("file id exists in the mapping")
            if os.path.exists(os.path.join(os.getcwd(), self.name, self.mapping.get(request.file_uuid)[0])):
                #file also exists in the directory
                # print("file also exists in the directory")
                f = open(os.path.join(os.getcwd(), self.name, self.mapping.get(request.file_uuid)[0]), 'w')
                # print("file opened")
                f.write(request.file_content)
                # print("file written")
                timevar = timestamp_pb2.Timestamp()
                timevar.FromDatetime(datetime.utcnow())
                # print( "timenow: " + f'{timevar}' )
                # print("timebefore" + str(self.mapping[request.file_uuid][1]))
                self.mapping[request.file_uuid][1] = timevar     

                return quorum_pb2.WriteReplicaResponse(status="SUCCESS", file_uuid=request.file_uuid, version=self.mapping.get(request.file_uuid)[1])
            else:
                #file does not exist in the directory
                # print("file does not exist in the directory")
                return quorum_pb2.WriteReplicaResponse(status="ALREADY DELETED FILE CANNOT BE UPDATED", file_uuid=request.file_uuid, version=None)
        else:
            #file id does not exist in the mapping
            # print("file id does not exist in the mapping")
            for key, val in self.mapping.items():
                if val[0] == request.file_name:
                    #file name exists in the mapping
                    # print("file name already exists in the mapping")
                    return quorum_pb2.WriteReplicaResponse(status="FILE NAME ALREADY EXISTS", file_uuid=request.file_uuid, version=self.mapping.get(request.file_uuid)[1])
            
            #file name does not exist in the mapping
            # print("same file name does not exist in the mapping")
            f = open(os.path.join(os.getcwd(), self.name, request.file_name), 'w')
            f.write(request.file_content)
            f.close()
            timevar = timestamp_pb2.Timestamp()

            timevar.FromDatetime(datetime.utcnow())
            self.mapping[request.file_uuid] = [request.file_name, timevar]
            # print("new file created")
            # print(self.mapping.get(request.file_uuid))
            return quorum_pb2.WriteReplicaResponse(status="NEW FILE CREATED", file_uuid=request.file_uuid, version=None)
        
    def DeleteFile(self, request, context):
        if request.file_uuid in self.mapping:
            #file id exists in the mapping
            # print("file id exists in the mapping")
            if os.path.exists(os.path.join(os.getcwd(), self.name, self.mapping.get(request.file_uuid)[0])):
                #file also exists in the directory
                # print("file also exists in the directory")
                os.remove(os.path.join(os.getcwd(), self.name, self.mapping.get(request.file_uuid)[0]))
                self.mapping.pop(request.file_uuid)
                return quorum_pb2.DeleteReplicaResponse(status="SUCCESS")
            else:
                #file does not exist in the directory
                # print("file does not exist in the directory")
                return quorum_pb2.DeleteReplicaResponse(status="FILE ALREADY DELETED")
        else:
            #file id does not exist in the mapping
            # print("file id does not exist in the mapping")
            timevar = timestamp_pb2.Timestamp()
            timevar.FromDatetime(datetime.utcnow())
            self.mapping[request.file_uuid] = ["empty", timevar]
            # print("file id added to the mapping"+ f'{self.mapping}')
            return quorum_pb2.DeleteReplicaResponse(status="FILE DOES NOT EXIST")
        
def serve( port, replica_name):
    # port, replica_name = input("Enter the port number and name: ").split()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    quorum_pb2_grpc.add_ReplicaServerServicesServicer_to_server(ReplicaServerServices(replica_name), server)
    server.add_insecure_port('[::]:' + port)
    os.mkdir(os.path.join(os.getcwd(), replica_name))
    server.start()
    print("Replica Server started on port " + port)

    with grpc.insecure_channel('localhost:50051') as channel:
        stub = quorum_pb2_grpc.RegistryServerServicesStub(channel)
        response = stub.RegisterReplica(quorum_pb2.RegisterReplicaRequest(replica_ip="localhost", replica_port=port))
        print(response.msg) 
    channel.close()
    server.wait_for_termination()

if __name__ == '__main__':
    replica_name = sys.argv[1]
    port = sys.argv[2]
    serve( port, replica_name)