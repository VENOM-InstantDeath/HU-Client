def scaper(s, c): # string scaper(string s, char c)
    ac = 0
    s = s.encode('unicode_escape').decode('utf-8')
    return s.replace(c, ('\\%s'%c).encode("unicode_escape").decode("utf-8"))

if __name__=='__main__':
    s = input("string: ")
    import json
    print(json.loads('{"txt": "%s"}' % scaper(s,'"')))
