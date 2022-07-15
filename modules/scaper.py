def scaper(s, c): # string scaper(string s, char c)
    return repr(s.replace(c, ('\\%s'%c)))[1:-1]

def escaper(s):
    s = repr(s)[1:-1]
    return s.replace('"', '\\"')

if __name__=='__main__':
    s = input("string: ")
    import json
    s = scaper(s,'"')
    print(s)
    print(json.loads('{"txt": "%s"}' % s))
