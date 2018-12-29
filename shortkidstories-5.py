## 英文故事爬虫，保存成本地json文件
## shortkidstories-5.py
## 源站：http://www.shortkidstories.com/story/
## 作者：David
## 菜鸡写代码，每一个字符都是心血！！！

import requests
from bs4 import BeautifulSoup
import bs4
import re
import os

import json

## 下载html
def getHTMLText(url):
    print("targetUrl: " + url)
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = "utf-8"
        return r.text
    except:
        return ""

## 文本数据清洗
def textClean(text):
    garbageText = ' class="(.{1,10})?"'
    garbageText1 = '<div>'
    garbageText2 = '</div>'
    cleanedText = re.sub(garbageText, "", text).replace(garbageText1, "").replace(garbageText2, "")
    return cleanedText

## 文本简单加上段落标签
def textProcess(text):
    if len(text) > 0:
        if text[0] != "<":
            ProcessedText = "<p>" + text + "</p>"
        else:
            ProcessedText = text
    else:
        ProcessedText = text
    return ProcessedText

## 下载文章中的图片
def getImg(url):
    if str(url)[0] not in "http+":
        url = "http://www.shortkidstories.com" + url
    root = "D://Python//shortkidstories//img//"
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

## 下载文章中的audio
def getAudio(url):
    if str(url)[0] not in "http+":
        url = "http://www.shortkidstories.com" + url
    root = "D://Python//shortkidstories//audio//"
    path = root + url.split("/")[-1]
    try:
        if not os.path.exists(root):
            os.mkdir(root)
        if not os.path.exists(path):
            r = requests.get(url)
            with open(path, "wb") as f:
                f.write(r.content)
                f.close()
                print("audio下载成功")
        else:
            print("audio已经存在")
        return ""
    except:
        print("audio下载失败")
        return ""

## 获取爬取列表
def getTaskList(start, end):
    urlList = []
    with open("linkList.txt", "r", encoding = "UTF-8") as f:
        lines = f.readlines()
        for i in range(start, end):## 分批控制
            url = lines[i].split("---")[-1]
            urlList.append(url)
        f.close()
    return urlList

## 解析文章内容
def getArticle(html):
    
    data = {
        "title": "",
        "author": "",
        "level": "",
        "category": "",
        "tag": "",
        "length": "",
        "body": ""
    }
    
    soup = BeautifulSoup(html, "html.parser")

    ## audio
##    if soup.find_all("audio"):
##        if soup.find_all("audio")[0].a["href"]:
##            audioUrl = soup.find_all("audio")[0].a["href"]
##            getAudio(audioUrl)
##            print("<audio src='https://xcx.mdavid.cn/img/" + audioUrl.split("/")[-1] + "' controls='controls'>Your browser does not support the audio element.</audio>")
##            data["body"] += "<img src='https://xcx.mdavid.cn/img/" + imgUrl.split("/")[-1] + "'></img>"
        
    ## allStories
    for child in soup.find_all("div", "allStories")[0].children:
        if child.name == "h1" and child.attrs == {'class': ['archiveTitle']}:
            if child.string[0] == " ":## 忽略题目开头的空格
                print("title: " + child.string[1:])
                data["title"] = child.string[1:]
            else:
                print("title: " + child.string)
                data["title"] = child.string
        if child.name == "h2":
            if child.find_all("img"):
                if 'data-lazy-src' in child.find_all("img")[0].attrs.keys():
                        imgUrl = child.find_all("img")[0].attrs['data-lazy-src']
                else:
                    imgUrl = child.find_all("img")[0].attrs['src']
                print("<img src='https://xcx.mdavid.cn/img/" + imgUrl.split("/")[-1] + "'></img>")
                data["body"] += "<img src='https://xcx.mdavid.cn/img/" + imgUrl.split("/")[-1] + "'></img>"
                getImg(imgUrl)
                if child.string != None:
                    print(child.string)
                    data["body"] += textProcess(child.string)
            else:
                print(child)
                data["body"] += str(child)
        if child.name == "h3":
