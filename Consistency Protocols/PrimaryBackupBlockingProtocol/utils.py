import os
import time
from concurrent import futures

import grpc

import blocking_pb2
import blocking_pb2_grpc


def rpc_primary(ip_address, operation, fileid, filename, content):
    with grpc.insecure_channel(ip_address) as channel:
        stub = blocking_pb2_grpc.ServerStub(channel)
        response = stub.Primary(blocking_pb2.PrimaryRequest(
            operation=operation,
            fileid=fileid,
            filename=filename,
            content=content
        ))
        return response


def rpc_server_write(ip_address, filename, content, fileid):
    with grpc.insecure_channel(ip_address) as channel:
        stub = blocking_pb2_grpc.ServerStub(channel)
        response = stub.Write(blocking_pb2.WriteRequest(filename=filename, content=content, fileid=fileid))
        return response


def rpc_server_delete(ip_address, fileid):
    with grpc.insecure_channel(ip_address) as channel:
        stub = blocking_pb2_grpc.ServerStub(channel)
        response = stub.Delete(blocking_pb2.DeleteRequest(fileid=fileid))
        return response


def rpc_client_read(ip_address, fileid):
    with grpc.insecure_channel(ip_address) as channel:
        stub = blocking_pb2_grpc.ServerStub(channel)
        response = stub.ReadReq(blocking_pb2.ReadRequest(fileid=fileid))
        return response


def rpc_client_delete(ip_address, fileid):
    with grpc.insecure_channel(ip_address) as channel:
        stub = blocking_pb2_grpc.ServerStub(channel)
        response = stub.DeleteReq(blocking_pb2.DeleteRequest(fileid=fileid))
        return response


def rpc_client_write(ip_address, filename, content, fileid):
    with grpc.insecure_channel(ip_address) as channel:
        stub = blocking_pb2_grpc.ServerStub(channel)
        response = stub.WriteReq(blocking_pb2.WriteRequest(filename=filename, content=content, fileid=fileid))
        return response


def rpc_registry_get_servers(ip_address):
    with grpc.insecure_channel(ip_address) as channel:
        stub = blocking_pb2_grpc.RegistryServerStub(channel)
        response = stub.GetServerList(blocking_pb2.ServerListRequest())
        return response


def read_check(request, name, files):
    if not os.path.exists(name):
        os.mkdir(name)

    if request.fileid not in files:
        return False, blocking_pb2.ReadResponse(
            status='FILE DOES NOT EXIST',
            filename="NULL",
            content="NULL",
            version="NULL"
        )

    fileid = request.fileid
    filename, timestamp = files[fileid]
    path = f'{name}/{filename}'

    if not os.path.exists(path):
        return False, blocking_pb2.ReadResponse(
            status='FILE ALREADY DELETED',
            filename="NULL",
            content="NULL",
            version="NULL"
        )
    return True, None


def write_check(request, name, files):
    filename = request.filename

    path = f'{name}/{filename}'

    if not os.path.exists(name):
        os.mkdir(name)

    if request.fileid not in files and os.path.exists(path):
        return False, blocking_pb2.WriteResponse(
            status='FILE WITH THE SAME NAME ALREADY EXISTS',
            fileid="NULL",
            version="NULL"
        )

    elif request.fileid in files and not os.path.exists(path):
        return False, blocking_pb2.WriteResponse(
            status='DELETED FILE CANNOT BE UPDATED',
            fileid="NULL",
            version="NULL"
        )

    return True, None


def delete_operation(request, name, files):
    if not os.path.exists(name):
        os.mkdir(name)

    fileid = request.fileid
    filename, timestamp = files[fileid]
    path = f'{name}/{filename}'
    os.remove(path)

    return blocking_pb2.DeleteResponse(
        status='SUCCESS'
    )


def read_operation(request, name, files):
    if not os.path.exists(name):
        os.mkdir(name)

    fileid = request.fileid
    filename, timestamp = files[fileid]
    path = f'{name}/{filename}'
    fp = open(path)
    content = fp.read()
    fp.close()

    return blocking_pb2.ReadResponse(
        status='SUCCESS',
        filename=filename,
        content=content,
        version=timestamp
    )


def write_operation(request, name, files):
    if not os.path.exists(name):
        os.mkdir(name)

    filename = request.filename
    fileid = request.fileid
    content = request.content
    timestamp = str(time.strftime("%d/%m/%Y %H:%M:%S"))

    files[fileid] = (filename, timestamp)
    path = f'{name}/{filename}'

    fp = open(path, 'w')
    fp.write(content)
    fp.close()

    return blocking_pb2.WriteResponse(
        status='SUCCESS',
        fileid=fileid,
        version=timestamp
    )


def delete_check(request, name, files):
    if not os.path.exists(name):
        os.mkdir(name)

    if request.fileid not in files:
        return False, blocking_pb2.DeleteResponse(
            status='FILE DOES NOT EXIST'
        )

    fileid = request.fileid
    filename, timestamp = files[fileid]

    if request.fileid in files and not os.path.exists(f'{name}/{filename}'):
        return False, blocking_pb2.DeleteResponse(
            status='FILE ALREADY DELETED'
        )
    return True, None
