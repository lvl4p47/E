from tkinter import *
from random import randrange
import random

def step():
    global m, Lb, Rb, Tb, Bb, grav
    for i in range(N):
        part[i][0] += part[i][2]
        part[i][1] += part[i][3]
        if part[i][0] - R < Lb:
            part[i][2] = abs(part[i][2])
        if part[i][0] + R > Rb:
            part[i][2] = -abs(part[i][2])
        #part[i][2] += 0.05 * m * m #- part[i][0]/1000
        if part[i][1] - R < Tb:
            part[i][3] = abs(part[i][3])
        if part[i][1] + R > Bb:
            part[i][3] = -abs(part[i][3])
        if grav == 1:
            part[i][3] += 0.04 * m * m

def draw():
    global m1, m2, N, R
    m1 = (max ** 2) * 2 / 9
    m2 = m1 * 4
    c.delete("particle")
    for i in range(N):
        if part[i][2]**2 + part[i][3]**2 > m2:
            c.create_oval(part[i][0] - R, part[i][1] - R, part[i][0] + R, part[i][1] + R, fill='red', tag="particle")
        elif part[i][2]**2 + part[i][3]**2 > m1:
            c.create_oval(part[i][0] - R, part[i][1] - R, part[i][0] + R, part[i][1] + R, fill='purple', tag="particle")
        else:
            c.create_oval(part[i][0] - R, part[i][1] - R, part[i][0] + R, part[i][1] + R, fill='blue', tag="particle")
        #print(m1)
        #print(m2)

def sort():
    for i in range(N):
        for j in range(3):
            if j == 2:
                partsort[i][j] = part[i][4]
            else:
                partsort[i][j] = part[i][j]
    for i in range(1, N):
        for j in range(i, 0, -1):
            if partsort[j][0] < partsort[j - 1][0]:
                for k in range(3):
                    temp = partsort[j - 1][k]
                    partsort[j - 1][k] = partsort[j][k]
                    partsort[j][k] = temp
            else:
                break

def collision():
    for i in range(N - 1):
        for l in range(i + 1, N):
            if abs(partsort[i][0] - partsort[l][0]) <= 2 * R:
                if (partsort[i][0] - partsort[l][0]) ** 2 + (partsort[i][1] - partsort[l][1]) ** 2 <= 4 * R * R:
                    if part[partsort[l][2]][0] - part[partsort[i][2]][0] != 0:
                        k = (part[partsort[l][2]][1] - part[partsort[i][2]][1]) / (
                                    part[partsort[l][2]][0] - part[partsort[i][2]][0])
                        v11 = (part[partsort[i][2]][2] + k * part[partsort[i][2]][3]) / (1 + k ** 2)
                        v12 = (part[partsort[i][2]][3] - k * part[partsort[i][2]][2]) / (1 + k ** 2)
                        v21 = (part[partsort[l][2]][2] + k * part[partsort[l][2]][3]) / (1 + k ** 2)
                        v22 = (part[partsort[l][2]][3] - k * part[partsort[l][2]][2]) / (1 + k ** 2)
                        part[partsort[i][2]][2] = v21 - k * v12
                        part[partsort[i][2]][3] = v12 + k * v21
                        part[partsort[l][2]][2] = v11 - k * v22
                        part[partsort[l][2]][3] = v22 + k * v11
                    else:
                        v11 = part[partsort[i][2]][3]
                        v12 = -part[partsort[i][2]][2]
                        v21 = part[partsort[l][2]][3]
                        v22 = part[partsort[l][2]][2]
                        part[partsort[i][2]][2] = v21
                        part[partsort[i][2]][3] = v12
                        part[partsort[l][2]][2] = v11
                        part[partsort[l][2]][3] = v22
                    d = ((partsort[i][0] - partsort[l][0]) ** 2 + (partsort[i][1] - partsort[l][1]) ** 2) ** 0.5
                    dx = (2 * R - d) * (partsort[i][0] - partsort[l][0]) / d
                    dy = (2 * R - d) * (partsort[i][1] - partsort[l][1]) / d
                    part[partsort[i][2]][0] += dx
                    part[partsort[i][2]][1] += dy
                    part[partsort[l][2]][0] -= dx
                    part[partsort[l][2]][1] -= dy

