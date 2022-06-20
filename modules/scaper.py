def scaper(s, c): # string scaper(string s, char c)
    ac = 0
    l = [i for i in s]
    x = ""
    for i in range(len(s)):
        if s[i] == c:
            l.insert(i+ac,'\\')
            ac += 1
    for i in l: x += i
    return x

if __name__=='__main__':
    s = input("string: ")
    import json
    print(json.loads('{"txt": "%s"}' % scaper(s,'"')))
