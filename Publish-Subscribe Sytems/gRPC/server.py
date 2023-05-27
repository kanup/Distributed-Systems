import pubsub_pb2
import pubsub_pb2_grpc
import grpc
import time 
from concurrent import futures
import uuid
import datetime

class ServerServices(pubsub_pb2_grpc.ServerServicesServicer):
    def __init__(self):
        self.subscribers = []
        self.articles = []


    def JoinServer(self, request, context):
        print("JOIN SERVER REQUEST FROM: " + request.id)
        if request.id in self.subscribers:
            print("Already joined")
            return pubsub_pb2.JoinServerResponse(message="FAILURE")
        self.subscribers.append(request.id)
        # print("Request Accepted")
        return pubsub_pb2.JoinServerResponse(message="SUCCESS")


    def PublishArticle(self, request, context):
        if( request.id not in self.subscribers):
            return pubsub_pb2.PublishArticleResponse(message="FAILURE")
        print("PUBLISH ARTICLE REQUEST FROM: " + request.id)
        articletype = request.article.WhichOneof('article_type')
        request.article.timestamp.FromDatetime(datetime.datetime.now())
        # obj = publishedarticles(articletype, request.article.title, request.article.author, request.article.content, )  
        self.articles.append(request.article)
        # print(self.articles[0].type)
        return pubsub_pb2.PublishArticleResponse(message="SUCCESS")
        

    def GetArticles(self, request, context):
        if request.id not in self.subscribers:
            print("Sorry, Not a subscriber")
            return 
        print("GET ARTICLES REQUEST FROM: " + request.id)
        listOFArticles = []
        for article in self.articles:
            articletype = article.WhichOneof('article_type')
            if checktype(article, request) and checkauthor(article, request) and checktimestamp(article, request):
                listOFArticles.append(article)
        print(listOFArticles)
        listOFArticles.sort(key=lambda x: x.timestamp.seconds, reverse=True)
        return pubsub_pb2.GetArticlesResponse(articles=listOFArticles)

    def LeaveServer(self, request, context):
        print("LEAVE SERVER REQUEST FROM: " + request.id)
        self.subscribers.remove(request.id)
        return pubsub_pb2.LeaveServerResponse(message="SUCCESS")
    
   

def serve():
    port = '4002'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pubsub_pb2_grpc.add_ServerServicesServicer_to_server(ServerServices(), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    print("Server started, listening on " + port)

    with grpc.insecure_channel('localhost:50051') as channel:
        stub = pubsub_pb2_grpc.RegistryServerServicesStub(channel)
        serverName = input("Enter server name: ")
        response = stub.RegisterServer(pubsub_pb2.RegistrServerRequest(name=serverName, port=port))
        channel.close()
        time.sleep(88888)
    server.wait_for_termination()

def checktype(article, request):
    if request.article_type == "":
        return True
    if article.HasField('article_type'):
        article_type = article.WhichOneof('article_type')
        if article_type == request.article_type:
            return True
        else:
            return False
    else:
        return False

def checkauthor(article, request):
    if request.author == "":
        return True
    if article.HasField('author'):
        if article.author == request.author:
            return True
        else:
            return False
    else:
        return False

def checktimestamp(article, request):
    
    t1=datetime.datetime.fromtimestamp(article.timestamp.seconds)
    t2=datetime.datetime.fromtimestamp(request.timestamp.seconds)
    if(t1 >= t2 or request.timestamp.seconds==0 or request.timestamp.nanos == 0):
        return True
    else:
        return False


if __name__ == '__main__':
    serve()

