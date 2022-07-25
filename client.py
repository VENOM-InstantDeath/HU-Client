import curses
import socket
import json
from requests import get
from hashlib import md5
from modules import ncRead
from modules.ncRead import ampsread
from modules.boxsel import boxsel
from modules.menu import menu
from os import path
from curses.textpad import rectangle
from modules.scaper import escaper
from shlex import split
from threading import Thread
from os import _exit
VERSION = '1.3.0'
DEBUG = 1

F = open("scroll.log", 'w+')

def msg_split(s):
    c = []
    sc = [0,0]
    sl = []
    for i in range(len(s)):
        if s[i] == '{': sc[0] = i
        if s[i] == '}':
            sc[1] = i
            c.append(sc)
            sc = [0,0]
    for i in c:
        sl.append(s[i[0]:i[1]+1])
    return sl

def msg_lines(nick, msg, x):
    # ( <venom>: lorem ipsum dolor ) -> size // x
    msg = f'<{nick}>: {msg}'
    lines = (len(f'<{nick}>: {msg}')//x)+1
    lines_list = []
    for i in range(lines):
        lines_list.append(msg[x*i:x*(i+1)])
    return lines_list

def rcver(sock, win, wint, A_CHAT, msglines, x, msgcur, WRITE, unprinted):
    while True:
        try:
            data = sock.recv(2048).decode('utf-8')
        except ConnectionResetError:
            win.addstr(f'<SYSTEM>: Ha ocurrido un error y el programa ha dejado de funcionar. Reinicia la app.')
            win.noutrefresh()
            wint.touchwin()
            wint.noutrefresh()
            curses.doupdate()
            win.addstr('<SYSTEM>: Saliendo...')
            win.noutrefresh()
            wint.touchwin()
            wint.noutrefresh()
            curses.doupdate()
            curses.napms(2000)
            sock.close()
            curses.endwin()
            _exit(0)
        if not data:
            break
        json_list = msg_split(data)
        for i in json_list:
            try:
                msg = json.loads(data, strict=False)
                if msg["chat"] != A_CHAT[0]: continue
            except Exception as e:
                continue
            try:
                lines = msg_lines(msg["name"], msg["msg"], x)
                msglines.extend(lines)
                msgcur[0] += len(lines); msgcur[1] += len(lines)
                if not WRITE[0]:
                    unprinted.append(f'<{msg["name"]}>: {msg["msg"]}\n')
                    continue
                win.addstr(f'<{msg["name"]}>: {msg["msg"]}\n')
            except KeyError:
                win.addstr('<SYSTEM>: KeyError on rcver thread.\n')
                win.addstr(f'<SYSTEM>: {msg}\n')
                win.addstr('<SYSTEM> Saliendo...')
                win.noutrefresh()
                wint.touchwin()
                wint.noutrefresh()
                curses.doupdate()
                curses.napms(5000)
                sock.close()
                curses.endwin()
                _exit(0)
        win.noutrefresh()
        wint.touchwin()
        wint.noutrefresh()
        curses.doupdate()

# TEMPORAL
def debug(name, value):
    print(f"{name}: {value}")
# !-!

def fill_rectangle(stdscr, y1,x1, y2,x2):
    lines=y2-(y1+1)
    n = x1+1
    for i in range(lines):
        stdscr.attron(curses.color_pair(1))
        stdscr.move(y1+(i+1), x1+1)
        for i in range(x2-1):
            stdscr.addch(" ")
        stdscr.attroff(curses.color_pair(1))

def clrbox(stdscr,y1,x1,y2,xm):
    for i in range(y1,y2+1):
        for e in range(x1,xm+1):
            stdscr.addch(i,e,' ')

def msgscroll(Wr, Wr_y, Wb, Wb_x, msglines, msgcur, WRITE, unprinted):
    WRITE[0] = 0
    F = open("scroll.log", 'a')
    F.write(f'msgcur: {msgcur}\n')
    F.write(f'len_msglines: {len(msglines)}\n')
    F.write(f'msglines: {msglines}\n')
#    F.write(f'og:line_a: {msglines[msgcur[0]]}\n')
#    F.write(f'og:line_b: {msglines[msgcur[1]]}\n')
    curcpy = msgcur.copy()
    while True:
        k = Wr.getch()
        if k == 27:
            for i in unprinted: pass
            unprinted.clear()
            WRITE[0] = 1
            F.close()
            return 0
        if k == curses.KEY_UP:
            if not curcpy[0]:
                F.write('KEY_UP continue\n')
                continue
            curcpy[0] -= 1; curcpy[1] -= 1
            Wr.scroll(-1)
            Wr.addstr(0,0,msglines[curcpy[0]])
            Wr.noutrefresh()
            for i in range(Wb_x):
                Wb.addch(0, i, curses.ACS_HLINE)
            Wb.noutrefresh()
            Wr.noutrefresh()
            curses.doupdate()
        if k == curses.KEY_DOWN:
            # quité el -1 del len(msglines)-1
            # pasa que pensé que tengo que sumar al
            # msgcur[1] la cantidad de líneas nuevas
            # y no de mensajes, porque los mensajes
            # pueden tener más de una línea.
            # Y como le sumo al msgcur[1], lo mismo
            # le tengo que sumar al msgcur[0].
            #
            # El índice empieza desde 0. len(msglines)
            # tiene que tener su -1. No entiendo.
            F.write(f'curcpy: {curcpy}')
            if curcpy[1] == len(msglines)-1:
                F.write('KEY_DOWN continue\n')
                continue
            curcpy[0] += 1; curcpy[1] += 1
            Wr.scroll(1)
            Wr.addstr(Wr_y-2,0,msglines[curcpy[1]])
            Wr.noutrefresh()
            for i in range(Wb_x):
                Wb.addch(0, i, curses.ACS_HLINE)
            Wb.noutrefresh()
            Wr.noutrefresh()
            curses.doupdate()

def readbox(stdscr,Wb,Wr,x,A_CHAT):
    curses.curs_set(1)
    curses.echo()
    while True:
        msg = ampsread(Wb,1,0,(x-2)-24,200)
        if msg == "ixil":
            curses.endwin();clt.close();_exit(0)
        Wb.move(1,0);Wb.clrtoeol()
        if msg == None: return 0
        if not msg: continue
        #TODO! BROKEN PIPE ERROR HANDLE ! TODO#
        clt.sendall(('{"operation": "2", "msg": "%s", "chat": %s, "reply": 0, "type": 0}' % (escaper(msg), A_CHAT[0])).encode('utf-8'))
        Wb.touchwin()
        stdscr.noutrefresh()
        Wr.noutrefresh()
        Wb.noutrefresh()
        curses.doupdate()

def chatselect(chat, A_CHAT, Wr, Wb, Wb_x, msglines, Wr_x, Wr_y, msgcur):
    A_CHAT[0] = chat
    msgcur.clear()
    msgcur.extend((0,0))
    Wr.erase()
    Wr.noutrefresh()
    curses.doupdate()
    clt.sendall(('{"operation": "3", "get": "chat", "msg": 50, "id": %s}' % chat).encode('utf-8'))
    BUFF_SIZE = int(clt.recv(8).decode())
    clt.send("1".encode())
    data = b''
    while True:
        data += clt.recv(BUFF_SIZE)
        if len(data) != BUFF_SIZE: continue
        else: break
    msgs = json.loads(data.decode('utf-8'))
    msgs.reverse()
    msglines.clear()
    for i in msgs:
        msglines.extend(msg_lines(i[6],i[3],Wr_x))
        Wr.addstr(f'<{i[6]}>: {i[3]}\n')
    if Wr_y-2 > len(msglines):
        msgcur[0] = 0
    else:
        msgcur[0] = len(msglines)-(Wr_y-2)
    msgcur[1] = len(msglines)-1
    Wr.noutrefresh()
    for i in range(Wb_x):
        Wb.addch(0, i, curses.ACS_HLINE)
    Wb.noutrefresh()
    curses.doupdate()

def mklam(*args):
    return lambda: args[0](*args[1:])

#!temporal
def ixil():
    curses.endwin()
    clt.close()
    _exit(0)
def _pass(): return 0
#

def design_1(stdscr,y,x,cx):
    A_CHAT = [1]
    WRITE = [1]
    stdscr.move(3,0);stdscr.clrtobot()
    ######################################
    # Obtención de los datos del usuario #
    ######################################
    USER = clt.recv(32).decode('utf-8')
    stdscr.addstr(2,1,f"Username: {USER}")

    ###########################
    # Dibujado de rectángulos #
    ###########################
    rectangle(stdscr,3,0,y-6,20)
    rectangle(stdscr,y-6,0,y-1,20)
    rectangle(stdscr,3,21,y-1,x-2)
    stdscr.addch(y-6,0,curses.ACS_LTEE)
    stdscr.addch(y-6,20,curses.ACS_RTEE)

    ###################################
    # Creación de objetos de ventanas #
    ###################################
    Wul = curses.newwin((y-6)-3-1,19,  4,1)
    Wdl = curses.newwin((y-1)-(y-6)-1,19,  y-5,1)
    Wr  = curses.newwin((y-3)-3,(x-2)-22, 4,22)
    Wb = curses.newwin(2,(x-2)-22,y-3,22) # Caja de texto

    caps = [[0,0], [0,0], [0,0], [0,0]]
    caps[0][0], caps[0][1] = Wul.getmaxyx()
    caps[1][0], caps[1][1] = Wdl.getmaxyx()
    caps[2][0], caps[2][1] = Wr.getmaxyx()
    caps[3][0], caps[3][1] = Wb.getmaxyx()

    for i in range(caps[3][1]):
        Wb.addch(0, i, curses.ACS_HLINE)

    #######################################
    # Escritura de los paneles izquierdos #
    #######################################
    clt.sendall('{"operation": "3", "get": "chatls"}'.encode('utf-8'))
    chats = clt.recv(2048).decode('utf-8')
    chats = json.loads(chats)
    opts = ["Chatrooms", "Cerrar Sesión"]
    for i in range(len(chats)):
        Wul.addstr(i,2,chats[i][3])
    Wul.addstr(0, 0, '*')
    for i in range(len(opts)):
        Wdl.addstr(i,2,opts[i])
    Wdl.addstr(0, 0, '*')

    stdscr.noutrefresh()
    Wul.noutrefresh()
    Wdl.noutrefresh()
    Wr.noutrefresh()
    Wb.noutrefresh()
    curses.doupdate()

    #####################################
    # Obtención y escritura de mensajes #
    #####################################
    # Wr
    msglines = []
    unprinted = []
    msgcur = [0,0]
    clt.sendall('{"operation": "3", "get": "chat", "msg": 50, "id": 1}'.encode('utf-8'))
    BUFF_SIZE = int(clt.recv(8).decode())
    clt.send("1".encode())
    data = b''
    while True:
        data += clt.recv(BUFF_SIZE)
        if len(data) != BUFF_SIZE: continue
        else: break
    msgs = json.loads(data.decode('utf-8'))
    msgs.reverse()
    Wr.scrollok(1)
    msgcur[0] = len(msgs)-(caps[2][0]-2)
    msgcur[1] = len(msgs)
    for i in msgs:
        msglines.extend(msg_lines(i[6], i[3], caps[2][1]))
        Wr.addstr(f'<{i[6]}>: {i[3]}\n')
    Wr.noutrefresh()
    for i in range(caps[3][1]):
        Wb.addch(0, i, curses.ACS_HLINE)
    Wb.noutrefresh()
    curses.doupdate()
    #####################
    # Inicio de threads #
    #####################
    rc = Thread(target=rcver, args=(cltch,Wr, Wb, A_CHAT, msglines, caps[2][1], msgcur, WRITE, unprinted))
    rc.start()

    #########
    # Input #
    #########
    Wb.keypad(1)
    Wr.keypad(1)
    Wul.keypad(1)
    Wdl.keypad(1)
    pos = (
            ((3,3,10,1, 0),(3,3,(21+(x-2))//2,1, 0)),
            ((3,y-6,10,1, 0),(3,y-3,(22+(x-2))//2,1, 0))
        )
    wdl_dict = {
        "Chatrooms": _pass,
        "Cerrar Sesión": ixil
    }
    wul_dict = {}
    for i in chats:
        wul_dict[i[3]] = mklam(chatselect, i[0], A_CHAT, Wr, Wb, caps[3][1], msglines, caps[2][1], caps[2][0], msgcur)
    # def msgscroll(Wr, Wr_y, Wb, Wb_x, msglines, msgcur):
    func = (
            (lambda: menu(Wul,0,2,wul_dict,aster=1), lambda: msgscroll(Wr, caps[2][0], Wb, caps[3][1], msglines, msgcur, WRITE, unprinted)),
            (lambda: menu(Wdl,0,2,wdl_dict,aster=1), lambda: readbox(stdscr, Wb, Wr,x,A_CHAT))
        )
    curses.curs_set(0)
    curses.noecho()
    while True:
        boxsel(stdscr,pos,func)
        curses.curs_set(0)
        curses.noecho()

def readondict(stdscr, y, x, vislim, chlim, mode,L, n):
    curses.curs_set(1)
    curses.echo()
    L[n] = ncRead.ampsread(stdscr,y,x,vislim,chlim,mode)
    curses.noecho()
    curses.curs_set(0)
    return 1

def register(stdscr,creds,cx):
    stdscr.move(6,(cx-(16//2))-13);stdscr.clrtoeol()
    if (not creds["username"]) or (not creds["password"]):
        stdscr.addstr(6,(cx-(16//2))-13,"Todos los campos son obligatorios!",curses.color_pair(10))
        return 1
    if ("\n" in creds["username"] or "\t" in creds["username"]):
        stdscr.addstr(6,(cx-(16//2))-13,"",curses.color_pair(10))
        return 1
    if " " in creds["username"]:
        stdscr.addstr(6,(cx-(16//2))-13,"El nombre de usuario no puede contener espacios",curses.color_pair(10))
        return 1 
    clt.sendall(('{"operation": "0", "username":"%s", "password":"%s"}' % (creds['username'], creds['password'])).encode('utf-8'))
    rsp = clt.recv(1024).decode('utf-8')
    if rsp == '1':
        stdscr.addstr(6,(cx-(16//2))-13,"El nombre de usuario ya existe",curses.color_pair(10))
        return 1
    else:
        login_screen(stdscr,cx)
    return 0


def login(stdscr,creds,cx):
    stdscr.move(6,(cx-(16//2))-13);stdscr.clrtoeol()
    if (not creds["username"]) or (not creds["password"]):
        stdscr.addstr(6,(cx-(16//2))-13,"Todos los campos son obligatorios!",curses.color_pair(10))
        return 1
    clt.sendall(('{"operation": "1", "username":"%s", "password":"%s"}' % (creds['username'], creds['password'])).encode('utf-8'))
    rsp = clt.recv(1024).decode('utf-8')
    if rsp == "0":
        y, x = stdscr.getmaxyx()
        design_1(stdscr,y,x,cx)
    else:
        stdscr.addstr(6,(cx-(16//2))-13,"Usuario o contraseña incorrectos",curses.color_pair(10))
    return 1

def register_screen(stdscr,cx):
    stdscr.move(3,0);stdscr.clrtobot()
    stdscr.addstr(4,cx-(8//2),"Registro", curses.A_UNDERLINE)
    stdscr.addstr(8,(cx-(16//2))-13,"Nombre de usuario: ")
    stdscr.addstr(9,(cx-(16//2))-13,"Contraseña:")
    rectangle(stdscr,11,(cx-(16//2))+10, 13,(cx-(16//2))+22)
    stdscr.addstr(12,(cx-(16//2)+11), "Registrarse")
    rectangle(stdscr,11,(cx-(16//2))-7, 13,(cx-(16//2))+8)
    stdscr.addstr(12,(cx-(16//2)-6),"Iniciar Sesión")
    rectangle(stdscr,16,(cx-(16//2))+1,18,(cx-(16//2))+12)
    stdscr.addstr(17,(cx-(16//2)+5),"Exit")
    curses.echo()
    curses.curs_set(0)
    creds = {"username":"","password":""}
    posit = (
             ((2, 8, ((cx-(16//2))-13)+19, 15, 1),),
             ((2, 9, ((cx-(16//2))-13)+11, 20, 1),),
             ((0, 11, (cx-(16//2))-7, 13, (cx-(16//2))+8,1), (0, 11,(cx-(16//2))+10,13,(cx-(16//2))+22,1)),
             ((0, 16,(cx-(16//2))+1,18,(cx-(16//2))+12,0),)
            )
    func = (
             (lambda: readondict(stdscr,8,((cx-(16//2))-13)+19,15,24,0,creds,"username"),),
             (lambda: readondict(stdscr,9,((cx-(16//2))-12)+11,20,24,0,creds,"password"),),
             (
                 lambda: login_screen(stdscr,cx),
                 lambda: register(stdscr,creds,cx)
             ),
             (exit,)
            )
    curses.noecho()
    boxsel(stdscr,posit,func)
    curses.echo()
    curses.curs_set(0)


def login_screen(stdscr,cx):
    stdscr.move(3,0);stdscr.clrtobot()
    stdscr.addstr(4,cx-(16//2),"Inicio de sesión", curses.A_UNDERLINE)
    stdscr.addstr(8,(cx-(16//2))-13,"Nombre de usuario: ")
    stdscr.addstr(9,(cx-(16//2))-13,"Contraseña:")
    rectangle(stdscr,11,(cx-(16//2))-7, 13,(cx-(16//2))+5)
    stdscr.addstr(12,(cx-(16//2)-6), "Registrarse")
    rectangle(stdscr,11,(cx-(16//2))+7, 13,(cx-(16//2))+22)
    stdscr.addstr(12,(cx-(16//2)+8),"Iniciar Sesión")
    rectangle(stdscr,16,(cx-(16//2))+1,18,(cx-(16//2))+12)
    stdscr.addstr(17,(cx-(16//2)+5),"Exit")
    curses.echo()
    curses.curs_set(0)
    creds = {"username":"","password":""}
    posit = (
             ((2, 8, ((cx-(16//2))-13)+19, 15, 1),),
             ((2, 9, ((cx-(16//2))-13)+11, 20, 1),),
             ((0, 11, (cx-(16//2))-7, 13, (cx-(16//2))+5,1), (0, 11,(cx-(16//2))+7,13,(cx-(16//2))+22,1)),
             ((0, 16,(cx-(16//2))+1,18,(cx-(16//2))+12,0),)
            )
    func = (
             (lambda: readondict(stdscr,8,((cx-(16//2))-13)+19,15,24,0,creds,"username"),),
             (lambda: readondict(stdscr,9,((cx-(16//2))-12)+11,20,24,1,creds,"password"),),
             (
                 lambda: register_screen(stdscr,cx),
                 lambda: login(stdscr,creds,cx)
             ),
             (exit,)
            )
    curses.noecho()
    boxsel(stdscr,posit,func)
    curses.echo()
    curses.curs_set(0)

def main(stdscr):
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1,curses.COLOR_BLACK,curses.COLOR_GREEN)
    curses.init_pair(17, 17, curses.COLOR_GREEN)
    curses.init_pair(2,curses.COLOR_GREEN,curses.COLOR_GREEN)
    curses.init_pair(10,9,-1)
    curses.curs_set(0)
    y,x = stdscr.getmaxyx()
    cx = x//2
    fill_rectangle(stdscr,0,0,2,x-1)
    stdscr.addstr(1,cx-(15//2),"Hacking-Utils.c (Demo version)", curses.color_pair(17))
    clt.sendall('{"operation": "3", "get": "version"}'.encode('utf-8'))
    L_VERSION = clt.recv(16).decode()
    if L_VERSION != VERSION:
        win = curses.newwin(4,50, (y//2)-4, cx-25)
        win.addstr(0,0,"El cliente está desactualizado, actualízalo para continuar.")
        win.addstr(3,25-(len("[ok]")//2),"[OK]",curses.color_pair(1))
        stdscr.refresh()
        win.refresh()
        while True:
            k = win.getch()
            if k == 10:
                curses.endwin()
                clt.close()
                exit(0)
    if IN_DEVELOPMENT:
        win = curses.newwin(4,50, (y//2)-4, cx-25)
        win.addstr(0,0,"El server se encuentra en mantenimiento, por lo que puede estar inestable.")
        win.addstr(3,25-(len("[ok]")//2),"[OK]",curses.color_pair(1))
        stdscr.refresh()
        win.refresh()
        while True:
            k = win.getch()
            if k == 10:
                del win
                stdscr.touchwin()
                stdscr.refresh()
                break
    clt.sendall('{"operation": "3", "get": "fchk"}'.encode())
    L_FCHK = clt.recv(512).decode('utf-8')
    L_FCHK = json.loads(L_FCHK)
    FCHK_ERR = 0
    for i in L_FCHK:
        if not path.exists(i):
            FCHK_ERR = 1
            break
        F = open(i, 'rb')
        if not md5(F.read()).hexdigest() in L_FCHK[i]:
            FCHK_ERR = 1
            break
        F.close()
    if FCHK_ERR:
        win = curses.newwin(4,50, (y//2)-4, cx-25)
        win.addstr(0,0,"Ha ocurrido un error en el cliente y el mismo no puede iniciarse.")
        win.addstr(3,25-(len("[salir]")//2),"[Salir]",curses.color_pair(1))
        stdscr.refresh()
        win.refresh()
        while True:
            k = win.getch()
            if k == 10:
                del win
                stdscr.touchwin()
                stdscr.refresh()
                exit(1)
    login_screen(stdscr,cx)

clt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
svad = open("modules/address").read().strip()
clt.connect((svad, 5555))
cltch = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cltch.connect((svad, 5556))
clt.sendall("24eds124".encode())
IN_DEVELOPMENT = int(clt.recv(20).decode())

curses.wrapper(main)
