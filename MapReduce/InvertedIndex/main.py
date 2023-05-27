import os
import shutil
import time
import subprocess
from utils import map_rpc, partition_rpc, reduce_rpc, split_files, MAPPER_START_PORT, REDUCER_START_PORT


def run_mapper(n, input_dir):
    cmd = f'python mapper.py {n} {input_dir}'
    print(cmd)
    os.system(cmd)


def run_reducer(n, N, output_dir):
    cmd = f'python reducer.py {n} {N} {output_dir}'
    print(cmd)
    os.system(cmd)


def mapper(n, input_dir):
    paths = split_files(input_dir, 'input', n)

    for i in range(n):
        if(i<len(paths)):
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

    INPUT_PATH = './input2'
    OUTPUT_PATH = './output2'
    N_MAPPERS = 3
    N_REDUCERS = 3
    with open("config.txt") as config:
        config_values = config.readlines()
        for line in config_values:
            input_line=line.split("=")
            if(input_line[0].strip()=="Mappers"):
                N_MAPPERS=int(input_line[1].strip())
            elif(input_line[0].strip()=="Reducers"):
                N_REDUCERS=int(input_line[1].strip())
    print(N_MAPPERS)
    print(N_REDUCERS)
    paths = split_files(INPUT_PATH, 'input', N_MAPPERS)
    l = len(paths)
    N_MAPPERS = min(N_MAPPERS, l)
    N_REDUCERS = min(N_REDUCERS,N_MAPPERS)

    for i in range(N_MAPPERS):
        # process = subprocess.Popen(['python', 'path/to/your/script.py'])
        # p = Process(target=run_mapper, args=(i, INPUT_PATH))
        # p.start()
        p=subprocess.Popen(['python3', 'mapper.py', str(i), INPUT_PATH])
        time.sleep(1)

    for i in range(N_REDUCERS):
        p=subprocess.Popen(['python3', 'reducer.py', str(i), str(N_REDUCERS), OUTPUT_PATH])
        # p = Process(target=run_reducer, args=(i, N_REDUCERS, OUTPUT_PATH))
        # p.start()
        time.sleep(1)

    time.sleep(1)
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
