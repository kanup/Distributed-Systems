import os
import pickle
import sys
import natural_join_pb2
import natural_join_pb2_grpc
from utils import serve, REDUCER_START_PORT, split_files, partition_index, fun

N_PARTITIONS = None
DIR = 'intermediate'
OUTPUT_DIR = None
ID = None


class Reducer(natural_join_pb2_grpc.ReducerServicer):

    def Partition(self, request, context):
        data = fun(ID, DIR, N_PARTITIONS)

        partitions = []

        for i in range(N_PARTITIONS):
            partitions.append([])

        for i in range(N_PARTITIONS):
            partition = f"{DIR}/partition{i}.dat"
            if os.path.exists(partition):
                with open(partition, 'rb') as fp:
                    partitions[i] = pickle.load(fp)

        for key_index in range(len(data)):
            key=data[key_index][0]
            index = partition_index(key, N_PARTITIONS)
            index=int(index)
            partition = partitions[index]
            partition.append((key, data[key_index][1]))
            # [key] = data[key]
            

        for i in range(N_PARTITIONS):
            partition = f"{DIR}/partition{i}.dat"
            with open(partition, 'wb') as fp:
                pickle.dump(partitions[i], fp)

        return natural_join_pb2.Empty()

    def Reduce(self, request, context):
        if not os.path.exists(OUTPUT_DIR):
            os.mkdir(OUTPUT_DIR)

        partition = f'{DIR}/partition{ID}.dat'

        with open(partition, 'rb') as fp:
            inter_data = pickle.load(fp)
        inter_data.sort(key=lambda x: x[0])

        fp = open(f'debug/partition{ID}', 'w')
        for key in inter_data:
            fp.write(f'{key}\n')
        fp.close()

        data = {}
        for key, val in inter_data:
            if key not in data:
                data[key] = []
            for file in val:
                data[key].append(file)
        

        

        path = f"{OUTPUT_DIR}/reducer{ID}.txt"
        fp = open(path, 'w')
        fp.write("word, document list \n")

        # Cross Join
        for key in data:
            fp.write(f"{key}, {data[key]}\n")
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
