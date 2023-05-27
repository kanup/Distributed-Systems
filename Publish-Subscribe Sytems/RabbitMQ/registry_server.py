import marshal
import os
import sys
import time

from utility import start_server, publish_message

MAX_SERVERS = 10
servers = dict()
ID = 'registry-server'


def deregister_server(client_id, request):
    print(f"DE-REGISTER REQUEST FROM {client_id}")
    if request in servers:
        servers.pop(request)
    return ["SUCCESS"]


def registerServer(client_id, request):
    print(f"REGISTER REQUEST FROM {client_id}")

    if not len(servers) < MAX_SERVERS:
        return ["FAILED", "MAX SERVER LIMIT REACHED"]

    name, address = request.split(",")
    servers[name] = address

    return ["SUCCESS"]


def getServerList(client_id):
    time.sleep(10)
    print(f"GET SERVERS REQUEST FROM {client_id}")

    if len(servers) == 0:
        return ["FAIL", "NO SERVERS ONLINE"]

    res = ["SUCCESS"]
    for server in servers:
        res.append(server + "," + servers[server])

    return res


def on_request(channel, method, props, body):
    client_id = props.correlation_id

    received = marshal.loads(body)
    request = received[0]

    if request == 'get-server-list':
        response = getServerList(client_id)
    elif request == 'register':
        response = registerServer(client_id, received[1])
    elif request == 'un-register':
        response = deregister_server(client_id, received[1])
    else:
        response = ["FAILED", "INVALID REQUEST"]

    publish_message(channel, props.reply_to, ID, response)


def main():
    start_server(ID, on_request)


if __name__ == '__main__':
    try:
        print("Registry server started...")
        main()
    except KeyboardInterrupt:
        print("Registry server shutting down...")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