def motion():
    global m
    if m == 1 or m == 0.5 or m == 2:
        draw()
        step()
        sort()
        collision()
        print(m)
        window.after(10, motion)

def pause_resume(event):
    global m, max
    if m == 0:
        m = 1
        spbut['text'] = 'Pause'
        motion()
    elif m == 0.5:
        for i in range(N):
            for j in range(2, 4):
                part[i][j] = part[i][j] * 2
        max = max * 2
        spbut['text'] = 'Resume'
        m = 0

    elif m == 2:
        for i in range(N):
            for j in range(2, 4):
                part[i][j] = part[i][j] / 2
        max = max / 2
        spbut['text'] = 'Resume'
        m = 0
    elif m == 1:
        spbut['text'] = 'Resume'
        m = 0

def spdx2(event):
    global m, max
    if m != 0:
        if m == 1:
            for i in range(N):
                for j in range(2, 4):
                    part[i][j] = part[i][j] * 2
            max = max * 2
        if m == 0.5:
            for i in range(N):
                for j in range(2, 4):
                    part[i][j] = part[i][j] * 4
            max = max * 4
        m = 2
    print(max)

def spdx1(event):
    global m, max
    if m != 0:
        if m == 2:
            for i in range(N):
                for j in range(2, 4):
                    part[i][j] = part[i][j] / 2
            max = max / 2
        if m == 0.5:
            for i in range(N):
                for j in range(2, 4):
                    part[i][j] = part[i][j] * 2
            max = max * 2
        m = 1
    print(max)

def spdx05(event):
    global m, max
    if m != 0:
        if m == 1:
            for i in range(N):
                for j in range(2, 4):
                    part[i][j] = part[i][j] / 2
            max = max / 2
        if m == 2:
            for i in range(N):
                for j in range(2, 4):
                    part[i][j] = part[i][j] / 4
            max = max / 4
        m = 0.5
    print(max)

def reset():
    global frame1, frame2, frame21, m, xent, yent, nent, rent, gch
    m = 0
    frame1.grid_forget()
    frame21.grid_forget()
    frame2.grid()
    frame21 = Frame(frame2)
    window.title("Параметры системы")
    xent = StringVar()
    yent = StringVar()
    nent = StringVar()
    rent = StringVar()
    gch = IntVar()

    xlab = Label(frame21, text="Размеры сосуда:    Ширина:")
    xlab.grid(row=0, column=0, sticky=W, padx=10, pady=20)
    xentry = Entry(frame21, textvariable=xent)
    xentry.grid(row=0, column=1)

    ylab = Label(frame21, text="Высота:")
    ylab.grid(row=0, column=2, sticky=W, padx=10, pady=20)
    yentry = Entry(frame21, textvariable=yent)
    yentry.grid(row=0, column=3)

    nlab = Label(frame21, text="Количество частиц:")
    nlab.grid(row=1, column=0, sticky=W, padx=10, pady=20)
    nentry = Entry(frame21, textvariable=nent)
    nentry.grid(row=1, column=1)

    rlab = Label(frame21, text="Радиус частиц:")
    rlab.grid(row=1, column=2, sticky=W, padx=10, pady=20)
    rentry = Entry(frame21, textvariable=rent)
    rentry.grid(row=1, column=3)

    gcheck = Checkbutton(frame21, text="Учитывать силу тяжести", variable=gch, onvalue=1, offvalue=0,)
    gcheck.grid(row=2, column=0)

    stbut = Button(frame21, text="Запустить")
    stbut.grid(row=3, column=3, sticky=NSEW)
    stbut.bind('<Button-1>', start)

    frame21.grid()

