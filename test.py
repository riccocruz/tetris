from tkinter import *
from random import *

root=Tk()
canvas=Canvas(root,width=400,height=300,bg='white')
def draw(event=None):
    canvas.delete(ALL)# clear canvas first
    canvas.create_oval(randint(0,399),randint(0,299),15,15,fill='red')
canvas.pack()

root.bind("<space>", draw)
root.mainloop()