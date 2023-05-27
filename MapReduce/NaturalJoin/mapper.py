import os
import sys
import natural_join_pb2
import natural_join_pb2_grpc
import pickle
from utils import serve, MAPPER_START_PORT, find_common

INPUT_DIR = None
DIR = 'intermediate'
ID = None


class Mapper(natural_join_pb2_grpc.MapperServicer):

    def Map(self, request, context):
        if not os.path.exists(DIR):
            os.mkdir(DIR)

        data = []
        paths = request.path.split(',')

        headings = []
        for i, path in enumerate(paths):
            data.append([])
            fp = open(f"{INPUT_DIR}/{path}", 'r')
            d = fp.readlines()
            fp.close()

            a, b = d[0].split(", ")
            if path.find("table1") != -1:
                headings.append((a, b[:-1], 't1'))
            else:
                headings.append((a, b[:-1], 't2'))
            for line in d[1:]:
                data[i].append(line[:-1])

        common = find_common(headings)

        h1, h2 = '', ''
        key = headings[0][common[0]]
        for a, b, c in headings:
            if c == 't1':
                if a == key:
                    h1 = b
                else:
                    h1 = a
            else:
                if a == key:
                    h2 = b
                else:
                    h2 = a

        fp = open(f"{DIR}/heading.txt", 'w')
        fp.write(f"{key}, {h1}, {h2}\n")
        fp.close()

        key_val = {}
        for i, table in enumerate(data):
            for line in table:
                if common[i] == 0:
                    key, val = line.split(", ")
                else:
                    val, key = line.split(", ")

                if paths[i].find('table2') == -1:
                    tbl = 't1'
                else:
                    tbl = 't2'

                if key not in key_val:
                    key_val[key] = [(tbl, val)]
                else:
                    key_val[key].append((tbl, val))

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
