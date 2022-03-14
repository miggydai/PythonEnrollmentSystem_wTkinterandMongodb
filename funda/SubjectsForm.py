import pymongo
import tkinter as tk
from tkinter import messagebox
#variables & mongodb connect
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["enrollmentsystem"]
mycol = mydb["subjects"]
lst = [['ID' , 'Code', 'Desc' , 'Units' , 'Sched']]

#assign to table
def callback(event):  
    li=[]
    li=event.widget._values
    subID.set(lst[li[1]][0])
    subCode.set(lst[li[1]][1])
    sdesc.set(lst[li[1]][2])
    units.set(lst[li[1]][3])
    sched.set(lst[li[1]][4])

#create table
def creategrid(n):
    lst.clear()
    lst.append(['ID' , 'Code', 'Desc' , 'Units' , 'Sched'])
    cursor = mycol.find({}) 
    for text_fromDB in cursor:
        studid = str(text_fromDB['subID'])
        studname = str(text_fromDB['subCode'].encode('utf-8').decode('utf-8'))
        studemail = str(text_fromDB['sdesc'].encode('utf-8').decode('utf-8'))
        studcourse = str(text_fromDB['units'])
        schedule =  str(text_fromDB['sched'].encode('utf-8').decode('utf-8'))
        lst.append([studid,studname,studemail,studcourse,schedule])
    
    for i in range(len(lst)):
       
        for j in range(len(lst[0])):
            mgrid = tk.Entry(window,width=10)
            mgrid.insert(tk.END,lst[i][j])
            mgrid._values = mgrid.get(), i
            mgrid.grid(row=i+8, column=j+4)
            mgrid.bind("<Button-1>", callback)
    if n == 1:
        for label in window.grid_slaves():
            if int(label.grid_info()["row"]) > 7:
                label.grid_forget()

#messagebox
def msgbox(msg,titlebar):
    result=messagebox.askokcancel(title=titlebar,message=msg)
    return result




def subsave():
     r=msgbox("Save record?","Record")
     if r == True:
        newid = mycol.count_documents({})
        if newid!=0:
            try:
                newid=mycol.find_one(sort=[("subID", -1)])["subID"] 
                id=newid+1 
                subID.set(int(id))
                sub = float(subid.get())
                mydict = {"subID":int(sub), "subCode":subjcode.get(), "sdesc":subjdesc.get(), "units":subjunits.get(), "sched": subjsched.get()}
                x = mycol.insert_one(mydict)
                creategrid(1)
                creategrid(0)
            except:
                print("shet")


def subdelete():
    r=msgbox("Delete?","record")
    if r == True:
        myquery = {"subID":int(subid.get())}
        mycol.delete_one(myquery)
        creategrid(1);
        creategrid(0);


def subupdate():
    r=msgbox("Update?","record")
    if r == True:
        myquery = {"subID": int(subid.get())}
        newvalues = {"$set":{"subCode": subjcode.get()}}
        mycol.update_one(myquery,newvalues)

        newvalues = {"$set":{"sdesc": subjdesc.get()}}
        mycol.update_one(myquery,newvalues)

        newvalues = {"$set":{"units": subjunits.get()}}
        mycol.update_one(myquery,newvalues)

        newvalues = {"$set":{"sched": subjsched.get()}}
        mycol.update_one(myquery,newvalues)

        creategrid(1)
        creategrid(0)


def sfilters():
    creategrid(1)
    mongoquery = mydb.get_collection("subjects")
    startname = '^' + ftsname.get()
    #startemail = '^' + femail.get()
    endname = ftname.get() + '$'
    startdesc = '^' + fcourse.get()
    selected = options.get()
   # x= int(filterid.get()) 
    result = mongoquery.find({"$and": [{"subID":{selected:fid.get()}} ,{"subCode":{'$regex':endname}} , {"subCode":{'$regex':startname}}, {"sdesc":{'$regex':startdesc}}, {"units":{'$regex':fnum.get()}}, {"sched":{'$regex':fsched.get()}}  ] })
    print(ftname.get())
    print(selected)
    lst.clear()
    lst.append(['ID' , 'Code', 'Desc' , 'Units' , 'Sched'])
    
    for text_fromDB in result:
        studid = str(text_fromDB['subID'])
        studname = str(text_fromDB['subCode'].encode('utf-8').decode('utf-8'))
        studemail = str(text_fromDB['sdesc'].encode('utf-8').decode('utf-8'))
        studcourse = str(text_fromDB['units'])
        schedule =  str(text_fromDB['sched'].encode('utf-8').decode('utf-8'))
        lst.append([studid,studname,studemail,studcourse,schedule])
    
    for i in range(len(lst)):
       
        for j in range(len(lst[0])):
            mgrid = tk.Entry(window,width=10)
            mgrid.insert(tk.END,lst[i][j])
            mgrid._values = mgrid.get(), i
            mgrid.grid(row=i+8, column=j+4)
            mgrid.bind("<Button-1>", callback)
    if n == 1:
        for label in window.grid_slaves():
            if int(label.grid_info()["row"]) > 7:
                label.grid_forget()


