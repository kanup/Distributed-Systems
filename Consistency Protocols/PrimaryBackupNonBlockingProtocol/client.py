import uuid

from utils import *
from time import sleep
import shutil
import asyncio
files = {}
import subprocess

async def read(filename, ipaddress):
    fileid=""
    if(filename not in files):
        print("UUID not found")
    else:
        fileid = files[filename]
    response = await rpc_client_read(ipaddress, fileid)
    print("Status:", response.status)
    print("Filename:", response.filename)
    print("Content:", response.content)
    print("Version:", response.version)


async def write(filename,content,ipaddress):    
    fileid = str(uuid.uuid4())
    if(filename in files):
        fileid = files[filename]
    else:
        files[filename] = fileid
    response = await rpc_client_write(ipaddress, filename, content, fileid)
    result = response
    print("Status:", result.status)
    print("UUID:", result.fileid)
    print("Version:", result.version)


async def delete(filename,ipaddress):
    fileid=""
    if(filename not in files):
        print("UUID not found")
    else:
        fileid = files[filename]
    response =await rpc_client_delete(ipaddress, fileid)
    print("Status:", response.status)


async def  get_available_servers():
    res = await rpc_registry_get_servers('localhost:8888')
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


async def main():
    while True:
        menu()
        print("----------------------------------")

        print("Enter Choice: ", end="")
        choice = input()

        if choice == '1':
            get_available_servers()
        elif choice == '2':
            ipaddress = input("Enter Server IP: ")
            filename = input("Enter filename: ")
            await read(filename=filename, ipaddress=ipaddress)
        elif choice == '3':
            ipaddress = input("Enter Server IP: ")
            filename = input("Enter filename: ")
            content = input("Enter file contents: ")
            await write(ipaddress=ipaddress, filename=filename, content=content)
        elif choice == '4':
            ipaddress = input("Enter Server IP: ")
            filename = input("Enter filename: ")
            await delete( filename=filename, ipaddress=ipaddress)
        elif choice == '5':
            break
        else:
            print("INVALID CHOICE")
        print("----------------------------------")


async def test():
    n=4
    try:
        for i in range(1,n+1):
            shutil.rmtree("s"+str(i))
    except Exception as e:
        pass
    sleep(1)
    subprocess.Popen(["python3", "registry_server.py"])
    sleep(2)
    processList=[]
    for i in range(1,n+1):
        processList.append(subprocess.Popen(["python3", "server.py", str(i)]))
        sleep(1)
    sleep(1)
    # delete(filename="a", ipaddress="localhost:5052")
    # sleep(1)
    # sleep(1)
    # await get_available_servers()
    # sleep(1)
    await write(ipaddress="localhost:5051", filename="a", content="hello")
    sleep(10)
    for i in range(1,n+1):
        await read(filename="a", ipaddress="localhost:505"+str(i))
    await write(ipaddress="localhost:5051", filename="b", content="hello2")
    sleep(10)
    for i in range(1,n+1):
        await read(filename="a", ipaddress="localhost:505"+str(i))
    await delete(filename="a", ipaddress="localhost:5052")
    sleep(1)
    for i in range(1,n+1):
        await read(filename="a", ipaddress="localhost:505"+str(i))
    
    for process in processList:
        process.wait()
    

if __name__ == '__main__':
    try:
        # main()
        # asyncio.run(main())
        
            # os.rmdir("s"+str(i))
        asyncio.run(test())
    except KeyboardInterrupt:
        print("Client Exiting")
