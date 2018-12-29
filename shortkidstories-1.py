## 英文故事爬虫，爬取所有的链接，生成一个txt文件
## shortkidstories-1.py
## 源站：http://www.shortkidstories.com/story/
## 作者：David

import requests
from bs4 import BeautifulSoup
import bs4

def getHTMLText(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = "utf-8"
        return r.text
    except:
        return ""

## 获取一个页面中全部的文章链接和文章标题
def getArticleInfo(html):
    soup = BeautifulSoup(html, "html.parser")
    with open('linkList.txt', 'a+', encoding = "UTF-8") as f:
        for item in soup.find_all("div", "catalogue"):
            print("title:", item.a.h2.string)
            print("link:", item.a.attrs["href"])
            if not verifyLink(item.a.attrs["href"]):
                f.write(item.a.h2.string + "---" + item.a.attrs["href"] + "\n")
        f.close()

    return ""

def verifyLink(url):
    url += "\n"## 写文件时有换行
    flag = False
    urlList = []
    with open('linkList.txt', 'r', encoding = "UTF-8") as f:
        lines = f.readlines()
        for line in lines:
            urlList.append(line.split("---")[-1])
        f.close()
    if url in urlList:
        print("link已经存在")
        flag = True
    return flag

## 获取所有的页面url
def getALLPage():
    urlList = []
    for i in range(1, 37):
        url = 'http://www.shortkidstories.com/story/page/' + str(i) + '/'
        urlList.append(url)
    return urlList    

def main():
    urlList = getALLPage()
    count = 1
    for item in urlList:
        print("----------", count, "----------")
        html = getHTMLText(item)
        getArticleInfo(html)
        count = count + 1
        print("***************************")

main()

##def reMain():## 需要重复运行几次尽量不遗漏
##    for i in range(5):
##        main()
##    return ""
##
##reMain()
