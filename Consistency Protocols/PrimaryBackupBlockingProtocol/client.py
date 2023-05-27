import uuid

from utils import *

files = {}


def read():
    ipaddress = input("Enter Server IP: ")
    filename = input("Enter filename: ")
    fileid = files[filename]
    response = rpc_client_read(ipaddress, fileid)
    print("Status:", response.status)
    print("Filename:", response.filename)
    print("Content:", response.content)
    print("Version:", response.version)


def write():
    ipaddress = input("Enter Server IP: ")
    filename = input("Enter filename: ")
    fileid = str(uuid.uuid4())
    files[filename] = fileid
    content = input("Enter file contents: ")

    response = rpc_client_write(ipaddress, filename, content, fileid)
    print("Status:", response.status)
    print("UUID:", response.fileid)
    print("Version:", response.version)


def delete():
    ipaddress = input("Enter Server IP: ")
    filename = input("Enter filename: ")
    fileid = files[filename]
    response = rpc_client_delete(ipaddress, fileid)
    print("Status:", response.status)


def get_available_servers():
    res = rpc_registry_get_servers('localhost:8888')
    res = list(res.listOfServers)
    for item in res:
        print(item)


def menu():
    print("Menu")
    print("\t1) Get Available Servers")
    print("\t2) READ Operation")
    print("\t3) WRITE Operation")
    print("\t4) DELETE Operation")
    print("\t5) Exit")


def main():
    while True:
        menu()
        print("----------------------------------")

        print("Enter Choice: ", end="")
        choice = input()

        if choice == '1':
            get_available_servers()
        elif choice == '2':
            read()
        elif choice == '3':
            write()
        elif choice == '4':
            delete()
        elif choice == '5':
            break
        else:
            print("INVALID CHOICE")
        print("----------------------------------")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Client Exiting")
