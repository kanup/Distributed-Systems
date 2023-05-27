from concurrent import futures

import grpc

import blocking_pb2
import blocking_pb2_grpc
import asyncio
PORT = '8888'

servers = dict()
primary_server = None


class RegistryServer(blocking_pb2_grpc.RegistryServerServicer):

    def RegisterServer(self, request, context):
        global primary_server
        print(f"JOIN REQUEST FROM {request.name}, {request.ipaddress}")
        if primary_server is None:
            primary_server = request.ipaddress
            primary = True
        else:
            primary = False
        servers[request.name] = request.ipaddress
        status = "SUCCESS"
        return blocking_pb2.RegisterResponse(status=status, primary_ipaddress=primary_server, primary=primary)

    def GetServerList(self, request, context):
        server_list = []
        for key in servers:
            server_list.append(key + "-" + servers[key])
        status = "SUCCESS"
        return blocking_pb2.ServerListResponse(status=status, listOfServers=server_list)


async def serve():
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    blocking_pb2_grpc.add_RegistryServerServicer_to_server(RegistryServer(), server)
    server.add_insecure_port('[::]:' + PORT)
    await server.start()
    print("Server started, listening on " + PORT)
    await server.wait_for_termination()


if __name__ == '__main__':
    try:
        asyncio.run(serve())
        # serve()
    except KeyboardInterrupt:
        print("Server shutting down")
