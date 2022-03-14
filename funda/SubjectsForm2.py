import pymongo
import tkinter as tk
from tkinter import messagebox
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["enrollmentsystem"]
mycol = mydb["subjects2"]
lst = [['ID' , 'Code', 'Desc' , 'Units' , 'Sched']]
subjectid = 0
window = ""
#IDs
subID =""
subid = ""
#subject code
subCode = ""
subjcode = ""
#subject desc
sdesc= ""
subjdesc = ""
#units
units = ""
subjunits = ""
#sched
sched = ""
subjsched =""

#assign to table
def callback(event):
    global subjectid  
    li=[]
    li=event.widget._values
    subID.set(lst[li[1]][0])
    subCode.set(lst[li[1]][1])
    sdesc.set(lst[li[1]][2])
    units.set(lst[li[1]][3])
    sched.set(lst[li[1]][4])
    subjectid = (lst[li[1]][0])
    print(subjectid)
    

def creategrid(n):
    lst.clear()
    lst.append(['ID' , 'Code', 'Desc' , 'Units' , 'Sched'])
    cursor = mycol.find({}) 
    for text_fromDB in cursor:
        studid = str(text_fromDB['subjid'])
        studname = str(text_fromDB['subjcode'].encode('utf-8').decode('utf-8'))
        studemail = str(text_fromDB['subjdesc'].encode('utf-8').decode('utf-8'))
        studcourse = str(text_fromDB['subjunits'])
        schedule =  str(text_fromDB['subjsched'].encode('utf-8').decode('utf-8'))
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


#save
def subsave():
    r=msgbox("Save record?","Record")
    if r == True:
        newid = mycol.count_documents({})
        if newid!=0:        
            newid=mycol.find_one(sort=[("subjid", -1)])["subjid"] 
            id=newid+1 
            subID.set(int(id))
            sub = float(subid.get())
            mydict = {"subjid":int(sub), "subjcode":subjcode.get(), "subjdesc":subjdesc.get(), "subjunits":int(subjunits.get()), "subjsched": subjsched.get()}
            x = mycol.insert_one(mydict)
            creategrid(1)
            creategrid(0)
        else:
            id=newid+1 
            subID.set(int(id))
            sub = float(subid.get())
            mydict = {"subjid":int(sub), "subjcode":subjcode.get(), "subjdesc":subjdesc.get(), "subjunits":int(subjunits.get()), "subjsched": subjsched.get()}
            x = mycol.insert_one(mydict)
            creategrid(1)
            creategrid(0)
           

#delete
def subdelete():
    r=msgbox("Delete?","record")
    if r == True:
        myquery = {"subjid":int(subid.get())}
        mycol.delete_one(myquery)
        creategrid(1);
        creategrid(0);

    
#update
def subupdate():
   r=msgbox("Update?","record")
   if r == True:
        myquery = {"subjid": int(subid.get())}
        newvalues = {"$set":{"subjcode": subjcode.get()}}
        mycol.update_one(myquery,newvalues)

        newvalues = {"$set":{"subjdesc": subjdesc.get()}}
        mycol.update_one(myquery,newvalues)

        newvalues = {"$set":{"subjunits": int(subjunits.get())}}
        mycol.update_one(myquery,newvalues)

        newvalues = {"$set":{"subjsched": subjsched.get()}}
        mycol.update_one(myquery,newvalues)

        creategrid(1)
        creategrid(0)



#Form
def subss():
    global window
    #IDs
    global subID
    global subid
    #subject code
    global subCode
    global subjcode
    #subject desc
    global sdesc
    global subjdesc
    #units
    global units
    global subjunits
    #sched
    global sched
    global subjsched
    window = tk.Tk()
    window.title("Subjects Form")
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



    window.mainloop()