##            print("author: ", child.a.string)## 文章题目下的作者
##            data["author"] = child.a.string
            if child.string:
                print(child)
                data["body"] += textProcess(str(child))
        if child.name == "p":
##            if child.string != None:
##                print(child)
##                data["body"] += textProcess(str(child))
##            else:## p标签中包含的图片
            if child.find_all("img"):
                if 'data-lazy-src' in child.find_all("img")[0].attrs.keys():
                    imgUrl = child.find_all("img")[0].attrs['data-lazy-src']
                else:
                    imgUrl = child.find_all("img")[0].attrs['src']
                print("<img src='https://xcx.mdavid.cn/img/" + imgUrl.split("/")[-1] + "'></img>")
                data["body"] += "<img src='https://xcx.mdavid.cn/img/" + imgUrl.split("/")[-1] + "'></img>"
                getImg(imgUrl)

            if child.attrs == {'style': 'text-align: center;'}:
                if child.string != None:
                    print(child)
                    data["body"] += textProcess(str(child))
            else:
                pString = ""
                for item in child:
                    if item.string != None:
                        if item.string[0] != "[":## 忽略类似[Pg 78]的字符
                            pString += item.string
                print(textProcess(pString))
                data["body"] += textProcess(pString)
            
        if child.name == "div":
            print(child.attrs)
            if child.attrs == {'class': ['image-with-text'], 'id': 'nurseryRhyme'}:## 文章的另一个主要形式，应该单独找出来解析
                print("ignore")
            elif child.attrs == {'class': ['image-with-text']}:## {'class': ['image-with-text']}文章的另一个主要形式，应该单独找出来解析
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
                data["body"] += textClean(str(child))
            else:## allStories中的其他div，一般由插入图片时自动生成的div，其attrs不是固定的，特殊的未知的就只能忽略了
                if child.find_all("img"):## 包含图片
                    print(child.attrs)
                    if 'data-lazy-src' in child.find_all("img")[0].attrs.keys():
                        imgUrl = child.find_all("img")[0].attrs['data-lazy-src']
                    else:
                        imgUrl = child.find_all("img")[0].attrs['src']
                    print("<img src='https://xcx.mdavid.cn/img/" + imgUrl.split("/")[-1] + "'></img>")
                    data["body"] += "<img src='https://xcx.mdavid.cn/img/" + imgUrl.split("/")[-1] + "'></img>"
                    getImg(imgUrl)                                           
        else:## allStories中的其他标签
            print()
        


    ## image-with-text
    if soup.find_all("div", "image-with-text"):
##        if soup.find_all("p", "drop-caps"):
##            print(soup.find_all("p", "drop-caps")[0].text)
##            data["body"] += textProcess(soup.find_all("p", "drop-caps")[0].text)

##        for item in soup.find_all("span"):## span
##            if item.parent.name == "p":
##                if item.attrs != {'class': ['required']} and item.attrs != {'id': 'email-notes'}:
##                    print(item)
##                    data["body"] += "<div style='text-align:center'>" + textProcess(str(item)) + "</div>"

        documentText = []
        i = 0
        for item in soup.find_all("p"):## p
            if item.parent.name == "[document]" and item:
                if item.find_all("span"):
                    documentText.append("<div style='text-align:center'>" + str(item) + "</div>")
                else:
                    documentText.append(textProcess(str(item)))
                
        for child in soup.find_all("div", "image-with-text"):
            for item in child:
                if item.name == "img":
                    imgUrl = child.img.attrs['data-lazy-src']
                    print("<img src='https://xcx.mdavid.cn/img/" + imgUrl.split("/")[-1] + "'></img>")
                    data["body"] += "<img src='https://xcx.mdavid.cn/img/" + imgUrl.split("/")[-1] + "'></img>"
                    getImg(imgUrl)
                    
                    if i < len(documentText):
                        print(documentText[i])
                        data['body'] += documentText[i]
                        i += 1                  
                    
                if item.name == "span" and item.string:
                    print("<p style='text-align:center'>" + item.string + "</p>")
                    data["body"] += "<p style='text-align:center'>" + item.string + "</p>"

                if item.name == "p":
                    if item.find_all("img"):
                        imgUrl = item.find_all("img")[0].attrs['data-lazy-src']
                        print("<img src='https://xcx.mdavid.cn/img/" + imgUrl.split("/")[-1] + "'></img>")
                        data["body"] += "<img src='https://xcx.mdavid.cn/img/" + imgUrl.split("/")[-1] + "'></img>"
                        getImg(imgUrl)
                    else:
                        print(item)
                        data["body"] += textClean(str(item))


