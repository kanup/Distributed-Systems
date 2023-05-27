import os
import sys
import uuid
from utility import *

ID = str(uuid.uuid4())
serverList = dict()
joinedServers = []


# ------------------------------------------------------------

def silent_accept(channel, method, props, body):
    response = marshal.loads(body)
    servers = response[1:]

    serverList.clear()
    for index, server in enumerate(servers):
        name, address = server.split(",")
        serverList[name] = address


def available_server_response(channel, method, props, body):
    response = marshal.loads(body)
    if not receive_template(response):
        return

    servers = response[1:]

    if len(servers) == 0:
        print("NO SERVERS ONLINE")

    serverList.clear()
    for index, server in enumerate(servers):
        name, address = server.split(",")
        serverList[name] = address

        print(f"\t{index + 1}) {name} - {address}")


def join_server_response(channel, method, props, body):
    response = marshal.loads(body)
    if not receive_template(response):
        return

    for server in serverList:
        if serverList[server] == props.correlation_id and server not in joinedServers:
            joinedServers.append(server)
            break


def leave_server_response(channel, method, props, body):
    response = marshal.loads(body)
    if not receive_template(response):
        return

    for server in serverList:
        if serverList[server] == props.correlation_id and server in joinedServers:
            joinedServers.remove(server)
            break


def get_articles_response(channel, method, props, body):
    response = marshal.loads(body)
    if not receive_template(response):
        return

    articles = response[1:]

    if len(articles) == 0:
        print("NO ARTICLES RETURNED")
        return

    for index, article in enumerate(articles):
        article_type, author, time, content = article.split(",")
        print(f"{index + 1})\t{article_type}")
        print(f"  \t{author}")
        print(f"  \t{time}")
        print(f"  \t{content}")


def publish_article_response(channel, method, props, body):
    response = marshal.loads(body)
    if not receive_template(response):
        return

    print("Article Published")


# ------------------------------------------------------------


def get_available_servers():
    args = ['get-server-list']
    request_reply('registry-server', available_server_response, ID, marshal.dumps(args))


def join_server():
    args = ['get-server-list']
    request_reply('registry-server', silent_accept, ID, marshal.dumps(args))

    print("Select a available server:")
    selected = display_choices(serverList)

    if selected is None:
        print("No server available to join")
        return

    address = serverList[selected]

    args = ['join-server']
    request_reply(address, join_server_response, ID, marshal.dumps(args))


def leave_server():
    print("Select a server to leave:")
    selected = display_choices(joinedServers)

    if selected is None:
        print("No server joined")
        return

    address = serverList[selected]

    args = ['leave-server']
    request_reply(address, leave_server_response, ID, marshal.dumps(args))


def publish_article():
    print("Select a joined server:")
    selected = display_choices(joinedServers)

    if selected is None:
        print("No server joined")
        return

    address = serverList[selected]

    print("Enter article:")
    article_type = input("Type: ")
    author = input("Author: ")
    time = input("Time (leave it blank): ")
    content = input("Content: ")

    if not check_publish_format(article_type, author, time, content):
        print("INVALID FORMAT")
        return

    args = ['publish-article', f'{article_type},{author},{content}']
    request_reply(address, publish_article_response, ID, marshal.dumps(args))


def get_articles():
    print("Select a joined server:")
    selected = display_choices(joinedServers)

    if selected is None:
        print("No server joined")
        return

    if selected not in serverList:
        print("Server not online")
        return

    address = serverList[selected]

    print("Enter article in request format:")
    article_type = input("Type: ")
    author = input("Author: ")
    time = input("Time: ")

    if time == '' or article_type == author == time == '':
        print("INVALID FORMAT")
        return


    args = ['get-articles', f'{article_type},{author},{time}']
    request_reply(address, get_articles_response, ID, marshal.dumps(args))


# ------------------------------------------------------------


def menu():
    print("Menu")
    print("\t1) Get Available Servers")
    print("\t2) Join Server")
    print("\t3) Leave Server")
    print("\t4) Get Articles")
    print("\t5) Publish Article")
    print("\t0) Exit")


def main():
    while True:
        menu()
        print("----------------------------------")

        print("Enter Choice: ", end="")
        choice = input()

        if choice == '1':
            get_available_servers()
        elif choice == '2':
            join_server()
        elif choice == '3':
            leave_server()
        elif choice == '4':
            get_articles()
        elif choice == '5':
            publish_article()
        elif choice == '0':
            break
        else:
            print("INVALID CHOICE")
        print("----------------------------------")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nClient shutting down...")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
