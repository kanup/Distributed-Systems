import os
import sys
import wordcount_pb2
import wordcount_pb2_grpc
import pickle
from utils import serve, MAPPER_START_PORT

INPUT_DIR = None
DIR = 'intermediate'
ID = None


class Mapper(wordcount_pb2_grpc.MapperServicer):

    def Map(self, request, context):
        # data = []
        # paths = request.path.split(',')

        # for path in paths:
        #     fp = open(f"{INPUT_DIR}/{path}", 'r')
        #     d = fp.readlines()
        #     fp.close()

        #     for line in d[1:]:
        #         data.append(line[:-1])

        # key_val = {}
        # for line in data:
        #     key, val = line.split(", ")

        #     if val.isdigit():
        #         tbl = 't1'
        #     else:
        #         tbl = 't2'

        #     if key not in key_val:
        #         key_val[key] = [(tbl, val)]
        #     else:
        #         key_val[key].append((tbl, val))

        data = []
        paths = request.path.split(',')

        for path in paths:
            fp = open(f"{INPUT_DIR}/{path}", 'r')
            d = fp.readlines()
            fp.close()

            for line in d[0:]:
                data.append(line.rstrip())

        key_val = {}
        words = []
        for line in data:
            words = line.split(" ")
            # print("words in a line")
            # print(words)
            for word in words:
                word = word.lower()
                
                if word not in key_val:
                    # print(f"{word} is not present")
                    key_val[str(word)] = [1]
                else:
                    # print(f"{word} is  present")
                    key_val[str(word)].append(1)



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

        return wordcount_pb2.Empty()


if __name__ == '__main__':
    try:
        ID = int(sys.argv[1])
        INPUT_DIR = sys.argv[2]
    except:
        ID = 1
        INPUT_DIR = 'input'

    MAPPER_START_PORT += ID

    serve(wordcount_pb2_grpc.add_MapperServicer_to_server, Mapper, str(MAPPER_START_PORT))
