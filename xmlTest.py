## xmlTest.py

from xml.etree.ElementTree import parse
from xml.etree.ElementTree import Element, SubElement, ElementTree
import os

## 保存每一篇文章
def saveArticle(name):
    root = "D://Python//shortkidstories//Articles//"
    path = root + name + ".xml"
    try:
        if not os.path.exists(root):
            os.mkdir(root)
        if not os.path.exists(path):
            makeXml(path)
        else:
            print(name + ".xml" + "已经存在")
            parseXml(path)
            updateXml(path)
        return path
    except:
        print(name + ".xml" + "创建失败")
        return ""

def makeXml(path):
    
    root = Element('root')
    head = SubElement(root, 'head')
    
    fileName = SubElement(head, 'fileName')
    fileName.text = ''

    title = SubElement(head, 'title')
    title.text = ''

    author = SubElement(head, 'author')
    author.text = ''

    level = SubElement(head, 'level')
    level.text = ''

    category = SubElement(head, 'category')
    category.text = ''

    tag = SubElement(head, 'tag')
    tag.text = ''
    
    length = SubElement(head, 'length')
    length.text = ''
    

    body = SubElement(root, 'body')
    body.text = ''
    
    tree = ElementTree(root)
    tree.write(path, encoding='utf-8')

    return ""

def parseXml(path):
    tree = parse(path)
    root = tree.getroot()
    str1 = tree.findtext('body')
    print(str1)
    
    return ""
def updateXml(path):
    print("update")
    
    tree = parse(path)
    root = tree.getroot()
    
    body = root.find('body')
    
    body.text += "789"
    body.text += "7890000"
    body.text += "7890000456"
    
    tree.write(path)
    
    parseXml(path)
    return ""

def main():
    saveArticle("123")

    return ""

main()
