import sys
from utils import *
import grpc
import asyncio
server=0
NAME = 's'+str(server)
PORT = str(5050+server)
PRIMARY = False
PRIMARY_IP = None

files = {}

servers = []
background_tasks = []
async def write_to_servers(filename, content, fileid):
    for ip in servers:
        res =await rpc_server_write(ip, filename, content, fileid)
        print(f'{ip}: {res.status}')

async def delete_to_servers(fileid):
    for ip in servers:
        print("ip")
        res = await rpc_server_delete(ip, fileid)
        print(f'{ip}: {res.status}')

def result_return(res):
    return res

async def perform(op, req):
    await get_servers()

    fileid = req.fileid

    if op == 'WRITE':
        filename = req.filename
        content = req.content
        primary_res=write_operation(req, NAME, files)
        task = asyncio.create_task(write_to_servers(filename, content, fileid))
        background_tasks.append(task)
        return primary_res
    else:
        res=delete_operation(req, NAME, files)
        task = asyncio.create_task(delete_to_servers(fileid))
        background_tasks.append(task)
        return res


class Server(blocking_pb2_grpc.ServerServicer):

    async def Primary(self, request, context):
        return await perform(request.operation, request)

    def Write(self, request, context):
        return write_operation(request, NAME, files)

    def Delete(self, request, context):
        return delete_operation(request, NAME, files)

    def ReadReq(self, request, context):
        status, res = read_check(request, NAME, files)
        if not status:
            return res

        return read_operation(request, NAME, files)

    async def WriteReq(self, request, context):
        status, res = write_check(request, NAME, files)
        if not status:
            return res

        if PRIMARY:
            return await perform('WRITE', request)
        
        res = await rpc_primary(PRIMARY_IP, 'WRITE', request.fileid, request.filename, request.content)
        print('f')
        print("Response from Primary:", res.status)
        return res

    async def DeleteReq(self, request, context):
        status, res = delete_check(request, NAME, files)
        if not status:
            return res

        if PRIMARY:
            return await perform('DELETE', request)

        res = await rpc_primary(PRIMARY_IP, 'DELETE', request.fileid, '', '')
        print("Response from Primary:", res.status)
        return res


async def register(NAME,PORT):
    global PRIMARY, PRIMARY_IP
    channel=grpc.aio.insecure_channel('localhost:8888')
    stub = blocking_pb2_grpc.RegistryServerStub(channel)
    res =  await stub.RegisterServer( blocking_pb2.RegisterRequest(
        name=NAME,
        ipaddress='localhost:' + str(PORT)
    ))
    PRIMARY = res.primary
    PRIMARY_IP = res.primary_ipaddress
    await channel.close()

    print("Status:", res.status)
    print("Primary IP Address:", res.primary_ipaddress)
    print("Primary:", res.primary)


async def get_servers():
    global servers
    res = await rpc_registry_get_servers('localhost:8888')
    res = list(res.listOfServers)
    for item in res:
        _, ip = item.split('-')
        if ip != PRIMARY_IP and ip not in servers:
            servers.append(ip)


async def serve(NAME,PORT):
    await register(name,port)
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    blocking_pb2_grpc.add_ServerServicer_to_server(Server(), server)
    server.add_insecure_port('[::]:' + PORT)
    await server.start()
    print("Server started, listening on " + PORT)
    
    await server.wait_for_termination()
    


if __name__ == '__main__':
    name=""
    port=""
    print(sys.argv[1])
    server = int(sys.argv[1])
    name = 's'+str(server)
    port = str(5050+server)
    NAME = name
    PORT = port
    
    try:
        asyncio.run(serve(NAME,port))
        
        # serve(port)
    except KeyboardInterrupt:
        print("Server shutting down")
