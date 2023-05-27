import sys
import unittest
from multiprocessing import Process
import uuid
from utils import *

files = {}

names = ['Google', 'Facebook', 'Microsoft']
ports = ['15001', '15002', '15003']


def run_registry():
    os.system('python registry_server.py')


def run_server(name, port):
    os.system(f'python server.py {name} {port}')


def read(ipaddress, filename):
    fileid = files[filename]
    response = rpc_client_read(ipaddress, fileid)
    # print("Status:", response.status)
    # print("Filename:", response.filename)
    # print("Content:", response.content)
    # print("Version:", response.version)
    return response


def write(ipaddress, filename, content):
    if filename in files:
        fileid = files[filename]
    else:
        fileid = str(uuid.uuid4())
    files[filename] = fileid

    response = rpc_client_write(ipaddress, filename, content, fileid)
    # print("Status:", response.status)
    # print("UUID:", response.fileid)
    # print("Version:", response.version)
    return response


def delete(ipaddress, filename):
    fileid = files[filename]
    response = rpc_client_delete(ipaddress, fileid)
    # print("Status:", response.status)
    return response


def get_available_servers(ipaddress):
    response = rpc_registry_get_servers(ipaddress)
    response = list(response.listOfServers)
    # for item in res:
    #     print(item)
    return response


class TestSystem(unittest.TestCase):
    def test1(self):
        res_write = write('localhost:15002', 'hello', 'Hello World')
        time.sleep(2)
        self.assertEqual(res_write.status, 'SUCCESS', "WRITE OPERATION FAILED")

    def test2(self):
        for port in ports:
            res_read = read(f'localhost:{port}', 'hello')
            time.sleep(1)
            self.assertEqual(res_read.status, 'SUCCESS', "READ OPERATION FAILED")

    def test3(self):
        res_delete = delete('localhost:15003', 'hello')
        time.sleep(2)
        self.assertEqual(res_delete.status, 'SUCCESS', "DELETE OPERATION FAILED")

    def test4(self):
        res_read_again = read('localhost:15002', 'hello')
        time.sleep(2)
        self.assertEqual(res_read_again.status, 'FILE ALREADY DELETED', "READ OPERATION FAILED")

    def test5(self):
        res_write = write('localhost:15001', 'hello', 'World Hello')
        time.sleep(2)
        self.assertEqual(res_write.status, 'DELETED FILE CANNOT BE UPDATED', "WRITE OPERATION FAILED")


def main():
    p = Process(target=run_registry)
    p.start()

    for i in range(3):
        p = Process(target=run_server, args=(names[i], ports[i]))
        p.start()

    time.sleep(1)
    unittest.main()


if __name__ == '__main__':
    main()