#Form
window = tk.Tk()
window.title("Students Form")
window.geometry("1050x400")
window.configure(bg="light blue")


#title
label = tk.Label(window, text = "Subjects Form", width = 30 , height = 1, bg = "pink" , anchor="center")
label.config(font=("Courier",10))
label.grid(column=2,row=1)

#SubjectID
label = tk.Label(window, text = "Subject ID", width = 15 , height = 1, bg = "pink")
label.grid(column=1,row=2)

subID=tk.StringVar(window)
subid = tk.Entry(window , textvariable=subID) 
subid.grid(column=2,row=2)
subid.configure(state=tk.DISABLED)

#SubjectCode
label2 = tk.Label(window, text = "Subject Code", width = 15 , height = 1, bg = "pink")
label2.grid(column=1,row=3)

subCode=tk.StringVar(window)
subjcode = tk.Entry(window , textvariable=subCode) 
subjcode.grid(column=2,row=3)

#Subject Description
label3 = tk.Label(window, text = "Subject Description", width = 15 , height = 1, bg = "pink")
label3.grid(column=1,row=4)

sdesc=tk.StringVar(window)
subjdesc = tk.Entry(window , textvariable=sdesc) 
subjdesc.grid(column=2,row=4)

#Units
label4 = tk.Label(window, text = "Units", width = 15 , height = 1, bg = "pink")
label4.grid(column=1,row=5)

units=tk.StringVar(window)
subjunits = tk.Entry(window , textvariable=units) 
subjunits.grid(column=2,row=5)

#Sched
label4 = tk.Label(window, text = "Schedule", width = 15 , height = 1, bg = "pink")
label4.grid(column=1,row=6)

sched=tk.StringVar(window)
subjsched = tk.Entry(window , textvariable=sched) 
subjsched.grid(column=2,row=6)

#create table
creategrid(0)

#Buttons
savebtn = tk.Button(window, text = "Save", command=subsave)
savebtn.grid(column=1, row=7)
delbtn = tk.Button(window, text = "Delete", command=subdelete)
delbtn.grid(column=2, row=7)
upbtn = tk.Button(window, text = "Update", command=subupdate)
upbtn.grid(column=3, row=7)
fltrbtn = tk.Button(window,text = "Filter", command=sfilters)
fltrbtn.grid(column=9, row=7)

#filter
n = tk.StringVar(window) #secret

options = tk.StringVar(window)
options.trace_add('write', lambda *args: print(options.get()))
options.set('$gt')
drop = tk.OptionMenu( window , options ,'$gt', '$lt', '$gte' ,'$lte','$eq','$ne')
drop.grid(column=4, row=7)

#textbox for filter
#id
label8 = tk.Label(window, text = "Filter ID", width = 10 , height = 1, bg = "pink")
label8.grid(column=4,row=5)

fid=tk.IntVar(window)
filterid = tk.Entry(window , textvariable=fid, width= 10) 
filterid.grid(column=4,row=6)

#Start Code
label7 = tk.Label(window, text = "StartCode", width = 10 , height = 1, bg = "pink")
label7.grid(column=5,row=4)

ftsname=tk.StringVar(window)
filtersname = tk.Entry(window , textvariable=ftsname, width= 10) 
filtersname.grid(column=5,row=5)

#EndName
label5 = tk.Label(window, text = "End Code", width = 10 , height = 1, bg = "pink")
label5.grid(column=5,row=6)

ftname=tk.StringVar(window)
filtername = tk.Entry(window ,width= 10 , textvariable=ftname) 
filtername.grid(column=5,row=7)

#desc
label6 = tk.Label(window, text = "Desc", width = 10 , height = 1, bg = "pink")
label6.grid(column=6,row=6)

fcourse=tk.StringVar(window)
filtercourse = tk.Entry(window , textvariable=fcourse, width= 10) 
filtercourse.grid(column=6,row=7)

#Units
label9 = tk.Label(window, text = "Units", width = 10 , height = 1, bg = "pink")
label9.grid(column=7,row=6)

fnum=tk.StringVar(window)
filterunits = tk.Entry(window , textvariable=fnum, width= 10) 
filterunits.grid(column=7,row=7)

#Sched
label10 = tk.Label(window, text = "Sched", width = 10 , height = 1, bg = "pink")
label10.grid(column=8,row=6)

fsched=tk.StringVar(window)
filtersched = tk.Entry(window , textvariable=fsched, width= 10) 
filtersched.grid(column=8,row=7)


window.mainloop()