##            if child.text:
##                print(child.text)
##                print(child.attrs)
##            print(child)
##            data["body"] += textProcess(child.text)

##            for item in soup.find_all("p"):## p
##                if item.parent.name == "[document]" and item:
##                    print(textProcess(str(item)))
##                    data["body"] += "<div style='text-align:center'>" + textProcess(str(item)) + "</div>"


    print("********* Article Info *********")
    
    ## end-story-section
    for li in soup.find_all("div", "end-story-section")[0].ul:
        if str(li)[4] == "B":
            print("Author: ")
            for item in li.find_all("a"):
                print(item.string)
                data["author"] += item.string## 底部作者
            print("-------")
            
        if str(li)[4] == "A":
            if str(li)[5] == "g":
                print("Age range: ")
                for item in li.find_all("a"):
                    print(item.string)
                    data["level"] += (item.string + ",")
                print("-------")
                
            else:
                print("Animals: ")
                for item in li.find_all("a"):
                    print(item.string)
                    data["tag"] += (item.string + ",")
                print("-------")
                
        if str(li)[4] == "C":
            print("Category: ")
            for item in li.find_all("a"):
                print(item.string)
                data["category"] += (item.string + ",")
            print("-------")
            
        if str(li)[4] == "R":
            print("Reading time: ")
            for item in li.find_all("a"):
                print(item.string)
                data["length"] += (item.string + ",")
            print("-------")
        
    return data

## 打印data看效果
def read(data):
    print("##########" + " data数据 " + "##########")
    print(data["title"])
    print(data["author"])
    print(data["level"])
    print(data["category"])    
    print(data["tag"])
    print(data["length"])
    print(data["body"])

    return ""

def makeJson(name, data):
    root = "D://Python//shortkidstories//Articles//"
    path = root + name + ".json"
    try:
        if not os.path.exists(root):
            os.mkdir(root)
        if not os.path.exists(path):
            with open(path, "w", encoding = "UTF-8") as f:## w模式与a+模式不一样
                json.dump(data, f)
        else:
            print(name + "文件已经存在")
        return path
    except:
        print(name + "文件创建失败")
        return ""

##def main():
####  2018年7月（0，160）；9月（160，200）;（200，250）;
##    start = 200## 从linkList.txt第(start+1)行开始，下次以end值作为start值
##    end = 250## 到第end行结束
##    urlList = getTaskList(start, end)
##    count = 0
##    for item in urlList:
##        print("----------", count, "----------")
##        html = getHTMLText(item)
##        data = getArticle(html)
##        name = item.split("/")[-2]## 文件名name
####        read(data)
##        makeJson(name, data)
##        count = count + 1
##        print("***************************")
##    print(count, "篇文章爬取成功")
##
##main()

def test():

    url = "http://www.shortkidstories.com/story/fairy-ring/"

    html = getHTMLText(url)
    data = getArticle(html)
    name = url.split("/")[-2]## 文件名name
##    read(data)
    makeJson(name, data)

test()
