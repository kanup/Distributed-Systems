
import datetime
import time
from anyio import sleep
import zmq
import pubsub_pb2 as pb
import threading
import base64
from utils import *

def connectToServer(port):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://127.0.0.1"+":"+port)
    print("Connected to registry server at tcp://localhost:" +port)
    return socket

def startTheServer(port):
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://127.0.0.1"+":"+port)
    print(address.name+ " started at tcp://localhost:"+port)
    return socket




def registerServer():
    socket=connectToServer("1111")
    sendRequest(socket,"RegisterServer",address.SerializeToString())
    message=socket.recv()
    response,body=getResponseFromStr(message)
    message=body.decode('utf-8')
    print(message)

def addClientToServer(Client):
    try:
        if(len(server.members)<server.maxclient and Client not in server.members):
            server.members.append(Client)
            return "SUCCESS"
        else:
            return "FAIL"
    except:
        return "FAIL"
def removeClientFromServer(Client):
    try:
        server.members.remove(Client)
        return "SUCCESS"
    except:
        return "FAIL"

def publishArticle(article):
    try:
        which_field=article.WhichOneof("type")
        if(which_field is None or article.author is None or article.client not in server.members or len(article.content.strip())==0 ):
            return "FAIL"
        article.timestamp.FromDatetime(datetime.datetime.now())
        # print('article ')
        # print(article)
        server.publishedArticles.append(article)
        return "SUCCESS"
    except:
        return "FAILED"

def checkArticleType(article,searchParameter):
    # print(searchParameter.WhichOneof("type"))
    if(article.WhichOneof("type") == searchParameter.WhichOneof("type") or searchParameter.WhichOneof("type")==None):
        return True
    else:
        return False
def checkArticleTimestamp(article,timestamp):
    t1=datetime.datetime.fromtimestamp(article.timestamp.seconds)
    t2=datetime.datetime.fromtimestamp(timestamp.seconds)
    if(t1 >=t2 or timestamp is None):
        return True
    else:
        return False
def checkArticleAuthor(article,author):
    if(article.author == author or author==''):
        return True
    else:
        return False



def GetPublishedArticles(searchParameter):
    if(searchParameter.client not in server.members):
        return "FAIL"
    articleResponse=pb.ArticleResponse()
    temp=[]
    for article in server.publishedArticles:
        if(checkArticleAuthor(article,searchParameter.author) and checkArticleTimestamp(article,searchParameter.timestamp) and checkArticleType(article,searchParameter)):
            temp.append(article)
    articleResponse.articles.extend(temp)
    return articleResponse.SerializeToString()

def handleRequest(message):
    request,body=getRequestFromStr(message)
    if request.method=="JoinServer":
        client=pb.client()
        client.ParseFromString(body)
        print('Join REQUEST FROM ' +str(client.uuid))
        message=addClientToServer(client)
        message=bytes(message,'utf-8')
        sendResponse(socket,message)
    elif request.method=="LeaveServer":
        client=pb.client()
        client.ParseFromString(body)
        print('Leave REQUEST FROM '+str(client.uuid))
        message=removeClientFromServer(client)
        message=bytes(message,'utf-8')
        sendResponse(socket,message)
        # print('client removed')
    elif request.method=="PublishArticle":
        article=pb.Article()
        article.ParseFromString(body)
        print('ARTICLES PUBLISH REQUEST FROM '+str(article.client.uuid))
        message=publishArticle(article)
        message=bytes(message,'utf-8')
        sendResponse(socket,message)
        # print('article published')
    elif request.method=="GetPublishedArticles":
        searchParameter=pb.ArticleRequest()
        searchParameter.ParseFromString(body)
        print('ARTICLES REQUEST FROM '+str(searchParameter.client.uuid))
        print("FOR")
        print("Author: "+str(searchParameter.author))
        print("Type: "+str(searchParameter.WhichOneof("type")))
        dd_mm_yyyy_str = ""
        if(searchParameter.timestamp.seconds!=0):
            datetime_obj = datetime.datetime.fromtimestamp(searchParameter.timestamp.seconds + searchParameter.timestamp.nanos / 1e9)
            dd_mm_yyyy_str = datetime_obj.strftime("%d/%m/%Y")
        print("Timestamp: "+str(dd_mm_yyyy_str))
        message=GetPublishedArticles(searchParameter)
        sendResponse(socket,message)
        # print('articles sent')
    else:
        sendResponse(socket,bytes('wrong method','utf-8'))

def receiveRequest(socket):
    while True:
        print("waiting for request \n")
        message = socket.recv()
        handleRequest(message)
        print("request served")
    
server_number=1
port=str(1111+server_number)
address=pb.address()
address.name="server "+str(server_number)
address.port=port
server=pb.Server()
server.maxclient=5
socket=startTheServer(port)
threadList=[]
receiveRequestThread=threading.Thread(target=receiveRequest,args=(socket,))
receiveRequestThread.start()

while True:
    print('Press 1 to register server')
    print('Press 0 to exit')
    end=input()
    if(end=="1"):
        registerServer()
    if(end=="0"):
        for thread in threadList:
            thread.join()
        exit()

    
