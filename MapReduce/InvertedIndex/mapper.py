import os
import sys
import natural_join_pb2
import natural_join_pb2_grpc
import pickle
from utils import serve, MAPPER_START_PORT

INPUT_DIR = None
DIR = 'intermediate'
ID = None


class Mapper(natural_join_pb2_grpc.MapperServicer):

    def Map(self, request, context):
        print("mapper")
        data = []
        paths = request.path.split(',')

        key_val = {}
        for path in paths:
            fp = open(f"{INPUT_DIR}/{path}", 'r')
            lines = fp.readlines()
            for line in lines:
                line = line.strip()
                for word in line.split(" "):
                    word = word.strip().lower()
                    if word not in key_val:
                        key_val[word] = [path]
                    else:
                        if path not in key_val[word]:
                            key_val[word].append(path)
            fp.close()

        if not os.path.exists(DIR):
            os.mkdir(DIR)

        with open(f'{DIR}/mapper{ID}.dat', 'wb') as f:
            pickle.dump(key_val, f)

        if not os.path.exists('debug'):
            os.mkdir('debug')

        fp = open(f'debug/mapper{ID}', 'w')
        for key in key_val:
            fp.write(f'{key}, {key_val[key]}\n')
        fp.close()

        return natural_join_pb2.Empty()


if __name__ == '__main__':
    try:
        ID = int(sys.argv[1])
        INPUT_DIR = sys.argv[2]
    except:
        ID = 1
        INPUT_DIR = 'input'

    MAPPER_START_PORT += ID

    serve(natural_join_pb2_grpc.add_MapperServicer_to_server, Mapper, str(MAPPER_START_PORT))
