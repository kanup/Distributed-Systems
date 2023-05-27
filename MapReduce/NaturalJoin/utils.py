import os
import pickle
from concurrent import futures
import grpc
import natural_join_pb2
import natural_join_pb2_grpc

MAPPER_START_PORT = 15000
REDUCER_START_PORT = 20000

GROUPS = []


def serve(servicer, service, port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    servicer(service(), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    server.wait_for_termination()


def map_rpc(port, path):
    ipaddress = f'localhost:{port}'
    with grpc.insecure_channel(ipaddress) as channel:
        stub = natural_join_pb2_grpc.MapperStub(channel)
        stub.Map(natural_join_pb2.ProcessRequest(path=path))


def partition_rpc(port):
    ipaddress = f'localhost:{port}'
    with grpc.insecure_channel(ipaddress) as channel:
        stub = natural_join_pb2_grpc.ReducerStub(channel)
        stub.Partition(natural_join_pb2.ProcessRequest())


def reduce_rpc(port):
    ipaddress = f'localhost:{port}'
    with grpc.insecure_channel(ipaddress) as channel:
        stub = natural_join_pb2_grpc.ReducerStub(channel)
        stub.Reduce(natural_join_pb2.ProcessRequest())


def split_files(_dir, start, n):
    # Splits files in "dir" starting with "start" into n partitions
    files = []
    for filename in os.listdir(_dir):
        if filename.startswith(start):
            files.append(filename)

    l = len(files)

    div = l // n
    rem = l % n

    res = []
    i = 0
    while i < l:
        path = ''
        size = div
        if rem > 0:
            size += 1
            rem -= 1
        for j in range(0, size):
            path += files[i + j] + ','
        path = path[:-1]
        res.append(path)
        i += size
    return res


def print_partitions():
    start = 'A'
    for i, val in enumerate(GROUPS):
        print(f"\tPartition {i + 1}: ", end="")
        end = chr(ord(start) + val - 1)
        print(f"{start} - {end}")
        start = chr(ord(end) + 1)


def form_partitions(n):
    global GROUPS
    div = 26 // n
    rem = 26 % n

    groups = []
    total = 0
    while True:
        size = div
        if rem > 0:
            size += 1
            rem -= 1
        total += size
        if total <= 26:
            groups.append(size)
        else:
            break
    GROUPS = groups


def partition_index(key, n):
    if len(GROUPS) == 0:
        form_partitions(n)

    k = ord(key[0]) - ord('A') + 1
    total = 0
    for i, val in enumerate(GROUPS):
        total += val
        if total >= k:
            return i

    return None


def read_mapper_output(_id, _dir, n):
    FILE_START_NAME = 'mapper'
    mapper_splits = split_files(_dir, FILE_START_NAME, n)
    res = {}
    paths = mapper_splits[_id].split(',')
    for path in paths:
        with open(f"{_dir}/{path}", 'rb') as f:
            d = pickle.load(f)
            for k in d:
                if k not in res:
                    res[k] = d[k]
                else:
                    for i in d[k]:
                        res[k].append(i)
    return res


def find_common(headings):
    res = []
    if headings[0][0] in headings[1]:
        res.append(0)
    else:
        res.append(1)

    for a, b, c in headings[1:]:
        if a == headings[0][res[0]]:
            res.append(0)
        else:
            res.append(1)

    return res
