import curses
from curses.textpad import rectangle

'''
    (0, y_1, x_1, y_2, x_2, return_action)
    (1, y, x, size, return_action)
    (2, y, x, size, return_action)
    (3, y, x, size, return_action)
    0: Rectángulo verde
    1: Fondo blanco
    2: Campo
    3: Línea verde
(posit
    0:(0:(izar),1:(dchar)),
    1:(0:(izab),1:(dchab))
)
'''

def boxsel(stdscr, posit, funct):
    curses.curs_set(0)
    curses.noecho()
    curses.start_color()
    curses.init_pair(1, 0, curses.COLOR_GREEN)
    curses.init_pair(2, curses.COLOR_GREEN, -1)
    curses.init_pair(15,-1,15)
    p = 0
    sp = 0

    for a in range(len(posit)):
        for b in range(len(posit[a])):
            if posit[a][b][0] == 0:
                rectangle(stdscr, posit[a][b][1], posit[a][b][2], posit[a][b][3], posit[a][b][4])
            if posit[a][b][0] == 1:
                stdscr.addstr(posit[a][b][1], posit[a][b][2], " "*posit[a][b][3], curses.color_pair(0))
            if posit[a][b][0] == 2:
                stdscr.addch(posit[a][b][1], posit[a][b][2]+posit[a][b][3], ' ')
            if posit[a][b][0] == 3:
                for i in range(posit[a][b][3]):
                    stdscr.addch(posit[a][b][1], posit[a][b][2]+i, curses.ACS_HLINE)
    if posit[p][sp][0] == 0:
        stdscr.attron(curses.color_pair(2))
        rectangle(stdscr, posit[p][sp][1], posit[p][sp][2], posit[p][sp][3], posit[p][sp][4])
        stdscr.attroff(curses.color_pair(2))
    if posit[p][sp][0] == 1:
        stdscr.addstr(posit[p][sp][1], posit[p][sp][2], " "*posit[p][sp][3], curses.color_pair(15))
    if posit[p][sp][0] == 2:
        stdscr.addch(posit[p][sp][1], posit[p][sp][2]+posit[p][sp][3], '<')
    if posit[p][sp][0] == 3:
        for i in range(posit[p][sp][3]):
            stdscr.attron(curses.color_pair(1))
            stdscr.addch(posit[p][sp][1], posit[p][sp][2]+i, 'x')
            stdscr.attroff(curses.color_pair(1))

    while True:
        curses.curs_set(0)
        curses.noecho()
        k = stdscr.getch()
        if k == curses.KEY_LEFT:
            if sp:
                sp -= 1
        if k == curses.KEY_RIGHT:
            if sp != len(posit[p])-1:
                sp += 1
        if k == curses.KEY_DOWN:
            if p != len(posit)-1:
                p += 1
                if sp > len(posit[p])-1:
                    sp = len(posit[p])-1
        if k == curses.KEY_UP:
            if p:
                p -= 1
                if sp > len(posit[p])-1:
                    sp = len(posit[p])-1
        if k == 10:
            r = funct[p][sp]()
            if posit[p][sp][0] == 0:
                if posit[p][sp][5]:
                    if r: continue
                    break
                else: break
            else:
                if posit[p][sp][4]:
                    if r: continue
                    break
                else: break
        for a in range(len(posit)):
            for b in range(len(posit[a])):
                if posit[a][b][0] == 0:
                    rectangle(stdscr, posit[a][b][1], posit[a][b][2], posit[a][b][3], posit[a][b][4])
                if posit[a][b][0] == 1:
                    stdscr.addstr(posit[a][b][1], posit[a][b][2], " "*posit[a][b][3], curses.color_pair(0))
                if posit[a][b][0] == 2:
                    stdscr.addch(posit[a][b][1], posit[a][b][2]+posit[a][b][3], ' ')
                if posit[a][b][0] == 3:
                    for i in range(posit[a][b][3]):
                        stdscr.addch(posit[a][b][1], posit[a][b][2]+i, curses.ACS_HLINE)

        if posit[p][sp][0] == 0:
            stdscr.attron(curses.color_pair(2))
            rectangle(stdscr, posit[p][sp][1], posit[p][sp][2], posit[p][sp][3], posit[p][sp][4])
            stdscr.attroff(curses.color_pair(2))
        if posit[p][sp][0] == 1:
            stdscr.addstr(posit[p][sp][1], posit[p][sp][2], " "*posit[p][sp][3], curses.color_pair(15))
        if posit[p][sp][0] == 2:
            stdscr.addch(posit[p][sp][1], posit[p][sp][2]+posit[p][sp][3], '<')
        if posit[p][sp][0] == 3:
            for i in range(posit[p][sp][3]):
                stdscr.attron(curses.color_pair(1))
                stdscr.addch(posit[p][sp][1], posit[p][sp][2]+i, 'x')
                stdscr.attroff(curses.color_pair(1))



if __name__=='__main__':
    def main(stdscr):
        curses.curs_set(0)
        curses.use_default_colors()
        y,x=stdscr.getmaxyx()
        rectangle(stdscr, 3,0,y-6,20)
        rectangle(stdscr,y-6,0,y-1,20)
        rectangle(stdscr,3,21,y-1,x-2)
        for i in range(x-24):
            stdscr.addch(y-3, 22+i, curses.ACS_HLINE)
        fn = (
                (exit,exit),
                (exit,exit)
            )
        pos = (
                ((3,3,10,1, 0),(3,3,(21+(x-2))//2,1, 0)),
                ((3,y-6,10,1, 0),(3,y-3,(22+(x-2))//2,1, 0))
            )
#        pos = (
#                ((0, 3,0,y-6,20),(0, 3,21,y-6,x-2)),
#                ((0, y-6,0,y-1,20),(1,y-5,22, 50)),
#            )
        boxsel(stdscr,pos,fn)

    curses.wrapper(main)
