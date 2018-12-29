def verifyLink(url):
    flag = False
    urlList = []
    with open('linkList.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            urlList.append(line.split("---")[-1])
        f.close()
    if url in urlList:
        print("link已经存在")
        flag = True
    print(urlList)
    return flag

def main():
    url = "http://www.shortkidstories.com/story/white-cat/" + "\n"
    print(verifyLink(url))
    
main()
