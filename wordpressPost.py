## 实现自动发布wordpress文章
## wordpressPost.py
## 作者：David
## 菜鸡写代码，每一个字符都是心血！！！

from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost
from wordpress_xmlrpc.methods.users import GetUserInfo
import os
import json
from bs4 import BeautifulSoup

def wordpressPost(data):
    if not verifyPost(data["title"]):
        if len(data["body"]) > 100:## 内容长度验证      
            wp = Client('https://xcx.mdavid.cn/xmlrpc.php', '', '')
            post = WordPressPost()
            post.title = data["title"]
            post.content = data["body"]
            post.post_status = 'publish'
            post.terms_names = {
                'post_tag': data["tag"],
                'category': data["category"]
                }
            
            wp.call(NewPost(post))

            print(data["title"], "发布成功")
            with open("xcx_successPostLog.txt", "a+", encoding = "UTF-8") as f:
                f.write(data["title"] + "\n")
                f.close()
        else:
            print(data["title"], "内容太短，可能有问题，已保存到日志")
            with open("xcx_failPostLog.txt", "a+", encoding = "UTF-8") as f:
                f.write(data["title"] + "\n")
                f.close()
    return ""

## 验证是否重复发布
def verifyPost(title):
    title += "\n"
    flag = False
    try:
        with open("xcx_successPostLog.txt", "r", encoding = "UTF-8") as f:
            lines = f.readlines()
            f.close()
        if title in lines:
            flag = True
            print("已经发送过了")
        return flag
    except:## 文件未找到，第一次发送前没有successPostLog.txt
        return flag 

def getData(name):
    root = "D://Python//shortkidstories//Articles//"
    path = root + name + ".json"
    try:
        if os.path.exists(path):
            with open(path, 'r', encoding = "UTF-8") as f:
                data = json.load(f)
            return data
        else:
            print(name + "文件未找到")
            return ""                
    except:
        print(name + "文件读取异常")
        return ""

def getTaskList(start, end):
    postList = []
    with open("linkList.txt", "r", encoding = "UTF-8") as f:
        lines = f.readlines()
        for i in range(start, end):## 分批控制
            name = lines[i].split("/")[-2]
            postList.append(name)
        f.close()
    return postList

def parserData(data):
    
    postData = {
        "title": "",
        "body": "",
        "tag": [],
        "category": []
        }

    postData["title"] = data["title"]

##    soup = BeautifulSoup(data["body"], "html.parser")
##    postData["body"] = soup.prettify()
    postData["body"] = data["body"]
    
    for item in data["tag"].split(","):
        if item:
            postData["tag"].append(item)
    for item in data["category"].split(","):
        if item:
             postData["category"].append(item)
    ## level与length决定一个分类

    return postData

def readData(data):
    print(data)
    return ""

def main():
    start = 147
    end = 150## POST记录：第1次（0， 30）；第2次（30， 100）；第3次（100， 120）；第4次（120， 122）；第5次（122， 124）；
##  第6次（124， 126）；第7次（126， 128）；第8次（128， 129）；第9次（129， 131）；
##  第10次（131， 133）；第11次（133， 137）；第12次（137， 138）；第13次（138， 140）；第14次（140， 142）；
##  第15次（142， 145）；第16次（145， 147）；第17次（147， 150）；  
    postList = getTaskList(start, end)
    count = 0
    for item in postList:## item是文件名name
        print("----------", count, "----------")
        data = getData(item)
        postData = parserData(data)
##        readData(postData)
        wordpressPost(postData)
        count = count + 1
    print(count, "篇文章发布成功")
    return ""

main()
