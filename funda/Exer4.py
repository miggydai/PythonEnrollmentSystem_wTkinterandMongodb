import pymongo
import tkinter as tk
from tkinter import messagebox

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["enrollmentsystem"]
mycol = mydb["students"]
lst = [['ID' , 'Name', 'Email' , 'Course']]

#assign to table
def callback(event):  
    li=[]
    li=event.widget._values
    sid.set(lst[li[1]][0])
    sname.set(lst[li[1]][1])
    semail.set(lst[li[1]][2])
    scourse.set(lst[li[1]][3])

#create table
def creategrid(n):
    lst.clear()
    lst.append(['ID' , 'Name', 'Email' , 'Course'])
    cursor = mycol.find({}) 
    for text_fromDB in cursor:
        studid = str(text_fromDB['sid'])
        studname = str(text_fromDB['sname'].encode('utf-8').decode('utf-8'))
        studemail = str(text_fromDB['semail'].encode('utf-8').decode('utf-8'))
        studcourse = str(text_fromDB['scourse'].encode('utf-8').decode('utf-8'))
        lst.append([studid,studname,studemail,studcourse])
    
    for i in range(len(lst)):
       
        for j in range(len(lst[0])):
            mgrid = tk.Entry(window,width=10)
            mgrid.insert(tk.END,lst[i][j])
            mgrid._values = mgrid.get(), i
            mgrid.grid(row=i+7, column=j+6)
            mgrid.bind("<Button-1>", callback)
    if n == 1:
        for label in window.grid_slaves():
            if int(label.grid_info()["row"]) > 6:
                label.grid_forget()

#messagebox
def msgbox(msg,titlebar):
    result=messagebox.askokcancel(title=titlebar,message=msg)
    return result

#save
def save():   
    r=msgbox("Save record?","Record")
    if r == True:
        newid = mycol.count_documents({})
        if newid!=0:
            newid=mycol.find_one(sort=[("sid", -1)])["sid"] 
            id=newid+1 
            sid.set(int(id))
            mydict = {"sid":int(studid.get()), "sname":studname.get(), "semail":studemail.get(), "scourse":studcourse.get()}
            x = mycol.insert_one(mydict)
            creategrid(1)
            creategrid(0)


#delete
def delete():
    r=msgbox("Delete?","record")
    if r == True:
        myquery = {"sid":int(studid.get())}
        mycol.delete_one(myquery)
        creategrid(1)
        creategrid(0)



#update
def update():
     r=msgbox("Update?","record")
     if r == True:
        myquery = {"sid": int(studid.get())}
        newvalues = {"$set":{"sname": studname.get()}}
        mycol.update_one(myquery,newvalues)

        newvalues = {"$set":{"semail": studemail.get()}}
        mycol.update_one(myquery,newvalues)

        newvalues = {"$set":{"scourse": studcourse.get()}}
        mycol.update_one(myquery,newvalues)

        creategrid(1)
        creategrid(0)

#call subjectsform
def subjectsform():
    import SubjectsForm


#call teachersform
def teachersform():
    import TeachersForm



window = tk.Tk()
window.title("Students Form")
window.geometry("1050x400")
window.configure(bg="blue")

#Menu bar
menubar = tk.Menu(window)
filemenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="Subjects", command=subjectsform)
filemenu.add_command(label="Teachers", command=teachersform)
filemenu.add_separator()
filemenu.add_command(label="Close", command=window.quit)

editmenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Edit", menu=editmenu)
editmenu.add_command(label="Undo")

editmenu.add_separator()
editmenu.add_command(label="Cut")

window.config(menu=menubar)

#title hehe
label = tk.Label(window, text = "Students Enlistment Form", width = 30 , height = 1, bg = "pink" , anchor="center")
label.config(font=("Courier",10))
label.grid(column=2,row=1)

#Student id
label = tk.Label(window, text = "Student ID", width = 15 , height = 1, bg = "pink")
label.grid(column=1,row=2)

sid=tk.StringVar()
studid = tk.Entry(window , textvariable=sid) 
studid.grid(column=2,row=2)
studid.configure(state=tk.DISABLED)

#Student name
label2 = tk.Label(window, text = "Student Name", width = 15 , height = 1, bg = "pink")
label2.grid(column=1,row=3)

sname=tk.StringVar()
studname = tk.Entry(window , textvariable=sname) 
studname.grid(column=2,row=3)

#Student email
label3 = tk.Label(window, text = "Student Email", width = 15 , height = 1, bg = "pink")
label3.grid(column=1,row=4)

semail=tk.StringVar()
studemail = tk.Entry(window , textvariable=semail) 
studemail.grid(column=2,row=4)

#Student course
label4 = tk.Label(window, text = "Student Course", width = 15 , height = 1, bg = "pink")
label4.grid(column=1,row=5)

scourse=tk.StringVar()
studcourse = tk.Entry(window , textvariable=scourse) 
studcourse.grid(column=2,row=5)

#create table
creategrid(0)
#Buttons
savebtn = tk.Button(window,text = "Save", command=save)
savebtn.grid(column=1, row=6)
delbtn = tk.Button(window,text = "Delete", command=delete)
delbtn.grid(column=2, row=6)
upbtn = tk.Button(window,text = "Update", command=update)
upbtn.grid(column=3, row=6)

window.mainloop()