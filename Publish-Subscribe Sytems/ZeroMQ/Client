
import time
import zmq
import pubsub_pb2 as pb
import uuid
import datetime
import base64
from utils import *
import traceback
from google.protobuf.timestamp_pb2 import Timestamp

unique_id = str(uuid.uuid1())

client = pb.client()
client.uuid=unique_id

def connectToServer(port):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://127.0.0.1"+":"+port)
    print("Connected to server at tcp://localhost:" +port)
    return socket



def createArticle(type,author,content,client):
    article=pb.Article()
    if(type=="SPORTS"):
        article.sports=True
    elif(type=="POLITICS"):
        article.politics=True
    elif(type=="FASHION"):
        article.fashion=True
    article.author=author
    article.content=content
    article.client.uuid=client.uuid
    return article


def requestServerList(port):
    socket=connectToServer(port)
    
    sendRequest(socket,"GetServers",bytes(unique_id,"utf-8"))
    message=socket.recv()
    response,body=getResponseFromStr(message)
    addressListResponse=pb.addressListResponse()
    addressListResponse.ParseFromString(body)
    return addressListResponse.addresses


def joinServer(port):
    socket=connectToServer(port)
    sendRequest(socket,"JoinServer",client.SerializeToString())
    message=socket.recv()
    response,body=getResponseFromStr(message)
    body=body.decode('utf-8')
    print(body)

def leaveServer(port):
    socket=connectToServer(port)
    sendRequest(socket,"LeaveServer",client.SerializeToString())
    message=socket.recv()
    response,body=getResponseFromStr(message)
    body=body.decode('utf-8')
    print(body)
def publishArticle(port,article):
    socket=connectToServer(port)
    sendRequest(socket,"PublishArticle",article.SerializeToString())
    message=socket.recv()
    response,body=getResponseFromStr(message)
    body=body.decode('utf-8')
    print(body)

def searchArticle(port,articleRequest):
    socket=connectToServer(port)
    sendRequest(socket,"GetPublishedArticles",articleRequest.SerializeToString())
    message=socket.recv()
    response,body=getResponseFromStr(message)
    if(body==b'fail'):
        body=body.decode('utf-8')
        print(body)
    else:
        articleResponse=pb.ArticleResponse()
        articleResponse.ParseFromString(body)
        for article in articleResponse.articles:
            print(article)

def createArticleRequest(type,author,timestamp):
    articleRequest=pb.ArticleRequest()
    if(type=="SPORTS"):
        articleRequest.sports=True
    elif(type=="POLITICS"):
        articleRequest.politics=True
    elif(type=="FASHION"):
        articleRequest.fashion=True
    articleRequest.author=author.strip()
    if(timestamp!=""):
        dt=datetime.datetime.strptime(timestamp, '%d-%m-%Y')
        # articleRequest.timestamp.FromDatetime(dt)
        articleRequest.timestamp.FromDatetime(dt)
    articleRequest.client.uuid=client.uuid
    return articleRequest

# print(requestServerList())
while True:
    try:
        print("Enter your choice")
        print("0. Get server list")
        print("1. Join server")
        print("2. Leave server")
        print("3. Publish article")
        print("4. Search article")
        print("5. Exit")
        choice=input()
        if(choice=="0"):
            print("Enter the port number of the server you want to get server list")
            print(requestServerList("1111"))
        elif(choice=="1"):
            print("Enter the port number of the server you want to join")
            port=input()
            joinServer(port)
        elif(choice=="2"):
            print("Enter the port number of the server you want to leave")
            port=input()
            leaveServer(port)
        elif(choice=="3"):
            print("Enter the port number of the server you want to publish article")
            port=input()
            print("Enter the type of the article")
            type=input()
            print("Enter the author of the article")
            author=input()
            print("Enter the content of the article")
            content=input()
            article=createArticle(type,author,content,client)
            publishArticle(port,article)
        elif(choice=="4"):
            print("Enter the port number of the server you want to search article")
            port=input()
            print("Enter the type of the article")
            type=input()
            print("Enter the author of the article")
            author=input()
            print("Enter the timestamp of the article in (dd-mm-yyyy)")
            timestamp=input()
            articleRequest=createArticleRequest(type,author,timestamp)
            searchArticle(port,articleRequest)
        elif(choice=="5"):
            exit()
        else:
            print("Invalid choice")
    except Exception as e:
        print("Error occurred")
        print(traceback.print_exc())

