## 英文故事爬虫
## shortkidstories-4.py
## 源站：http://www.shortkidstories.com/story/
## 作者：David
## 菜鸡写代码，每一个字符都是心血！！！

import requests
from bs4 import BeautifulSoup
import bs4
import re
import os

from xml.etree.ElementTree import parse
from xml.etree.ElementTree import Element, SubElement, ElementTree

import json

## 下载html
def getHTMLText(url):
    print("link:  " + url)
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = "utf-8"
        return r.text
    except:
        return ""

## 保存每一篇文章
def saveArticle(name):
    root = "D://Python//shortkidstories//Articles//"
    path = root + name + ".json"
    try:
        if not os.path.exists(root):
            os.mkdir(root)
        if not os.path.exists(path):
            print("应该创建")
        else:
            print(name + "文件已经存在")
        return path
    except:
        print(name + "文件创建失败")
        return ""

## 生成xml
def makeXml(path):
    
    root = Element('root')## 根节点
    
    filePath = SubElement(root, 'filePath')
    filePath.text = ' '

    title = SubElement(root, 'title')
    title.text = ' '

    author = SubElement(root, 'author')
    author.text = ' '

    level = SubElement(root, 'level')
    level.text = ' '

    category = SubElement(root, 'category')
    category.text = ' '

    tag = SubElement(root, 'tag')
    tag.text = ' '
    
    length = SubElement(root, 'length')
    length.text = ' '
    

    body = SubElement(root, 'body')
    body.text = ' '
    
    tree = ElementTree(root)
    
    tree.write(path, encoding='utf-8')

    print("生成xml成功")

    return ""

## 更新xml
def updateXml(data):
    print("updateXml")
    
    updataTree = parse(data["filePath"])
    root = updataTree.getroot()

    filePath = root.find('filePath')
    filePath.text = data["filePath"]

    title = root.find('title')
    title.text = data["title"]

    author = root.find('author')
    author.text = data["author"]

    level = root.find('level')
    level.text = data["level"]

    category = root.find('category')
    category.text = data["category"]

    tag = root.find('tag')
    tag.text = data["tag"]

    length = root.find('length')
    length.text = data["length"]

    body = root.find('body')
    body.text = data["body"]

    updataTree.write(str(data["filePath"]))
    
    return ""
## 文本数据清洗
def textClean(text):
    garbageText = ' class="(.{1,10})?"'
    garbageText1 = '<div>'
    garbageText2 = '</div>'
    cleanedText = re.sub(garbageText, "", text).replace(garbageText1, "").replace(garbageText2, "")
    return cleanedText

## 下载文章中的图片
def getImg(url):
    if str(url)[0] not in "http+":
        url = "http://www.shortkidstories.com" + url
    root = "D://Python//shortkidstories//Images//"
    path = root + url.split("/")[-1]
    try:
        if not os.path.exists(root):
            os.mkdir(root)
        if not os.path.exists(path):
            r = requests.get(url)
            with open(path, "wb") as f:
                f.write(r.content)
                f.close()
                print("图片下载成功")
        else:
            print("图片已经存在")
        return ""
    except:
        print("图片下载失败")
        return ""

## 获取爬取列表
def getTaskList(start, end):
    urlList = []
    with open("linkList.txt", "r") as f:
        lines = f.readlines()
        for i in range(start, end):## 分批控制
            url = lines[i].split("---")[-1]
            urlList.append(url)
        f.close()
    return urlList

