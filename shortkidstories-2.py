## 英文故事爬虫
## shortkidstories-2.py
## 源站：http://www.shortkidstories.com/story/
## 作者：David
## 菜鸡写代码，每一个字符都是心血！！！

import requests
from bs4 import BeautifulSoup
import bs4
import re
import os

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
    
## 保存每一篇文章
def saveArticle(name):
    root = "D://Python//shortkidstories//Articles//"
    path = root + name + ".txt"
    try:
        if not os.path.exists(root):
            os.mkdir(root)
        if not os.path.exists(path):

            with open(path, "a+", encoding="utf-8") as f:
                f.write("fileName: " + name + "\n")
                f.write("link: "+ "http://www.shortkidstories.com/story/" + name + "/" + "\n")
                f.close()
                print(name + ".txt" + "创建成功")
        else:
            print(name + ".txt" + "已经存在")
        return path
    except:
        print(name + ".txt" + "创建失败")
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
    soup = BeautifulSoup(html, "html.parser")
    
    with open(path, 'a+', encoding="utf-8") as f:

        ## allStories
        for child in soup.find_all("div", "allStories")[0].children:
            if child.name == "h1":
                print("title:", child.string)
                f.write("title:" + str(child.string) + "\n")
            if child.name == "h3":
                print("author: ", child.a.string)
                f.write("author: " + str(child.a.string) + "\n")
            if child.name == "p":
                if child.string != None:
                    print(child)
                    f.write(textClean(str(child)) + "\n")
                else:## p标签中包含的图片
                    if child.find_all("img"):
                        imgUrl = child.find_all("img")[0].attrs['data-lazy-src']
                        print("<img src='https://xcx.mdavid.cn/Imaegs/" + imgUrl.split("/")[-1] + "'></img>")
                        f.write("<img src='https://xcx.mdavid.cn/Imaegs/" + imgUrl.split("/")[-1] + "'></img>" + "\n")
                        getImg(imgUrl)

            if child.name == "div":
                print(child.attrs)
##                if child.attrs['class'] == ['image-with-text']:## 文章的另一个主要形式，应该单独找出来解析
##                    print("yes ignore")
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

##                elif child.attrs == {'class': ['figcenter']} or child.attrs == {'class': ['figleft']} or child.attrs == {'class': ['figright']}:## 包含图片的div
##                    if child.find_all("img"):
##                        imgUrl = child.find_all("img")[0].attrs['data-lazy-src']
##                        print("<img src='https://xcx.mdavid.cn/Imaegs/" + imgUrl.split("/")[-1] + "'></img>")
##                        f.write("<img src='https://xcx.mdavid.cn/Imaegs/" + imgUrl.split("/")[-1] + "'></img>" + "\n")
##                        getImg(imgUrl)
                    
                elif child.attrs == {'class': ['poem']}:## 包含blockquote标签的div
                    soup1 = BeautifulSoup(textClean(str(child)), "html.parser")
                    print(soup1.prettify())
                    f.write(str(soup1.prettify()) + "\n")

                            
                else:## allStories中的其他div，一般由插入图片时自动生成的div，其attrs不是固定的
                    if child.find_all("img"):## 包含图片
                        print(child.attrs)
                        if child.find_all("img")[0].attrs['data-lazy-src']:
                            imgUrl = child.find_all("img")[0].attrs['data-lazy-src']
                            print("<img src='https://xcx.mdavid.cn/Imaegs/" + imgUrl.split("/")[-1] + "'></img>")
                            f.write("<img src='https://xcx.mdavid.cn/Imaegs/" + imgUrl.split("/")[-1] + "'></img>" + "\n")
                            getImg(imgUrl)
                            
##                    if child.find_all("p"):## 包含p
##                        if child.string != None:
##                            print(child)
##                            f.write(textClean(str(child)) + "\n")
##                            
##                    if child.find_all("span"):## 包含span
##                        for item in child.find_all("span"):
##                            if item.string != None:
##                                print(item)
##                                f.write(str(child) + "\n")
                            

            else:## allStories中的其他标签
                print()

        ## image-with-text
        if soup.find_all("div", "image-with-text"):
            if soup.find_all("p", "drop-caps"):
                print(soup.find_all("p", "drop-caps")[0].text)
                f.write(soup.find_all("p", "drop-caps")[0].text + "\n")
            
            for item in soup.find_all("span"):## span
                if item.parent.name == "p":
                    if item.attrs != {'class': ['required']} and item.attrs != {'id': 'email-notes'}:
                        print(item)
                        f.write(str(item.prettify()) + "\n")
            
            for child in soup.find_all("div", "image-with-text"):
                if child.find_all("img"):
                    imgUrl = child.img.attrs['data-lazy-src']
                    print("<img src='https://xcx.mdavid.cn/Imaegs/" + imgUrl.split("/")[-1] + "'></img>")
                    f.write("<img src='https://xcx.mdavid.cn/Imaegs/" + imgUrl.split("/")[-1] + "'></img>" + "\n")
                    getImg(imgUrl)
                print(child.text)
                f.write(child.text + "\n")

        
        print("*********Article Info*********")
        f.write("\n" + "*********Article Info*********" + "\n")

        ## end-story-section
        for li in soup.find_all("div", "end-story-section")[0].ul:
            if str(li)[4] == "B":
                print("Author: ")
                f.write("Author: ")
                for item in li.find_all("a"):
                    print(item.string)
                    f.write(item.string + " ")
                print("-------")
                f.write("\n" + "-------" + "\n")
            if str(li)[4] == "A":
                if str(li)[5] == "g":
                    print("Age range: ")
                    f.write("Age range: ")
                    for item in li.find_all("a"):
                        print(item.string)
                        f.write(item.string + " ")
                    print("-------")
                    f.write("\n" + "-------" + "\n")
                else:
                    print("Animals: ")
                    f.write("Animals: ")
                    for item in li.find_all("a"):
                        print(item.string)
                        f.write(item.string + " ")
                    print("-------")
                    f.write("\n" + "-------" + "\n")
            if str(li)[4] == "C":
                print("Category: ")
                f.write("Category: ")
                for item in li.find_all("a"):
                    print(item.string)
                    f.write(item.string + " ")
                print("-------")
                f.write("\n" + "-------" + "\n")
            if str(li)[4] == "R":
                print("Reading time: ")
                f.write("Reading time: ")
                for item in li.find_all("a"):
                    print(item.string)
                    f.write(item.string + " ")
                print("-------")
                f.write("\n" + "-------")

        
        f.close()

    return ""


def main():
    start = 4## 从linkList.txt第(start+1)行开始
    end = 6## 到第end行结束
    urlList = getTaskList(start, end)
    count = 0
    for item in urlList:
        print("----------", count, "----------")
        path = saveArticle(item.split("/")[-2])
        html = getHTMLText(item)
        getArticle(html, path)
        count = count + 1
        print("***************************")
    print(count, "篇文章爬取成功")

main()