def start(en):
    global part, partsort, frame1, frame2, c, Lb, Rb, Tb, Bb, N, R, max, grav, m, xent, yent, nent, rent, gch
    if int(yent.get()) > window.winfo_screenheight() - 180:
        Bb = window.winfo_screenheight() - 170
    else:
        Bb = 10 + int(yent.get())
    if int(xent.get()) > window.winfo_screenwidth() - 30:
        Rb = window.winfo_screenwidth() - 20
    else:
        Rb = 10 + int(xent.get())
    if Rb < Bb:
        max = Rb/400 * 4
    else:
        max = Bb/400 * 4
    print(max)
    N = int(nent.get())
    R = int(rent.get())
    grav = gch.get()
    part = [[0 for j in range(5)] for i in range(N)]
    partsort = [[0 for j in range(3)] for i in range(N)]
    for i in range(N):
        for j in range(5):
            if j == 0:
                part[i][j] = R + Lb + randrange(Rb - R - 20)
            elif j == 1:
                part[i][j] = R + Tb + randrange(Bb - R - 20)
            elif j == 4:
                part[i][j] = i
            else:
                part[i][j] = random.uniform(-max, max)
    frame2.grid_forget()
    frame1.grid()
    window.title("Моделирование газа")
    c.grid_remove()
    c = Canvas(frame1, width=(Rb - Lb) + 20, height=(Bb - Tb) + 20, bg='black')
    c.grid(row=0, column=0)
    c.create_rectangle(Lb, Tb, Rb, Bb,
                       fill='black',
                       outline='white',
                       width=2)
    m = 1
    spbut['text'] = 'Pause'
    motion()


N = 10
R = 10
Lb = 10
Rb = 400
Tb = 10
Bb = 400
grav = 1
m = 1
max = 4
max0 = max
m1 = (max**2)*2/9
m2 = m1 * 4
part = [[0 for j in range(5)] for i in range(N)]
partsort = [[0 for j in range(3)] for i in range(N)]

for i in range(N):
    for j in range(5):
        '''if i == 0:
            part[i][2] = random.uniform(-max, max)
            part[i][3] = random.uniform(-max, max)'''
        if j == 0:
            part[i][j] = R + Lb + randrange(Rb - R - 20)
        elif j == 1:
            part[i][j] = R + Tb + randrange(Bb - R - 20)
        elif j == 4:
            part[i][j] = i
        else:
            part[i][j] = random.uniform(-max, max)
window = Tk()
window.title("Моделирование газа")
#window.geometry('900x900')

frame1 = Frame(window)
frame2 = Frame(window, height=100, width= 300)
frame21 = Frame(frame2)
xentry = Entry(frame21)
yentry = Entry(frame21)

menu = Menu(window)
window.config(menu=menu)

filemenu = Menu(menu, tearoff=0)
filemenu.add_command(label="Перезапустить", command=reset)
filemenu.add_separator()
filemenu.add_command(label="Выход", command=window.quit)

helpmenu = Menu(menu, tearoff=0)
helpmenu.add_command(label="Помощь")
helpmenu.add_command(label="О программе")

menu.add_cascade(label="Файл",
                     menu=filemenu)
menu.add_cascade(label="Справка",
                     menu=helpmenu)

c = Canvas(frame1, width=(Rb - Lb) + 20, height=(Bb - Tb) + 20, bg='black')
c.grid(row=0, column=0)
c.create_rectangle(Lb, Tb, Rb, Bb,
                   fill='black',
                   outline='white',
                   width=2,)
speed_frame = LabelFrame(frame1, text="Скорость")

spbut = Button(speed_frame, width=7, height=1, text="Pause")
spbut.grid(row=0, column=0)
spbut.bind('<Button-1>', pause_resume)

speedx05 = Button(speed_frame, width=4, height=1, text="X 0.5")
speedx05.grid(row=0, column=1)
speedx05.bind('<Button-1>', spdx05)

speedx1 = Button(speed_frame, width=4, height=1, text="X 1")
speedx1.grid(row=0, column=2)
speedx1.bind('<Button-1>', spdx1)

speedx2 = Button(speed_frame, width=4, height=1, text="X 2")
speedx2.grid(row=0, column=3)
speedx2.bind('<Button-1>', spdx2)



speed_frame.grid(row=1, column=0, sticky=W, padx=10)
frame1.grid()
window.after(500, motion())
window.mainloop()
