import sys
from utils import *

NAME = 'Amazon'
PORT = '5050'
PRIMARY = False
PRIMARY_IP = None

files = {}

servers = []


def perform(op, req):
    get_servers()

    fileid = req.fileid

    if op == 'WRITE':
        filename = req.filename
        content = req.content
        for ip in servers:
            res = rpc_server_write(ip, filename, content, fileid)
            print(f'{ip}: {res.status}')
        return write_operation(req, NAME, files)

    for ip in servers:
        res = rpc_server_delete(ip, fileid)
        print(f'{ip}: {res.status}')
    return delete_operation(req, NAME, files)


class Server(blocking_pb2_grpc.ServerServicer):

    def Primary(self, request, context):
        return perform(request.operation, request)

    def Write(self, request, context):
        return write_operation(request, NAME, files)

    def Delete(self, request, context):
        return delete_operation(request, NAME, files)

    def ReadReq(self, request, context):
        status, res = read_check(request, NAME, files)
        if not status:
            return res

        return read_operation(request, NAME, files)

    def WriteReq(self, request, context):
        status, res = write_check(request, NAME, files)
        if not status:
            return res

        if PRIMARY:
            return perform('WRITE', request)

        res = rpc_primary(PRIMARY_IP, 'WRITE', request.fileid, request.filename, request.content)
        print("Response from Primary:", res.status)
        return res

    def DeleteReq(self, request, context):
        status, res = delete_check(request, NAME, files)
        if not status:
            return res

        if PRIMARY:
            return perform('DELETE', request)

        res = rpc_primary(PRIMARY_IP, 'DELETE', request.fileid, '', '')
        print("Response from Primary:", res.status)
        return res


def register():
    global PRIMARY, PRIMARY_IP
    with grpc.insecure_channel('localhost:8888') as channel:
        stub = blocking_pb2_grpc.RegistryServerStub(channel)
        res = stub.RegisterServer(blocking_pb2.RegisterRequest(
            name=NAME,
            ipaddress='localhost:' + str(PORT)
        ))
        PRIMARY = res.primary
        PRIMARY_IP = res.primary_ipaddress

        print("Status:", res.status)
        print("Primary IP Address:", res.primary_ipaddress)
        print("Primary:", res.primary)


def get_servers():
    global servers
    res = rpc_registry_get_servers('localhost:8888')
    res = list(res.listOfServers)
    for item in res:
        _, ip = item.split('-')
        if ip != PRIMARY_IP:
            servers.append(ip)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    blocking_pb2_grpc.add_ServerServicer_to_server(Server(), server)
    server.add_insecure_port('[::]:' + PORT)
    server.start()
    print("Server started, listening on " + PORT)
    server.wait_for_termination()


if __name__ == '__main__':
    if len(sys.argv) == 3:
        NAME = sys.argv[1]
        PORT = sys.argv[2]

    register()
    try:
        serve()
    except KeyboardInterrupt:
        print("Server shutting down")
