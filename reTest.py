import re

def main():
    garbageText = ' class="(.*)?"'
    str1 = ' class="abc"'
    str2 = '<p class="drop-caps">It was '
    str3 = '<div class="poem"><blockquote><div class="stanza">“Tell me, glass, tell me true! Of all the ladies in the land, Who is fairest? tell me who?”</div></blockquote></div>'

    test = re.search(garbageText, str3)
    if test:
        print("YES")
        
    print(re.sub(garbageText, "", str1))
    print(re.sub(garbageText, "", str2))
    print(re.sub(garbageText, "", str3))
    return ""
main()
