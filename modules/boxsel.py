import curses
from curses.textpad import rectangle

def vboxsel(stdscr, posit, funct):
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_GREEN)
    p = 0
    sp = 0

    stdscr.attron(curses.color_pair(1))
    if isinstance(posit[0][0], tuple):
        if posit[0][0][0] == posit[0][0][2]:
            stdscr.attroff(curses.color_pair(1))
            stdscr.addch(posit[0][0][0],posit[0][0][1], '<')
            stdscr.attron(curses.color_pair(1))
        else:
            rectangle(stdscr,posit[0][0][0],posit[0][0][1],posit[0][0][2],posit[0][0][3])
    else:
        if posit[0][0] == posit[0][2]:
            stdscr.attroff(curses.color_pair(1))
            stdscr.addch(posit[0][0],posit[0][1], '<')
            stdscr.attron(curses.color_pair(1))
        else:
            rectangle(stdscr,posit[0][0],posit[0][1],posit[0][2],posit[0][3])
    stdscr.attroff(curses.color_pair(1))
    while True:
        k = stdscr.getch()
        if isinstance(posit[p][0], tuple):
            if posit[p][sp][0] == posit[p][sp][2]:
                stdscr.addch(posit[p][sp][0],posit[p][sp][1], ' ')
            else:
                rectangle(stdscr, posit[p][sp][0], posit[p][sp][1], posit[p][sp][2], posit[p][sp][3])
        else:
            if posit[p][0] == posit[p][2]:
                stdscr.addch(posit[p][0],posit[p][1], ' ')
            else:
                rectangle(stdscr,posit[p][0], posit[p][1], posit[p][2], posit[p][3])
        if k == curses.KEY_LEFT:
            if isinstance(posit[p][0], tuple):
                if sp:
                    sp -= 1
        if k == curses.KEY_RIGHT:
            if isinstance(posit[p][0], tuple):
                if sp != len(posit[p])-1:
                    sp += 1
        if k == curses.KEY_DOWN:
            if p != len(posit)-1:
                p += 1
        if k == curses.KEY_UP:
            if p:
                p -= 1
        if k == 10:
            if isinstance(funct[p], tuple):
                r = funct[p][sp]()
                if posit[p][sp][4]:
                    if r: continue
                    break
            else:
                r = funct[p]()
                if posit[p][4]:
                    if r: continue
                    break
        stdscr.attron(curses.color_pair(1))
        if isinstance(posit[p][0], tuple):
            if posit[p][sp][0] == posit[p][sp][2]:
                stdscr.attroff(curses.color_pair(1))
                stdscr.addch(posit[p][sp][0],posit[p][sp][1], '<')
                stdscr.attron(curses.color_pair(1))
            else:
                rectangle(stdscr, posit[p][sp][0], posit[p][sp][1], posit[p][sp][2], posit[p][sp][3])
        else:
            if posit[p][0] == posit[p][2]:
                stdscr.attroff(curses.color_pair(1))
                stdscr.addch(posit[p][0],posit[p][1], '<')
                stdscr.attron(curses.color_pair(1))
            else:
                rectangle(stdscr, posit[p][0], posit[p][1], posit[p][2], posit[p][3])
        stdscr.attroff(curses.color_pair(1))

def hboxsel(stdscr, posit, funct):
    """
    posit = (
             (1,1,30,20),
             ((1,21,12,80), (13,21,24,80), (25,21,30,80)),
             (1,81,30,101)
            )
    funct = (
            lambda:menu(stdscr,2,2,d1),
             (
                 lambda: menu(stdscr,2,22,d2),
                 lambda: menu(stdscr,14,22,d2),
                 lambda: menu(stdscr,26,22,d3),
             ),
             lambda: menu(stdscr,2,82,d1)
            )
    """
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_GREEN)
    p = 0
    sp = 0

    stdscr.attron(curses.color_pair(1))
    if isinstance(posit[0][0], tuple):
        if posit[0][0][0] == posit[0][0][2]:
            fillspace(stdscr,posit[0][0][0],posit[0][0][1],25)
        else:
            rectangle(stdscr,posit[0][0][0],posit[0][0][1],posit[0][0][2],posit[0][0][3])
    else:
        if posit[0][0] == posit[0][2]:
            fillspace(stdscr,posit[0][0],posit[0][1],25)
        else:
            rectangle(stdscr,posit[0][0],posit[0][1],posit[0][2],posit[0][3])
    stdscr.attroff(curses.color_pair(1))
    while True:
        k = stdscr.getch()
        if isinstance(posit[p][0], tuple):
            if posit[p][sp][0] == posit[p][sp][2]:
                fillspace(stdscr,posit[p][sp][0],posit[p][sp][1],25)
            else:
                rectangle(stdscr, posit[p][sp][0], posit[p][sp][1], posit[p][sp][2], posit[p][sp][3])
        else:
            if posit[p][0] == posit[p][2]:
                fillspace(stdscr,posit[p][0],posit[p][1],25)
            else:
                rectangle(stdscr,posit[p][0], posit[p][1], posit[p][2], posit[p][3])
        if k == curses.KEY_UP:
            if isinstance(posit[p][0], tuple):
                if sp:
                    sp -= 1
        if k == curses.KEY_DOWN:
            if isinstance(posit[p][0], tuple):
                if sp != len(posit[p])-1:
                    sp += 1
        if k == curses.KEY_RIGHT:
            if p != len(posit)-1:
                p += 1
        if k == curses.KEY_LEFT:
            if p:
                p -= 1
        if k == 10:
            if isinstance(funct[p], tuple):
                funct[p][sp]()
            else:
                funct[p]()
        stdscr.attron(curses.color_pair(1))
        if isinstance(posit[p][0], tuple):
            if posit[p][sp][0] == posit[p][sp][2]:
                fillspace(stdscr,posit[p][sp][0],posit[p][sp][1],25)
            else:
                rectangle(stdscr, posit[p][sp][0], posit[p][sp][1], posit[p][sp][2], posit[p][sp][3])
        else:
            if posit[p][0] == posit[p][2]:
                fillspace(stdscr,posit[p][0],posit[p][1],25)
            else:
                rectangle(stdscr, posit[p][0], posit[p][1], posit[p][2], posit[p][3])
        stdscr.attroff(curses.color_pair(1))

if __name__=='__main__':
    def main(stdscr):
        hboxsel(stdscr)

    curses.wrapper(main)