## 解析文章内容
def getArticle(html, path):
    data = {
        "filePath": "",
        "title": "",
        "author": "",
        "level": "",
        "category": "",
        "tag": "",
        "length": "",
        "body": ""
    }

    data["filePath"] = path
    
    soup = BeautifulSoup(html, "html.parser")
    
    ## allStories
    for child in soup.find_all("div", "allStories")[0].children:
        if child.name == "h1":
            print("title:", child.string)
            if child.string[0] == " ":## 忽略题目开头的空格
                data["title"] = child.string[1: -1]
            else:
                data["title"] = child.string
        if child.name == "h3":
            print("author: ", child.a.string)
            data["author"] = child.a.string
        if child.name == "p":
            if child.string != None:
                print(child)
                data["body"].append(child)
            else:## p标签中包含的图片
                if child.find_all("img"):
                    imgUrl = child.find_all("img")[0].attrs['data-lazy-src']
                    print("<img src='https://xcx.mdavid.cn/Imaegs/" + imgUrl.split("/")[-1] + "'></img>")
                    data["body"].append("<img src='https://xcx.mdavid.cn/Imaegs/" + imgUrl.split("/")[-1] + "'></img>")
                    getImg(imgUrl)
        if child.name == "div":
            print(child.attrs)
            if child.attrs == {'class': ['image-with-text'], 'id': 'nurseryRhyme'}:## 文章的另一个主要形式，应该单独找出来解析
                print("ignore")
            elif child.attrs == {'class': ['image-with-text']}:## 文章的另一个主要形式，应该单独找出来解析
                print("ignore")    
            elif child.attrs == {'class': ['fontSize']}:## 忽略已知的无关div
                print("ignore")
            elif child.attrs == {'style': 'display: none'}:## 忽略已知的无关div
                print("ignore")
            elif child.attrs == {'class': ['ratingblock', '']}:## 忽略已知的无关div
                print("ignore")
            elif child.attrs == {'id': 'ssba-classic-2', 'class': ['ssba', 'ssbp-wrap', 'left', 'ssbp--theme-1']}:## 忽略已知的无关div
                print("ignore")
            elif child.attrs == {'class': ['lookForComments']}:## 忽略已知的无关div
                print("ignore")
            elif child.attrs == {'class': ['end-story-section']}:## 文章的属性，单独找出来解析
                print("ignore")
            elif child.attrs == {'class': ['poem']}:## 包含blockquote标签的div
                soup1 = BeautifulSoup(textClean(str(child)), "html.parser")
                print(soup1.prettify())
                data["body"].append(textClean(str(child)))    
            else:## allStories中的其他div，一般由插入图片时自动生成的div，其attrs不是固定的
                if child.find_all("img"):## 包含图片
                    print(child.attrs)
                    if child.find_all("img")[0].attrs['data-lazy-src']:
                        imgUrl = child.find_all("img")[0].attrs['data-lazy-src']
                        print("<img src='https://xcx.mdavid.cn/Imaegs/" + imgUrl.split("/")[-1] + "'></img>")
                        data["body"].append("<img src='https://xcx.mdavid.cn/Imaegs/" + imgUrl.split("/")[-1] + "'></img>")
                        getImg(imgUrl)                                            
        else:## allStories中的其他标签
            print()

    ## image-with-text
    if soup.find_all("div", "image-with-text"):
        if soup.find_all("p", "drop-caps"):
            print(soup.find_all("p", "drop-caps")[0].text)
            data["body"].append(soup.find_all("p", "drop-caps")[0].text)
    
        for item in soup.find_all("span"):## span
            if item.parent.name == "p":
                if item.attrs != {'class': ['required']} and item.attrs != {'id': 'email-notes'}:
                    print(item)
                    data["body"].append(item)
    
        for child in soup.find_all("div", "image-with-text"):
            if child.find_all("img"):
                imgUrl = child.img.attrs['data-lazy-src']
                print("<img src='https://xcx.mdavid.cn/Imaegs/" + imgUrl.split("/")[-1] + "'></img>")
                data["body"].append("<img src='https://xcx.mdavid.cn/Imaegs/" + imgUrl.split("/")[-1] + "'></img>")
                getImg(imgUrl)
            print(child.text)
            data["body"].append(child.text)
        
    print("*********Article Info*********")

    ## end-story-section
    for li in soup.find_all("div", "end-story-section")[0].ul:
        if str(li)[4] == "B":
            print("Author: ")
            for item in li.find_all("a"):
                print(item.string)
                data["author"].append(item.string)
            print("-------")
            
        if str(li)[4] == "A":
            if str(li)[5] == "g":
                print("Age range: ")
                for item in li.find_all("a"):
                    print(item.string)
                    data["level"].append(item.string)
                print("-------")
                
            else:
                print("Animals: ")
                for item in li.find_all("a"):
                    print(item.string)
                    data["tag"].append(item.string)
                print("-------")
                
        if str(li)[4] == "C":
            print("Category: ")
            for item in li.find_all("a"):
                print(item.string)
                data["category"].append(item.string)
            print("-------")
            
        if str(li)[4] == "R":
            print("Reading time: ")
            for item in li.find_all("a"):
                print(item.string)
                data["length"].append(item.string)
            print("-------")
        
    return data

def read(data):
    print("############################################################")

    print(type(data))

    print(data["filePath"])
    print(type(data["filePath"]))
    
    print(data["title"])
    print(type(data["title"]))
    
    print(data["author"])
    print(type(data["author"]))
    
    print(data["level"])
    print(type(data["level"]))
    
    print(data["category"])
    print(type(data["category"]))
    
    print(data["tag"])
    print(type(data["tag"]))
    
    print(data["length"])
    print(type(data["length"]))
    
##    print(data["body"])
    for text in data["body"]:
        print(text)
    
    return ""

def makeJson(data):
    filePath = data["filePath"]
    with open(filePath, "w") as f:
        json.dump(data, f)
    return ""

def main():
    start = 0## 从linkList.txt第(start+1)行开始
    end = 1## 到第end行结束
    urlList = getTaskList(start, end)
    count = 0
    for item in urlList:
        print("----------", count, "----------")
        path = saveArticle(item.split("/")[-2])## item.split("/")[-2]是name
        html = getHTMLText(item)
        data = getArticle(html, path)
        read(data)
        makeJson(data)
##        updateXml(data)
        count = count + 1
        print("***************************")
    print(count, "篇文章爬取成功")

main()
