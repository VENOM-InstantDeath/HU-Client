import curses
from modules.menu import menu


def writer(*p):
    F=open("modules/address", 'w+');s=BASEAD.split('.')
    for i in range(2): s[i]=str(int(BASEAD.split('.')[i])*p[i])
    s[2]=str(p[2]);s[3]=str(p[3])
    F.write(''.join([i+'.' for i in s])[:-1]);F.close()

def main(stdscr):
    y,x = stdscr.getmaxyx()
    y //= 2;x //= 2
    stdscr.addstr(y-4, x-12, "Backend Adress Selector")
    d = {
            "Main": lambda: writer(1,82,171,34),
            "Alternative": lambda: writer(1,23,102,248)
        }
    menu(stdscr,y,x,d)

BASEAD = '181.2.0.17'
curses.wrapper(main)
