import curses
import socket
import json
from modules import ncRead
from modules.ncRead import ampsread
from modules.boxsel import vboxsel, hboxsel
from curses.textpad import rectangle
from shlex import split
from threading import Thread
#from time import sleep
from os import _exit

#def server():
#    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#    srv.bind(("127.0.0.1", 4444))
#    srv.listen()
#    conn, addr = srv.accept()
#    while True:
#        data = conn.recv(2048)
#        conn.sendall(data)

#def msger(sock):
#    while True:
#        sleep(2)
#        sock.sendall('{"name": "Anonymous", "msg": "Just a test."}'.encode())

def rcver(sock, win, wint):
    while True:
        try:
            data = sock.recv(2048).decode()
        except ConnectionResetError:
            win.addstr(f'SYSTEM: Ha ocurrido un error y el programa ha dejado de funcionar. Reinicia la app, puedes cerrar escribiendo "ixil"')
            win.noutrefresh()
            wint.touchwin()
            wint.noutrefresh()
            curses.doupdate()
            break
        if not data:
            break
        msg = eval(data)
        win.addstr(f'{msg["name"]}: {msg["msg"]}\n')
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

def design_1(stdscr,y,x,cx,user,chat):
    # Arrancar server
    #sv = Thread(target=server)
    #sv.start()
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
    chats = ["Chat oficial","EssEnemiGz","Arch","Staff","Logs","Bots","Python","C/C++","Slackware","Repositorios"]
    opts = ["Chatrooms", "Publicaciones", "Ajustes", "Cerrar Sesión"]
    for i in range(len(chats)):
        Wul.addstr(i,2,chats[i])
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

    #####################
    # Inicio de threads #
    #####################
    clt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clt.connect(("181.164.171.34", 5555))
    rc = Thread(target=rcver, args=(clt,Wr, Wb))
    #ms = Thread(target=msger, args=(clt,))
    rc.start()#;ms.start()

    #########
    # Input #
    #########
    curses.curs_set(1)
    Wb.keypad(1)
    Wr.scrollok(1)
    curses.echo()
    while True:
        msg = ampsread(Wb,1,0,(x-2)-24,200)
        if msg == "ixil":
            curses.endwin();_exit(0)
        Wb.move(1,0);Wb.clrtoeol()
        if not msg: continue
        clt.sendall(('{"name": "%s", "msg": "%s"}' % (user,msg)).encode())
        # Wr.addstr(f"{user}:",curses.color_pair(10))
        # Wr.addstr(f" {msg}\n")
        Wb.touchwin()
        stdscr.noutrefresh()
        Wr.noutrefresh()
        Wb.noutrefresh()
        curses.doupdate()

    # TEMPORAL
    stdscr.getch();curses.endwin();exit(0);
    # !-!    

def readondict(stdscr, y, x, vislim, chlim, mode,L, n):
    curses.curs_set(1)
    curses.echo()
    L[n] = ncRead.ampsread(stdscr,y,x,vislim,chlim,mode)
    curses.noecho()
    curses.curs_set(0)

def register(stdscr,creds,cx):
    stdscr.move(6,(cx-(16//2))-13);stdscr.clrtoeol()
    if (not creds["username"]) or (not creds["password"]):
        stdscr.addstr(6,(cx-(16//2))-13,"Todos los campos son obligatorios!",curses.color_pair(10))
        return 1
    if " " in creds["username"]:
        stdscr.addstr(6,(cx-(16//2))-13,"El nombre de usuario no puede contener espacios",curses.color_pair(10))
        return 1
    dbcur.execute(f'select name from user;')
    for i in dbcur.fetchall():
        if i[0] == creds["username"]:
         stdscr.addstr(6,(cx-(16//2))-13,"El nombre de usuario ya existe",curses.color_pair(10))
         return 1
    dbcur.execute(f'insert into user (name, passw) values ("{creds["username"]}", "{creds["password"]}")')
    dbcon.commit()
    login_screen(stdscr,cx)
    return 0


def login(stdscr,creds,cx):
    stdscr.move(6,(cx-(16//2))-13);stdscr.clrtoeol()
    if (not creds["username"]) or (not creds["password"]):
        stdscr.addstr(6,(cx-(16//2))-13,"Todos los campos son obligatorios!",curses.color_pair(10))
        return 1
    """for i in names:
        if i[0] == creds["username"] and i[1] == creds["password"]:
            y, x = stdscr.getmaxyx()
            stdscr.move(3,0);stdscr.clrtobot()
            design_1(stdscr,y,x,cx,creds["username"], 'm1')
            return 0"""
    if (creds["password"] == "demo"):
        y, x = stdscr.getmaxyx()
        stdscr.move(3,0);stdscr.clrtobot()
        design_1(stdscr,y,x,cx,creds["username"], 'm1')
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
             (8, ((cx-(16//2))-13)+19+15, 8, 0, 0),
             (9, ((cx-(16//2))-13)+11+20, 9, 0, 0),
             ((11, (cx-(16//2))-7, 13, (cx-(16//2))+8,1), (11,(cx-(16//2))+10,13,(cx-(16//2))+22,1)),
             (16,(cx-(16//2))+1,18,(cx-(16//2))+12)
            )
    func = (
             lambda: readondict(stdscr,8,((cx-(16//2))-13)+19,15,24,0,creds,"username"),
             lambda: readondict(stdscr,9,((cx-(16//2))-12)+11,20,24,1,creds,"password"),
             (
                 lambda: login_screen(stdscr,cx),
                 lambda: register(stdscr,creds,cx)
             ),
             exit
            )
    curses.noecho()
    vboxsel(stdscr,posit,func)
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
             (8, ((cx-(16//2))-13)+19+15, 8, 0, 0),
             (9, ((cx-(16//2))-13)+11+20, 9, 0, 0),
             ((11, (cx-(16//2))-7, 13, (cx-(16//2))+5,1), (11,(cx-(16//2))+7,13,(cx-(16//2))+22,1)),
             (16,(cx-(16//2))+1,18,(cx-(16//2))+12)
            )
    func = (
             lambda: readondict(stdscr,8,((cx-(16//2))-13)+19,15,24,0,creds,"username"),
             lambda: readondict(stdscr,9,((cx-(16//2))-12)+11,20,24,1,creds,"password"),
             (
                 lambda: register_screen(stdscr,cx),
                 lambda: login(stdscr,creds,cx)
             ),
             exit
            )
    curses.noecho()
    vboxsel(stdscr,posit,func)
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
    stdscr.addstr(1,cx-(15//2),"Hacking-Utils.c (Dev version)", curses.color_pair(17))
    login_screen(stdscr,cx)

curses.wrapper(main)