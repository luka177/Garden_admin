import tkinter as tk
from tkinter import *
import numpy as np
from numpy import zeros
import os
import re
from tkinter import filedialog
import shutil
import zipfile
inmaindir=True
xcell=25
donerec=0
ycell=25
x = 0
created=0
y = 0
def callbackc(event):
    xx = canvas.canvasx(event.x)
    yy = canvas.canvasy(event.y)
    yr = int(yy/ycell)
    xr = int(xx/xcell)
    if(yr<y and xr<x):
        diag = tk.Toplevel(main)
        Label(diag, text="Name").grid(row=0)
        Label(diag, text="index_of_image").grid(row=1)
        name1 = Entry(diag)
        name1.grid(row =0, column = 1)
        L = tk.Listbox(diag)
        gifsdict = {}
        i =0
        while(i<imnum-1):
            L.insert(tk.END, images[i])
            i+=1
        L.grid(row =1, column = 1)
        name1.insert(0,str(mass1[xr][yr]))
        img = tk.Label(diag)
        img.grid(row=2, column=2)
        def list_entry_clicked(*ignore):
            global imgname
            imgname = L.get(L.curselection()[0])
            imgname = re.findall(r'\d+', imgname)
            imgname=int(imgname[0])
            img.config(image=images[imgname])
        def okd():
            global imgname
            mass1[xr][yr]=name1.get()
            mmas[xr][yr]=imgname
            canvas.itemconfig(mass2[xr][yr], image = images[imgname])
            diag.destroy()
        ok = Button(diag, text="OK", command=okd).grid(row= 2, column = 1)
        L.bind('<ButtonRelease-1>', list_entry_clicked)
def callbackm(event):
    xx = canvas.canvasx(event.x)
    yy = canvas.canvasy(event.y)
    yr = int(yy/ycell)
    xr = int(xx/xcell)
    global lastx
    global lasty
    global created
    global rec
    if(yr<y and xr<x):
        res = int(y/ycell)-int(1200-(x/xcell))
       # draw_grid()
        v.set(mass1[xr][yr])
        if(created==0):
            rec=canvas.create_rectangle(xr*xcell, yr*ycell, xr*xcell+xcell, yr*ycell+ycell, outline='red', width=3)
            lastx=xr
            lasty=yr
            created=1
        else:
            canvas.delete(rec)
            rec=canvas.create_rectangle(xr*xcell, yr*ycell, xr*xcell+xcell, yr*ycell+ycell, outline='red', width=3)
def new():
    global inmaindir
    if (inmaindir!=True):
        os.chdir("..")
        inmaindir=True
    if(os.path.isdir("work")):
        shutil.rmtree('work')
    os.mkdir("work")
    os.chdir("work")
    inmaindir=False
    diag = tk.Toplevel(main)
    Label(diag, text="Rows").grid(row=0)
    Label(diag, text="Columes").grid(row=1)
    e1 = Entry(diag)
    e2 = Entry(diag)
    def okd():
        global x
        global y
        x =int(e1.get())
        y = int(e2.get())
        if(x>5000):
            e1.delete(0,END)
            e1.insert(0,"5000")
            if(y>5000):
                e2.delete(0,END)
                e2.insert(0,"5000")
            return
        if(y>5000):
            e2.delete(0,END)
            e2.insert(0,"5000")
            return
        global mmas
        global mass1
        global mass2
        mmas = zeros((int(e1.get()),int(e2.get())),dtype ='int')
        mass1 = zeros((int(e1.get()),int(e2.get())),dtype ='object')
        mass2 = zeros((int(e1.get()),int(e2.get())),dtype ='object')
        xfile= open("x","w+")
        yfile=open("y","w+")
        xfile.write(e1.get())
        yfile.write(e2.get())
        xfile.close()
        yfile.close()
        diag.destroy()
        draw_grid()
    ok = Button(diag, text="OK", command=okd).grid(row= 3, column = 3)
    e1.grid(row=0, column=1)
    e2.grid(row=1, column=1)
def file_save():
    canvas.postscript(file='/home/luka/father/test.ps', colormode='color')
