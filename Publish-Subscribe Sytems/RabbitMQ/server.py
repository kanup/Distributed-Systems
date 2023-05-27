import os
import uuid
import marshal
import sys
from datetime import date, timedelta
from utility import request_reply, start_server, publish_message, receive_template


class Article:
    count = 0

    def __init__(self, article_type, author, content):
        self.article_type = article_type
        self.author = author
        self.time = date.today() + timedelta(days=Article.count)
        self.content = content
        Article.count += 1

    def __str__(self) -> str:
        return self.article_type + "," + self.author + "," + str(self.time) + "," + self.content


ID = str(uuid.uuid4())

MAX_CLIENTS = 10
clientList = []
articles = [
    Article("SPORTS", "Jack Dorsey", "Messi has won the FIFA World Cup"),
    Article("POLITICS", "Kejriwal", "Toh kar na!"),
    Article("FASHION", "Raveena Tandon", "I don't do fashion"),
]


def registry_response(channel, method, props, body):
    response = marshal.loads(body)
    if not receive_template(response):
        sys.exit(0)


def deregister(server):
    args = ['un-register', server]
    request_reply('registry-server', registry_response, ID, marshal.dumps(args))


def register(server):
    args = ['register', f'{server},{ID}']
    request_reply('registry-server', registry_response, ID, marshal.dumps(args))


def add_client(client_id):
    print(f"JOIN REQUEST FROM {client_id}")

    if not len(clientList) < MAX_CLIENTS:
        return ["FAILED", "MAX CLIENT LIMIT REACHED"]

    if client_id not in clientList:
        clientList.append(client_id)

    return ["SUCCESS"]


def remove_client(client_id):
    print(f"LEAVE REQUEST FROM {client_id}")

    if client_id in clientList:
        clientList.remove(client_id)
    return ["SUCCESS"]


def publish_article(client_id, request):
    print(f"ARTICLE PUBLISH FROM {client_id}")

    if client_id not in clientList:
        return ["FAIL", "CLIENT HAS NOT JOINED SERVER"]

    article_type, author, content = request.split(",")
    articles.append(Article(article_type, author, content))

    return ["SUCCESS"]


def send_articles(client_id, request):
    print(f"ARTICLE REQUEST FROM {client_id}")
    print("\tFOR", request)
    print(f"")

    article_type, author, time_tmp = request.split(",")
    year, month, day = time_tmp.split("/")
    time = date(int(year), int(month), int(day))

    res = ["SUCCESS"]
    for article in articles:
        if article.time >= time and \
                (article_type == '' or article.article_type == article_type) and \
                (author == '' or article.author == author):
            res.append(str(article))

    return res


def on_request(channel, method, props, body):
    client_id = props.correlation_id

    received = marshal.loads(body)
    request = received[0]

    if request == 'join-server':
        response = add_client(client_id)
    elif request == 'leave-server':
        response = remove_client(client_id)
    elif request == 'publish-article':
        response = publish_article(client_id, received[1])
    elif request == 'get-articles':
        response = send_articles(client_id, received[1])
    else:
        response = ["FAILED", "INVALID REQUEST"]

    publish_message(channel, props.reply_to, ID, response)


def main():
    start_server(ID, on_request)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        name = ID
    else:
        name = sys.argv[1]
    register(name)
    print(f"Server {name} started...")

    try:
        main()
    except KeyboardInterrupt:
        print(f"Server {name} shutting down...")
        deregister(name)
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)