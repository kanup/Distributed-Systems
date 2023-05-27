import os
import shutil
import time
from multiprocessing import Process
from utils import map_rpc, partition_rpc, reduce_rpc, split_files, MAPPER_START_PORT, REDUCER_START_PORT


def run_mapper(n, input_dir):
    cmd = f'python mapper.py {n} {input_dir}'
    # print(cmd)
    print("Starting  Mapper:", n + 1)
    os.system(cmd)


def run_reducer(n, N, output_dir):
    cmd = f'python reducer.py {n} {N} {output_dir}'
    # print(cmd)
    print("Starting Reducer:", n + 1)
    os.system(cmd)


def mapper(n, input_dir):
    paths = split_files(input_dir, 'input', n)

    for i in range(n):
        map_rpc(MAPPER_START_PORT + i, paths[i])
        time.sleep(1)


def partition(n):
    for i in range(n):
        partition_rpc(REDUCER_START_PORT + i)
        time.sleep(1)


def reduce(n):
    for i in range(n):
        reduce_rpc(REDUCER_START_PORT + i)
        time.sleep(1)


def main():
    shutil.rmtree('intermediate', ignore_errors=True)
    shutil.rmtree('debug', ignore_errors=True)

    INPUT_PATH = 'input'
    OUTPUT_PATH = 'output'
    N_MAPPERS = 2
    N_REDUCERS = 2

    FILE_START_NAME = 'input'
    paths = split_files(INPUT_PATH, FILE_START_NAME, N_MAPPERS)
    l = len(paths)
    N_MAPPERS = min(N_MAPPERS, l)
    N_REDUCERS = min(N_REDUCERS, N_MAPPERS)

    print("Number of Mappers:", N_MAPPERS)
    print("Number of Reducers:", N_REDUCERS)

    for i in range(N_MAPPERS):
        time.sleep(1)
        p = Process(target=run_mapper, args=(i, INPUT_PATH))
        p.start()

    for i in range(N_REDUCERS):
        time.sleep(1)
        p = Process(target=run_reducer, args=(i, N_REDUCERS, OUTPUT_PATH))
        p.start()

    print("Mapping Tasks")
    mapper(N_MAPPERS, INPUT_PATH)

    print("Partitioning Tasks")
    partition(N_REDUCERS)

    print("Reducing Tasks")
    reduce(N_REDUCERS)

    print("Done, now quit with ctrl+c")
    shutil.rmtree('intermediate')


if __name__ == '__main__':
    main()
