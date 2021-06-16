 
from tkinter import Frame, Tk, Toplevel, ttk
import tkinter
from tkinter.constants import CENTER, FALSE, TOP, TRUE
from tkinter.messagebox import showinfo
from tkinter import filedialog as fd
from PIL import ImageTk, Image
import os
import time
from index import Indexer
from search import Retriever
import sqlite3
from sqlite3 import Error
from person import Person



class Conan:
    def __init__(self):
        self.person1=Person()
        self.person2=Person()

        self.app = tkinter.Tk()
        self.app.geometry("800x500")
        self.app.resizable(height=0,width=0)
        self.app.configure(background="grey")
        self.app.title("Conan")
        self.ImageResultPaths=None
        
        self.conan()

     
        
        self.app.mainloop()


############################################################
#                                                          #         
#                     conan GUI                            #     
#                                                          #
# ##########################################################  
    def cover(self):

        t1 = tkinter. Label(self.app,text="Conan",fg = "orange",bg="grey",
              font=("Arial", 50),
              )
        t1.place(x=270,y=200)      
        
        t2= tkinter. Label(self.app,text="a way to find missing people",fg = "orange",bg="grey",
              font=("Arial", 15),
              )
        t2.place(x=400,y=280)

        self.app.after(1000, t1.destroy)
        self.app.after(1000, t2.destroy)
     


    def conan(self):


        self.cover()
        
            

      

        tkinter.Button(self.app,text="search",command=self.search).place(x=220,y=300)
        tkinter.Button(self.app,text="browse",command=self.image_search).place(x=150,y=300)
      

        tkinter.Label(self.app,text="Name").place(x=550,y=300)
        tkinter.Label(self.app,text="tel").place(x=550,y=335)
        tkinter.Label(self.app,text="Addr.").place(x=550,y=370)
        tkinter.Label(self.app,text="descr.").place(x=550,y=405)

        self.name = tkinter.StringVar()
        self.tel = tkinter.StringVar()
        self.addr = tkinter.StringVar()
        self.des = tkinter.StringVar()
        tkinter.Label(self.app,textvariable=self.name).place(x=600,y=300)
        tkinter.Label(self.app,textvariable=self.tel ).place(x=600,y=335)
        tkinter.Label(self.app,textvariable=self.addr).place(x=600,y=370)
        tkinter.Label(self.app,textvariable=self.des).place(x=600,y=405)



        tkinter.Button(self.app,text="Insert",command=self.insert_gui).place(x=700,y=450)


############################################################
#                                                          #         
#                     Search GUI                           #     
#                                                          #
# ##########################################################  
    def insert_gui(self):

        self.search = Toplevel(self.app)
        self.search.geometry("300x500")
        self.search.title("conan search")
        self.search.resizable(height=0,width=0)
        tkinter.Button(self.search,text="Browse",command=self.show_image).place(x=125,y=255)
        self.entry_data()


    def find_image(self):
        filename = fd.askopenfilename(title ='"pen')
        return filename

    def show_image(self):
        self.person1 = self.find_image()
        os.system("cp {}  /dataset".format(self.person1))
        img = Image.open(self.person1)
        img = img.resize((500, 250), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        panel =tkinter.Label(self.search, image = img)
        panel.image = img
        panel.grid(row = 2)




    def entry_data(self):

        tkinter.Label(self.search,text="Name").place(x=10,y=300)
        self.name_entry = tkinter.Entry(self.search)
        self.name_entry.place(x=80,y=300)

        tkinter.Label(self.search,text="Age").place(x=10,y=335)
        self.tel_entry = tkinter.Entry(self.search)
        self.tel_entry.place(x=80,y=335)
 
        tkinter.Label(self.search,text="Addr.").place(x=10,y=370)
        self.add_entry = tkinter.Entry(self.search)
        self.add_entry.place(x=80,y=370)

        tkinter.Label(self.search,text="descr.").place(x=10,y=405)
        self.des_entry = tkinter.Entry(self.search)
        self.des_entry.place(x=80,y=405)

        tkinter.Button(self.search,text="Insert",command=self.insert).place(x=90,y=450)

        tkinter.Button(self.search,text="updateDB",command=self.updateDB).place(x=160,y=450)
    

    def image_search(self):
        self.person2 = self.find_image()
        img = Image.open(self.person2)
        img = img.resize((250, 250), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        panel =tkinter.Label(self.app, image = img)
        panel.image = img
        panel.place(x=100,y=0)
    

    def updateDB(self):
        # update index.csv file
        self.infomessage("Please wait this may take a while", "UpdatingDatabase")
        index = Indexer()
        index.IndexHog()
      
        self.infomessage("Database  has been  Updated", "Database Status")


    def infomessage(str, info, event=None):
        showinfo(info, str)
    def errormessage(str, event=None):
        showinfo.showerror("Error", str)

    def insert(self):
        id=self.person1
        id="dataset/"+id.split("/")[-1]
        name=self.name_entry.get()
        tel=self.tel_entry.get()
        addr=self.add_entry.get()
        dis=self.des_entry.get()
        db = sqlite3.connect('pe.db')
        cursor=db.cursor()
        sql="INSERT INTO `people`('ID',`NAME`, `TEL`, `ADDR`,'DIS') VALUES ('%s','%s','%s','%s','%s')"%(id,name,tel,addr,dis)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
            
        db.close()
        self.infomessage("insert done")


    





    def search(self):
        Result = Retriever(self.person2)
        Result.HogSearch()

        self.ImageResultPaths = Result.GetImageList()[0]
        
        img = Image.open(self.ImageResultPaths)
        img = img.resize((250, 250), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        panel =tkinter.Label(self.app, image = img)
        panel.image = img
        panel.place(x=500,y=0)

        id=self.ImageResultPaths
        print(id)
        db = sqlite3.connect('pe.db')
        cursor=db.cursor()

        sql="SELECT * FROM `people` WHERE id ='%s' " %(id)

        try:
            cursor.execute(sql)
            result=cursor.fetchall()
            for row in result:
                print(row)
                self.name.set(row[1])
                self.tel.set(row[2])
                self.addr.set(row[3])
                self.des.set(row[4])

        except:
            print("unable to fetch data")
            
        db.close()

Conan()