main =Tk()
canvas = tk.Canvas(main, width=1000, height=700)
canvas.grid(row=0, column=0)
v = StringVar()
v.set("hi")
Label(main, textvariable=v).grid(row=2, column=0)
v.set("hi")
canvas.bind("<Motion>", callbackm)
canvas.bind('<Button>', callbackc)
scroll_x = tk.Scrollbar(main, orient="horizontal", command=canvas.xview)
scroll_x.grid(row=1, column=0, sticky="ew")
scroll_y = tk.Scrollbar(main, orient="vertical", command=canvas.yview)
scroll_y.grid(row=0, column=1, sticky="ns")
canvas.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
main.attributes("-fullscreen", True)
menubar = Menu(main)
main.config(menu=menubar)
def draw_grid():
    canvas.delete("all")
    global images
    global x
    global y
    global scroll_x
    global scroll_y
    i=0
    canvas.create_line(0, 0, x*xcell, 0)
    while(i<x):
        i+=1
        canvas.create_line(i*xcell, 0, i*xcell, y*ycell)
    i=0
    canvas.create_line(0, 0, 0, y*ycell)
    while(i<y):
        i+=1
        canvas.create_line(0, i*ycell, x*xcell, i*ycell)
    i=0
    xy=0
    xx=0
    yy=0
    ylin=0
    canvas.configure(scrollregion=canvas.bbox("all"))
    while (i<x*y):
        mass2[xy][ylin]=canvas.create_image(xx+1, yy+1, image=images[mmas[xy][ylin]], anchor=NW)
        i+=1
        xx+=xcell
        xy+=1
        if(xy==x):
            xy=0
            ylin+=1
            xx=0
            yy+=ycell
def localsave():
    mmasfi=open("mmas",'wb')
    np.save(mmasfi, mmas)
    mmasfi.close()
    mass1fi=open("mass1",'wb')
    np.save(mass1fi, mass1)
    mass1fi.close()
    wi=open("w",'w+')
    wi.write(str(xcell))
    he=open("h",'w+')
    he.write(str(ycell))
    savename=filedialog.asksaveasfilename(defaultextension=".sad", filetypes=(("sad file", "*.sad"),("All Files", "*.*") ))
    print(savename)
    os.chdir("..")
    shutil.make_archive(savename, 'zip', "work")
    savename = savename[:-4]
    print(savename)
    shutil.move((savename+".sad.zip"), (savename+".sad"))
    os.chdir("work")
def load():
    global inmaindir
    global x
    global y
    global mmas
    global mass1
    global mass2
    if(inmaindir!=True):
        os.chdir("..")
        inmaindir=True
    shutil.rmtree("work")
    os.mkdir("work")
    file_path = filedialog.askopenfilename()
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall("work")
    os.chdir("work")
    inmaindir=False
    mmasfi=open("mmas",'rb')
    mmas=np.load(mmasfi)
    mmasfi.close()
    mass1fi=open("mmas",'rb')
    mass1=np.load(mass1fi)
    mass1fi.close()
    xfile= open("x","r")
    yfile=open("y","r")
  #  w= open("w","r")
  #  h=open("h","r")
    x=int(xfile.read())
    y=int(yfile.read())
  #  xcell=int(w.read())
  #  ycell=int(h.read())
    xfile.close()
    yfile.close()
    print(x,y)
    mass2 = zeros((x,y), dtype='object')
    draw_grid()
def csize():
    diag = tk.Toplevel(main)
    Label(diag, text="width").grid(row=0)
    Label(diag, text="heidth").grid(row=1)
    e1 = Entry(diag)
    e2 = Entry(diag)
    def okd():
        global xcell
        global ycell
        xcell =int(e1.get())
        ycell = int(e2.get())
        if(x>500):
            e1.delete(0,END)
            e1.insert(0,"500")
            if(y>500):
                e2.delete(0,END)
                e2.insert(0,"500")
            return
        if(y>500):
            e2.delete(0,END)
            e2.insert(0,"500")
            return
        diag.destroy()
        draw_grid()
    ok = Button(diag, text="OK", command=okd).grid(row= 3, column = 3)
    e1.grid(row=0, column=1)
    e2.grid(row=1, column=1)
imnum=4
images=[0]*imnum
i=0
while(i<imnum):
    images[i]=PhotoImage(file= str(i)+'.png')
    i+=1
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Set cell size", command=csize)
filemenu.add_command(label="New", command=new)
filemenu.add_command(label="Export as image", command=file_save)
#filemenu.add_command(label="Save", command=donothing)
filemenu.add_command(label="Save as...", command=localsave)
filemenu.add_command(label="load", command=load)
menubar.add_cascade(label="File", menu=filemenu)
menubar.add_command(label="Quit", command=main.quit)
main.mainloop()
