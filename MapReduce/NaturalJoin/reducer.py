import os
import pickle
import sys

import natural_join_pb2
import natural_join_pb2_grpc
from utils import serve, REDUCER_START_PORT, partition_index, read_mapper_output, print_partitions

N_PARTITIONS = None
DIR = 'intermediate'
OUTPUT_DIR = None
ID = None


class Reducer(natural_join_pb2_grpc.ReducerServicer):

    def Partition(self, request, context):
        data = read_mapper_output(ID, DIR, N_PARTITIONS)

        partitions = []

        for i in range(N_PARTITIONS):
            partitions.append(dict())

        for i in range(N_PARTITIONS):
            partition = f"{DIR}/partition{i}.dat"
            if os.path.exists(partition):
                with open(partition, 'rb') as fp:
                    partitions[i] = pickle.load(fp)

        for key in data:
            index = partition_index(key, N_PARTITIONS)
            partition = partitions[index]

            if key not in partition:
                partition[key] = data[key]
            else:
                for d in data[key]:
                    partition[key].append(d)

        for i in range(N_PARTITIONS):
            partition = f"{DIR}/partition{i}.dat"
            with open(partition, 'wb') as fp:
                pickle.dump(partitions[i], fp)

        if ID == 0:
            print_partitions()

        return natural_join_pb2.Empty()

    def Reduce(self, request, context):
        if not os.path.exists(OUTPUT_DIR):
            os.mkdir(OUTPUT_DIR)

        partition = f'{DIR}/partition{ID}.dat'

        with open(partition, 'rb') as fp:
            data = pickle.load(fp)

        fp = open(f'debug/partition{ID}', 'w')
        for key in data:
            fp.write(f'{key}, {data[key]}\n')
        fp.close()

        fp = open(f"{DIR}/heading.txt", 'r')
        heading = fp.read()
        fp.close()

        path = f"{OUTPUT_DIR}/reducer{ID}.txt"
        fp = open(path, 'w')
        fp.write(heading)

        # Cross Join
        for key in data:
            first, second = [], []
            for t, val in data[key]:
                if t == 't1':
                    first.append(val)
                else:
                    second.append(val)

            if not (len(first) > 0 and len(second) > 0):
                continue
            for i, a in enumerate(first):
                for j, b in enumerate(second):
                    fp.write(f"{key}, {a}, {b}\n")
        fp.close()

        return natural_join_pb2.Empty()


if __name__ == '__main__':
    try:
        ID = int(sys.argv[1])
        N_PARTITIONS = int(sys.argv[2])
        OUTPUT_DIR = sys.argv[3]
    except:
        ID = 1
        N_PARTITIONS = 2
        OUTPUT_DIR = 'output'

    REDUCER_START_PORT += ID

    serve(natural_join_pb2_grpc.add_ReducerServicer_to_server, Reducer, str(REDUCER_START_PORT))
