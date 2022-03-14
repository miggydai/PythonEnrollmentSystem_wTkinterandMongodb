import pymongo
import tkinter as tk
from tkinter import messagebox
#variables & mongodb connect
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["enrollmentsystem"]
mycol = mydb["teachers"]
lst = [['ID' , 'Name', 'Dept' , 'Contact']]

#assign to table
def callback(event):  
    li=[]
    li=event.widget._values
    tid.set(lst[li[1]][0])
    tname.set(lst[li[1]][1])
    tdept.set(lst[li[1]][2])
    tnum.set(lst[li[1]][3])

#create table
def creategrid(n):
    lst.clear()
    lst.append(['ID' , 'Name', 'Dept' , 'Number'])
    cursor = mycol.find({}) 
    for text_fromDB in cursor:
        studid = str(text_fromDB['tid'])
        studname = str(text_fromDB['tname'].encode('utf-8').decode('utf-8'))
        studemail = str(text_fromDB['tdept'].encode('utf-8').decode('utf-8'))
        studcourse = str(text_fromDB['tnum'])
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


def tsave():
    r=msgbox("Save record?","Record")
    if r == True:
        newid = mycol.count_documents({})
        if newid!=0:
            newid=mycol.find_one(sort=[("tid", -1)])["tid"] 
            id=newid+1 
            tid.set(int(id))
            mydict = {"tid":int(teachid.get()), "tname":teachname.get(), "tdept":teachdept.get(), "tnum":teachnum.get()}
            x = mycol.insert_one(mydict)
            creategrid(1)
            creategrid(0)


def tdelete():
    r=msgbox("Delete?","record")
    if r == True:
        myquery = {"tid":int(teachid.get())}
        mycol.delete_one(myquery)
        creategrid(1)
        creategrid(0)


def tupdate():
    r=msgbox("Update?","record")
    if r == True:
        myquery = {"tid": int(teachid.get())}
        newvalues = {"$set":{"tname": teachname.get()}}
        mycol.update_one(myquery,newvalues)

        newvalues = {"$set":{"tdept": teachdept.get()}}
        mycol.update_one(myquery,newvalues)

        newvalues = {"$set":{"tnum": teachnum.get()}}
        mycol.update_one(myquery,newvalues)

        creategrid(1)
        creategrid(0)


def tfilters():
    creategrid(1)
    mongoquery = mydb.get_collection("teachers")
    startname = '^' + ftsname.get()
    #startemail = '^' + femail.get()
    endname = ftname.get() + '$'
    selected = options.get()
   # x= int(filterid.get()) 
    result = mongoquery.find({"$and": [{"tid":{selected:fid.get()}},{"tname":{'$regex':endname}}, {"tname":{'$regex':startname}}, {"tdept":{'$regex':fdept.get()}}, {"tnum":{'$regex':fnum.get()}} ] })
    print(ftname.get())
    print(selected)
    
    lst.clear()
    lst.append(['ID' , 'Name', 'Dept' , 'Number'])
    
    for text_fromDB in result:
        studid = str(text_fromDB['tid'])
        studname = str(text_fromDB['tname'].encode('utf-8').decode('utf-8'))
        studemail = str(text_fromDB['tdept'].encode('utf-8').decode('utf-8'))
        studcourse = str(text_fromDB['tnum'])
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



window = tk.Tk()
window.title("Teachers Form")
window.geometry("1050x400")
window.configure(bg="light blue")


#title hehe
label = tk.Label(window, text = "Teachers Form", width = 30 , height = 1, bg = "pink" , anchor="center")
label.config(font=("Courier",10))
label.grid(column=2,row=1)

#Teacher id
label = tk.Label(window, text = "Teachers ID", width = 15 , height = 1, bg = "pink")
label.grid(column=1,row=2)

tid=tk.StringVar(window)
teachid = tk.Entry(window , textvariable=tid) 
teachid.grid(column=2,row=2)
teachid.configure(state=tk.DISABLED)

#Teacher name
label2 = tk.Label(window, text = "Teacher Name", width = 15 , height = 1, bg = "pink")
label2.grid(column=1,row=3)

tname=tk.StringVar(window)
teachname = tk.Entry(window , textvariable=tname) 
teachname.grid(column=2,row=3)

#Department
label3 = tk.Label(window, text = "Department", width = 15 , height = 1, bg = "pink")
label3.grid(column=1,row=4)

tdept=tk.StringVar(window)
teachdept = tk.Entry(window , textvariable=tdept) 
teachdept.grid(column=2,row=4)

#Contact
label4 = tk.Label(window, text = "Contact Num", width = 15 , height = 1, bg = "pink")
label4.grid(column=1,row=5)

tnum=tk.StringVar(window)
teachnum = tk.Entry(window , textvariable=tnum) 
teachnum.grid(column=2,row=5)

#create table
creategrid(0)

#Buttons
savebtn = tk.Button(window,text = "Save", command=tsave)
savebtn.grid(column=1, row=6)
delbtn = tk.Button(window,text = "Delete", command=tdelete)
delbtn.grid(column=2, row=6)
upbtn = tk.Button(window,text = "Update", command=tupdate)
upbtn.grid(column=3, row=6)
fltrbtn = tk.Button(window,text = "Filter", command=tfilters)
fltrbtn.grid(column=10, row=6)

#filter
n = tk.StringVar(window) #secret

options = tk.StringVar(window)
options.trace_add('write', lambda *args: print(options.get()))
options.set('$gt')
drop = tk.OptionMenu( window , options ,'$gt', '$lt', '$gte' ,'$lte','$eq','$ne')
drop.grid(column=6, row=6)


#textbox for filter
#id
label8 = tk.Label(window, text = "Filter ID", width = 10 , height = 1, bg = "pink")
label8.grid(column=6,row=4)

fid=tk.IntVar(window)
filterid = tk.Entry(window , textvariable=fid, width= 10) 
filterid.grid(column=6,row=5)


#Start Name
label7 = tk.Label(window, text = "StartName", width = 10 , height = 1, bg = "pink")
label7.grid(column=7,row=3)

ftsname=tk.StringVar(window)
filtersname = tk.Entry(window , textvariable=ftsname, width= 10) 
filtersname.grid(column=7,row=4)

#EndName
label5 = tk.Label(window, text = "Endname", width = 10 , height = 1, bg = "pink")
label5.grid(column=7,row=5)

ftname=tk.StringVar(window)
filtername = tk.Entry(window ,width= 10 , textvariable=ftname) 
filtername.grid(column=7,row=6)

#email
label6 = tk.Label(window, text = "Start Email", width = 10 , height = 1, bg = "pink")
label6.grid(column=8,row=5)

fdept=tk.StringVar(window)
filteremail = tk.Entry(window , textvariable=fdept, width= 10) 
filteremail.grid(column=8,row=6)

#number
label6 = tk.Label(window, text = "Number", width = 10 , height = 1, bg = "pink")
label6.grid(column=9,row=5)

fnum=tk.StringVar(window)
filtercourse = tk.Entry(window , textvariable=fnum, width= 10) 
filtercourse.grid(column=9,row=6)



window.mainloop()