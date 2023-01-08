#!/usr/bin/env python3

from os.path import basename, splitext
import tkinter as tk
from tkinter import Scale, Frame, Label, LEFT, S, HORIZONTAL, Entry


# from tkinter import ttk


class Application(tk.Tk):
    name = "ColorMishMash"

    def __init__(self):
        super().__init__(className=self.name)

        self.fileName = 'colors.txt'

        self.title(self.name)

        self.bind("<Escape>", self.quit)

        self.lblHlavni = tk.Label(self, text="Color picker")
        self.lblHlavni.pack()

        self.varR = tk.IntVar()
        self.varR.trace('w', self.color_change)
        self.varB = tk.IntVar()
        self.varB.trace('w', self.color_change)
        self.varG = tk.IntVar()
        self.varG.trace('w', self.color_change)

        self.frameR = Frame(self)
        self.frameR.pack()
        self.frameG = Frame(self)
        self.frameG.pack()
        self.frameB = Frame(self)
        self.frameB.pack()

        self.lblR = Label(self.frameR, text="R")
        self.lblR.pack(side=LEFT, anchor=S)
        self.scaleR = tk.Scale(self.frameR, from_=0, to=0xff,
                               orient=HORIZONTAL, length=333, variable=self.varR)
        self.scaleR.pack(side=LEFT, anchor=S)
        self.entryR = Entry(self.frameR, textvariable=self.varR)
        self.entryR.pack(side=LEFT, anchor=S)
        self.entryR.bind("<Key>", self.update)

        self.lblB = Label(self.frameB, text="B")
        self.lblB.pack(side=LEFT, anchor=S)
        self.scaleB = tk.Scale(self.frameB, from_=0, to=0xff,
                               orient=HORIZONTAL, length=333, variable=self.varB)
        self.scaleB.pack(side=LEFT, anchor=S)
        self.entryB = Entry(self.frameB, textvariable=self.varB)
        self.entryB.pack(side=LEFT, anchor=S)
        self.entryB.bind("<Key>", self.update)

        self.lblG = Label(self.frameG, text="G")
        self.lblG.pack(side=LEFT, anchor=S)
        self.scaleG = tk.Scale(self.frameG, from_=0, to=0xff,
                               orient=HORIZONTAL, length=333, variable=self.varG)
        self.scaleG.pack(side=LEFT, anchor=S)
        self.entryG = Entry(self.frameG, textvariable=self.varG)
        self.entryG.pack(side=LEFT, anchor=S)
        self.entryG.bind("<Key>", self.update)

        self.canvasMain = tk.Canvas(self, bg="black")
        self.canvasMain.pack()
        self.canvasMain.bind("<Button-1>", self.clickHandler)

        self.frameMen = Frame(self)
        self.frameMen.pack()
        self.canvasMen = []

        loadColors = self.getSavedColors()
        for row in range(3):
            for column in range(7):
                canvas = tk.Canvas(self.frameMen, width=50,
                                   height=50, bg=loadColors[row][column])
                canvas.grid(row=row, column=column)
                canvas.bind(
                    "<Button-1>", self.clickHandler)
                self.canvasMen.append(canvas)

        self.btnQuit = tk.Button(
            self, text="Quit", command=self.quit, pady=10, padx=10)
        self.btnQuit.pack()

    def clickHandler(self, event):
        info = event.widget.grid_info()
        if self.cget("cursor") != "pencil":
            self.config(cursor="pencil")
            self.color = event.widget.cget("bg")
        else:
            self.config(cursor="")
            # if event.widget is self.canvasMain:
            #     self.canvasColor25lids()
            event.widget.config(bg=self.color)

            if (str(event.widget).__contains__(f".!frame4.!canvas")):
                colors = self.getSavedColors()
                colors[int(info['row'])][int(info['column'])] = self.color
                file = open(self.fileName, 'w')
                colors = '|'.join([' '.join(i) for i in colors])
                file.write(colors)
                file.close()

    def getSavedColors(self):
        file = open(self.fileName, 'r')
        colors = file.readline().split('|')
        colors = [i.split(' ') for i in colors]
        file.close()

        return colors

    def color_change(self, var=None, index=None, mode=None):
        print(var, index, mode)
        r = self.varR.get()
        b = self.varB.get()
        g = self.varG.get()

        colorstring = f"#{r:02X}{g:02X}{b:02X}"
        print(colorstring)
        self.canvasMain.config(bg=colorstring)

    def quit(self, event=None):
        super().quit()

    def update(self, event=None):
        print(event.keycode, event.keysym, event.x, event.y)


app = Application()
app.mainloop()
