# --------------------------------------------Imports-------------------------------------------------------------------#
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as t
from tkinter import filedialog as fd
from PIL import ImageTk, Image
from index import Indexer
from search import Retriever

import os
from pathlib import Path
import cv2
from tkinter import ttk

root = Tk()
root.geometry('800x650')
root.title('CBIR')


# ------------------------------------Show Errors-----------------------------------------------------------------------#
def errormessage(str, event=None):
    t.showerror("Error", str)


def infomessage(str, info, event=None):
    t.showinfo(info, str)


imagePath = str()
imglist = list()


def showHelp():
    str1 = """ To search for an image
 1-press update db
 2-browse the required picture
 3-choose the required algorthim
 4-press reterieve
                   

           """
    infomessage(str1, "instructions")


    

     


    

     
    #infomessage("could not find video", "result", event=None)


def file_opener():
    # get image query and display it
    global imagePath
    global InputImg
    global img
    InputImg.create_image((0, 0), anchor=NW, image=img)
    InputImg.update()
    filename = fd.askopenfilename()
    imagePath = filename
    img = Image.open(filename)
    img = img.resize((400, 270), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    InputImg.create_image((0, 0), anchor=NW, image=img)
    InputImg.update()

RetrieveOption = str()  # default option is histogram

def ShowResults():
    #('HOG', 'SHAPE')
    global ResultImg
    global imglist
    global imagePath
    global RetrieveOption
    ResultImg.delete("all")
    Result = Retriever(imagePath)
    if RetrieveOption == "HOG":
        Result.HogSearch()

    ImageResultPaths = Result.GetImageList()
    imglist.clear()
    for i, imagepath in enumerate(ImageResultPaths):
        with Image.open(imagepath) as im:
            imp = im.copy()
            #                im = Image.open(imagePath)
            imp = imp.resize((150, 150), Image.ANTIALIAS)
            imglist.append((ImageTk.PhotoImage(imp), imagepath))

    for i, (image, imagepath) in enumerate(imglist):
        ResultImg.create_image((i % 5 * 160, int(i / 5) * 160), anchor=NW, image=image)
        print((i % 5 * 150 + 10, int(i / 5) * 150 + 5))
        ResultImg.update()
    print("finished")


def UpdateDB():
    # update index.csv file
    infomessage("Please wait this may take a while", "UpdatingDatabase")
    index = Indexer()

    index.IndexHog()

    infomessage("Database  has been  Updated", "Database Status")




def t1():
    global RetrieveOption
    RetrieveOption = n1.get()
    print(n1.get())

def t2():
    global RetrieveOption
    RetrieveOption = n2.get()
    print(n2.get())


def getorigin(eventorigin):
    global imglist
    global x, y
    x = eventorigin.x
    y = eventorigin.y
    imageIndex = int(x / 160) + (int(y / 160) * 5)
    print(imageIndex)
    print(x, y)
    t = cv2.imread(imglist[imageIndex][1])
    cv2.imshow("image", t)
    cv2.waitKey(4000)
    print(imglist[imageIndex])
    print(imglist)


# tab control
########################################################
tabControl = ttk.Notebook(root)
image_tab = ttk.Frame(tabControl)

tabControl.pack(expand=1, fill="both")
tabControl.add(image_tab, text='Image Search')


# menu
##########################################################
menu_bar = Menu(root)
file_menu = Menu(menu_bar, tearoff=0)
help_menu = Menu(menu_bar, tearoff=0)

help_menu.add_command(label='Instructions', command=showHelp)




file_menu.add_command(label='UpdateDB', accelerator='Alt+F4', command=UpdateDB)
file_menu.add_separator()
file_menu.add_command(label='Exit', accelerator='Alt+F4', command=exit)
menu_bar.add_cascade(label='File', menu=file_menu)
menu_bar.add_cascade(label='Help', menu=help_menu)

root.config(menu=menu_bar)

# image retreival tab
#################################################################

lf = LabelFrame(image_tab, text='Image Query', bg='MistyRose4', fg='white')
R1 = Radiobutton(lf, text="HOG", value=1, command=t1, bg='MistyRose4')
R1.grid(row=0, column=0)

n1 = StringVar()
method1 = ttk.Combobox(lf, width=20, textvariable=n1)
img = Image.open("loading.png").resize((300, 170), Image.ANTIALIAS)
img = ImageTk.PhotoImage(img, Image.ANTIALIAS)
method1['values'] = ('HOG')
method1.grid(row=0, column=1)
n2 = StringVar()



lf.pack(fill='both')
Button(lf, text='Browse', bd=3, relief=RAISED, width=20, command=file_opener).grid(row=2, column=0, columnspan=2)
Button(lf, text='Retrieve', bd=3, relief=RAISED, width=20, command=ShowResults).grid(row=3, column=0, columnspan=2)
inputframe = Frame(lf)

InputImg = Canvas(lf, bg='MistyRose3', relief=RAISED, bd=5)
OutputFrame = LabelFrame(image_tab, bd=2, text="Result", background='MistyRose', fg="gray14")
InputImg.grid(column=4, row=0, rowspan=4, padx=70)  # pack(expand='yes', fill='both')
ResultImg = Canvas(OutputFrame, takefocus=0, relief=SUNKEN, background='MistyRose4', bd=2)

inputframe.grid(row=0, column=4, rowspan=4)  # pack(expand='yes', fill='both')
ResultImg.pack(expand=True, fill='both')
OutputFrame.pack(expand='yes', fill='both')
ResultImg.bind("<Button 1>", getorigin)

# second reterval tab
##############################################################






root.mainloop()

