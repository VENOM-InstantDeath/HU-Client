import curses
import locale
from curses import KEY_BACKSPACE, KEY_LEFT, KEY_RIGHT

locale.setlocale(locale.LC_ALL, '')

def listostr(l):
    if not isinstance(l,list): raise ValueError
    s = ""
    for i in l:
        s += i
    return s

def clrbox(stdscr, y, x, minlim, vislim):
    for i in range(x,x+(vislim-minlim)+1):
        stdscr.addch(y,i,32)


# Amplified sread()
def ampsread(stdscr,y,x,vislim=30,chlim=30,mode=0):
    curses.cbreak()
    curses.noecho()

    string = []
    p = 0
    sp = 0
    minlim = 0
    clrbox(stdscr,y,x,minlim,vislim)

    while True:
        ch = stdscr.get_wch(y,x+p)
        if isinstance(ch, str):
            if ord(ch) == 127: ch = KEY_BACKSPACE
            elif ord(ch) == 8: ch = KEY_BACKSPACE
        if ch == chr(4):
            pass
        if ch == chr(27):
            return None
        if ch == '\n':
            return listostr(string)
        if ch == KEY_BACKSPACE:
            if not sp: continue
            string.pop(sp-1)
            clrbox(stdscr,y,x,minlim,vislim)
            if not p and sp:
                vislim -= 1
                minlim -= 1
            acum1 = 0
            for i in string[minlim:vislim+1]:
                if mode: stdscr.addch(y,x+acum1,'*')
                else: stdscr.addch(y,x+acum1,i)
                acum1 += 1
            if not (not p and sp): p -= 1
            sp -= 1
            continue
        if ch == KEY_RIGHT:
            if sp == len(string): continue
            if sp == vislim:
                vislim += 1
                minlim += 1
                clrbox(stdscr,y,x,minlim,vislim)
                acum1 = 0
                for i in string[minlim:vislim+1]:
                    if mode: stdscr.addch(y,x+acum1,'*')
                    else: stdscr.addch(y,x+acum1,i)
                    acum1 += 1
                sp += 1
                continue
            p += 1
            sp += 1
        if ch == KEY_LEFT:
            if not sp: continue
            if not p and sp:
                vislim -= 1
                minlim -= 1
                clrbox(stdscr,y,x,minlim,vislim)
                acum1 = 0
                for i in string[minlim:vislim+1]:
                    if mode: stdscr.addch(y,x+acum1,'*')
                    else: stdscr.addch(y,x+acum1,i)
                    acum1 += 1
                sp -= 1
                continue
            p -= 1
            sp -= 1
        if len(string) == chlim: continue
        if isinstance(ch, int): continue
        string.insert(sp,ch)
        clrbox(stdscr,y,x,minlim,vislim)
        if sp == vislim:
            vislim += 1
            minlim += 1
            acum1 = 0
            for i in string[minlim:vislim+1]:
                if mode: stdscr.addch(y,x+acum1,'*')
                else: stdscr.addstr(y,x+acum1,i)
                acum1 += 1
            sp += 1
            continue
        acum1 = 0
        for i in string[minlim:vislim+1]:
            if mode: stdscr.addch(y,x+acum1,'*')
            else: stdscr.addstr(y,x+acum1,i)
            acum1 += 1
        sp += 1
        p += 1

# End


def sread(stdscr,y,x,chlim=30):
    curses.cbreak()
    curses.curs_set(1)

    string = []
    p = 0

    while True:
        ch = stdscr.getch(y,x+p)
        if ch == 4:
            return
        if ch == 10:
            return listostr(string)
        if (ch in range(65,91)) or (ch in range(97,123)) or (ch == 32):
            if len(string) == chlim: continue
            string.insert(p,chr(ch))
            clrbox(stdscr,y,x,minlim,vislim)
            acum1 = 0
            for i in range(x,x+len(string)):
                stdscr.addch(y,i,string[acum1])
                acum1 += 1
            p += 1
        if ch == KEY_BACKSPACE:
            if not p: continue
            string.pop(p-1)
            clrbox(stdscr,y,x,minlim,vislim)
            acum1 = 0
            for i in range(x,x+len(string)):
                stdscr.addch(y,i,string[acum1])
                acum1 += 1
            p -= 1
        if ch == KEY_RIGHT:
            if p == len(string): continue
            p += 1
        if ch == KEY_LEFT:
            if not p: continue
            p -= 1

if __name__ == "__main__":
    def main(stdscr):
        curses.use_default_colors()
        curses.curs_set(0)
        stdscr.addstr(0,0,"Input:")
        s = ampsread(stdscr,0,7,7,20)
        stdscr.addstr(2,0,f"String: {s}")
        stdscr.getch()
        curses.endwin()

    curses.wrapper(main)
