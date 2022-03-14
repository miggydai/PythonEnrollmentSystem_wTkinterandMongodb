from tabnanny import check
from typing import final
from matplotlib.pyplot import magnitude_spectrum
import pymongo
import tkinter as tk
from tkinter import E, messagebox
import SubjectsForm2

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["enrollmentsystem"]
#global studentid
#for filters(might change)
studentscol = mydb.get_collection("students2")
subjectscol = mydb.get_collection("subjects2")

pipeline1 = [{"$lookup": {"from":"subjects2", "localField": "enrolled.subjid", "foreignField":"subjid", "as":"enrolled" }}, {"$unwind": {"path": "$enrolled","preserveNullAndEmptyArrays":True}}, {"$project": {"sid":1,"sname":1,"semail":1,"scourse":1,"units":"$enrolled.subjunits"}}, {"$group": {"_id":'$sid', "name":{"$first":'$sname'},"email":{"$first":'$semail'},"course":{"$first":'$scourse'}, "totunits":{"$sum":'$units'} } } ]
#pipeline2 = [{"$match":{"sid":3}},{"$lookup": {"from":"subjects2", "localField": "subjid", "foreignField":"subjid", "as":"enrolled" }}, {"$unwind": {"path": "$enrolled","preserveNullAndEmptyArrays":True}}, {"$project": {"subjid":"$enrolled.subjid","subjcode":"$enrolled.subjcode","subjdesc":"$enrolled.subjdesc","subjsched":"$enrolled.subjsched","units":"$enrolled.subjunits"}}, {"$group": {"_id":'$subjid', "SubCode":{"$first":'$subjcode'},"SubjDesc":{"$first":'$subjdesc'},"SubjUnits":{"$first":'$units'}, "sched":{"$first":'$subjsched'} } }]

mycol = mydb["students2"]
lst = [['ID' , 'Name', 'Email' , 'Course', 'Units']]
#for subjects
smycol = mydb["subjects2"]
slst = [['ID' , 'Code', 'Desc' , 'Units' , 'Sched']]
#for grades
elst = [['ID','prelim' , 'midterm', 'prefinal' , 'final']]
studentid = 0
global subjectid



def gradegrid(n):
    elst.clear()
    elst.append(['ID','prelim' , 'mid', 'prefinal' , 'final'])
    cursor = studentscol.aggregate([
{"$match": {
  "sid": studentid,
  "enrolled.subjid": enrollid
 }
},
{
 "$addFields": {
  "enrolled": {
    "$filter": {
      "input": "$enrolled",
      "as": "en",
      "cond": {
        "$eq": [
          "$$en.subjid",
          enrollid
        ]
      }
    }
   }
  }
 },
 {
  "$unwind": {"path":"$enrolled","preserveNullAndEmptyArrays":True}
 },
 {
  "$unwind": {"path":"$enrolled.grades","preserveNullAndEmptyArrays":True}
 },
 {"$limit":1}
  ,
 {
  "$project": {
  "_id": "$enrolled.subjid",
  "prelim": "$enrolled.grades.prelim",
  "midterm": "$enrolled.grades.midterm",
  "prefinal": "$enrolled.grades.prefinal",
  "final": "$enrolled.grades.final"
  }
 },
{"$group": {"_id":'$_id', "prelim":{"$first":'$prelim'},"midterm":{"$first":'$midterm'},"prefinal":{"$first":'$prefinal'},"final":{"$first":'$final'} } }
])
    #print(cursor)
    for text_fromDB in cursor:       
        studid = str(text_fromDB['_id'])
        studname = str(text_fromDB['prelim'])
        studemail = str(text_fromDB['midterm'])
        studcourse = str(text_fromDB['prefinal'])
        schedule =  str(text_fromDB['final'])
        elst.append([studid,studname,studemail,studcourse,schedule])
   

    for i in range(len(elst)):
        if not elst[1]:
            for j in range(len(elst[0])):
                mgrid = tk.Entry(window,width=10)
                mgrid.insert(tk.END,elst[i][j])
                mgrid._values = mgrid.get(), i
                mgrid.grid(row=i+25, column=j+4)
                mgrid.bind("<Button-1>", callback3)
        else:
            for j in range(len(elst[1])):
                mgrid = tk.Entry(window,width=10)
                mgrid.insert(tk.END,elst[i][j])
                mgrid._values = mgrid.get(), i
                mgrid.grid(row=i+25, column=j+4)
                mgrid.bind("<Button-1>", callback3)
    if n == 1:
        for label in window.grid_slaves():
            if int(label.grid_info()["row"]) > 25:
                label.grid_forget()





def callback3(event):
    #global prelim
   # global midterm
    #global prefinal
    #global final
    li = []
    li = event.widget._values
    prelim.set(elst[li[1]][1])
    midterm.set(elst[li[1]][2])
    prefinal.set(elst[li[1]][3])
    final.set(elst[li[1]][4])
    #print(prelim)
    #print(midterm)
    #print(prefinal)
    #print(final)




def savegrade():
    r=msgbox("Save Grade?","Record")
    try:
        if r == True:
             mycol.update_one({"sid":studentid,"enrolled.subjid":enrollid},{"$push":{"enrolled.$.grades":{"prelim":preL.get(), "midterm": mid.get(), "prefinal": preF.get(), "final":ff.get()} } })
             gradegrid(1)
             gradegrid(0)
            
    except:
        print("yawa")



def updategrade():
    r=msgbox("Update Grade?","Record")
    try:
        if r == True:
             mycol.update_one({"sid":studentid,"enrolled.subjid":enrollid},{"$set":{"enrolled.$.grades":{"prelim":preL.get(), "midterm": mid.get(), "prefinal": preF.get(), "final":ff.get()} } })
             gradegrid(1)
             gradegrid(0)
            
    except:
        print("yawa")



def enrollgrid(n):
    slst.clear()
    slst.append(['ID' , 'Code', 'Desc' , 'Units' , 'Sched'])
    cursor = studentscol.aggregate([{"$match":{"sid":sid.get()}},{"$lookup": {"from":"subjects2", "localField": "enrolled.subjid", "foreignField":"subjid", "as":"enrolled" }}, {"$unwind": {"path": "$enrolled","preserveNullAndEmptyArrays":True}}, {"$project": {"subjid":"$enrolled.subjid","subjcode":"$enrolled.subjcode","subjdesc":"$enrolled.subjdesc","subjsched":"$enrolled.subjsched","units":"$enrolled.subjunits"}}, {"$group": {"_id":'$subjid', "SubCode":{"$first":'$subjcode'},"SubjDesc":{"$first":'$subjdesc'},"SubjUnits":{"$first":'$units'}, "sched":{"$first":'$subjsched'} } }]) 
    #print(cursor)
    for text_fromDB in cursor:
        studid = str(text_fromDB['_id'])
        studname = str(text_fromDB['SubCode'].encode('utf-8').decode('utf-8'))
        studemail = str(text_fromDB['SubjDesc'].encode('utf-8').decode('utf-8'))
        studcourse = str(text_fromDB['SubjUnits'])
        schedule =  str(text_fromDB['sched'].encode('utf-8').decode('utf-8'))
        slst.append([studid,studname,studemail,studcourse,schedule])
    
    for i in range(len(slst)):
       
        for j in range(len(slst[0])):
            mgrid = tk.Entry(window,width=10)
            mgrid.insert(tk.END,slst[i][j])
            mgrid._values = mgrid.get(), i
            mgrid.grid(row=i+15, column=j+4)
            mgrid.bind("<Button-1>", callback2)
    if n == 1:
        for label in window.grid_slaves():
            if int(label.grid_info()["row"]) > 15:
                label.grid_forget()



def callback2(event):
    global enrollid
    li = []
    li = event.widget._values
    sid.set((slst[li[1]][0]))
    enrollid = int((slst[li[1]][0]))
    print(enrollid)
    gradegrid(1)
    gradegrid(0)

#assign to table
def callback(event):
    global studentid  
    li=[]
    li=event.widget._values
    sid.set(lst[li[1]][0])
    sname.set(lst[li[1]][1])
    semail.set(lst[li[1]][2])
    scourse.set(lst[li[1]][3])
    studentid = int((lst[li[1]][0]))
    #from SubjectsForm2 import subjectid
    #print(SubjectsForm2.subjectid)
    print(studentid)
    #table
    enrollgrid(1)
    enrollgrid(0)



#print(subjectid)
#create table
def creategrid(n):
    lst.clear()
    lst.append(['ID' , 'Name', 'Email' , 'Course','Units'])
    cursor = studentscol.aggregate(pipeline1) 
    #print(cursor)
    for text_fromDB in cursor:
        studid = str(text_fromDB['_id'])
        studname = str(text_fromDB['name'].encode('utf-8').decode('utf-8'))
        studemail = str(text_fromDB['email'].encode('utf-8').decode('utf-8'))
        studcourse = str(text_fromDB['course'].encode('utf-8').decode('utf-8'))
        studunits = str(text_fromDB['totunits'])
        lst.append([studid,studname,studemail,studcourse,studunits])
    
    for i in range(len(lst)):
       
        for j in range(len(lst[0])):
            mgrid = tk.Entry(window,width=10)
            mgrid.insert(tk.END,lst[i][j])
            mgrid._values = mgrid.get(), i
            mgrid.grid(row=i+8, column=j+4)
            mgrid.bind("<Button-1>", callback)
    if n == 1:
        for label in window.grid_slaves():
            if int(label.grid_info()["row"]) > 8:
                label.grid_forget()

#messagebox
def msgbox(msg,titlebar):
    result=messagebox.askokcancel(title=titlebar,message=msg)
    return result

#save
def save():   
    r=msgbox("Save record?","Record")
    try:
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
            else:
                id=newid+1 
                sid.set(int(id))
                mydict = {"sid":int(studid.get()), "sname":studname.get(), "semail":studemail.get(), "scourse":studcourse.get()}
                x = mycol.insert_one(mydict)
                creategrid(1)
                creategrid(0)
    except:
        print("yawa")



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


#===================================FOR SUBJECTS+++++++++++++++++++++++++++++++++


def subjectsform2():
    import SubjectsForm2


#call teachersform
def teachersform():
    import TeachersForm



#Add Subject
def add():
    r=msgbox("insert subject number:"+str(SubjectsForm2.subjectid)+" to student:"+str(studentid),"record")
    if r == True:
        mycol.update_one({"sid":studentid},{"$push":{"enrolled":{"subjid": int(SubjectsForm2.subjectid)}}})
        creategrid(1)
        creategrid(0)
 


#Drop Subject
def drop():
    global studentid
    print(studentid)
    r=msgbox("remove subject number:"+str(enrollid)+" to student number:"+str(studentid),"record")
    if r == True:
        mycol.update_one({"sid":studentid},{"$pull":{"enrolled":{"subjid": enrollid}}})
        creategrid(1)
        creategrid(0)



def filters():
    creategrid(1)
    mongoquery = mydb.get_collection("students")
    startname = '^' + fsname.get()
    startemail = '^' + femail.get()
    endname = fname.get() + '$'
    selected = options.get()
   # x= int(filterid.get()) 
    result = mongoquery.aggregate( [ {"$match":{"$and": [{"sname":{'$regex':endname}},{"semail":{'$regex':startemail}},{"scourse":{'$regex':fcourse.get()}},{"sname":{'$regex':startname}}, {"sid":{selected:fid.get()}} ] } }])
    print(fname.get())
    print(selected)
    lst.clear()
    lst.append(['ID' , 'Name', 'Email' , 'Course'])
 
    for text_fromDB in result:
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
            mgrid.grid(row=i+8, column=j+4)
            mgrid.bind("<Button-1>", callback)
    if n == 1:
        for label in window.grid_slaves():
            if int(label.grid_info()["row"]) > 7:
                label.grid_forget()


#main
window = tk.Tk()
window.title("Students Form")
window.geometry("1050x400")
window.configure(bg="blue")

#Menu bar
menubar = tk.Menu(window)
filemenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="Subjects", command=SubjectsForm2.subss)
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

sid=tk.IntVar()
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
#enrollgrid(0)
#Buttons
savebtn = tk.Button(window,text = "Save", command=save)
savebtn.grid(column=1, row=6)
delbtn = tk.Button(window,text = "Delete", command=delete)
delbtn.grid(column=2, row=6)
upbtn = tk.Button(window,text = "Update", command=update)
upbtn.grid(column=3, row=6)
fltrbtn = tk.Button(window,text = "Filter", command=filters)
fltrbtn.grid(column=10, row=7)
addbtn = tk.Button(window,text = "Add Subject", command=add)
addbtn.grid(column=12, row=7)
dropbtn = tk.Button(window,text = "Drop Subject", command=drop)
dropbtn.grid(column=13, row=7)
sgradebtn = tk.Button(window,text="Save Grade", command=savegrade)
sgradebtn.grid(column=12,row=6)
ugradebtn = tk.Button(window,text="Update Grade", command=updategrade)
ugradebtn.grid(column=13,row=6)




#filter
n = tk.StringVar(window) #secret

options = tk.StringVar(window)
options.trace_add('write', lambda *args: print(options.get()))
options.set('$gt')
drop = tk.OptionMenu( window , options ,'$gt', '$lt', '$gte' ,'$lte','$eq','$ne')
drop.grid(column=4, row=6)


#textbox for filter
#id
label8 = tk.Label(window, text = "Filter ID", width = 10 , height = 1, bg = "pink")
label8.grid(column=4,row=5)

fid=tk.IntVar(window)
filterid = tk.Entry(window , textvariable=fid, width= 10) 
filterid.grid(column=4,row=7)

#EndName
label5 = tk.Label(window, text = "Endname", width = 10 , height = 1, bg = "pink")
label5.grid(column=5,row=6)

fname=tk.StringVar(window)
filtername = tk.Entry(window ,width= 10 , textvariable=fname, ) 
filtername.grid(column=5,row=7)

#email
label6 = tk.Label(window, text = "Start Email", width = 10 , height = 1, bg = "pink")
label6.grid(column=6,row=6)

femail=tk.StringVar(window)
filteremail = tk.Entry(window , textvariable=femail, width= 10) 
filteremail.grid(column=6,row=7)

#course
label6 = tk.Label(window, text = "Course", width = 10 , height = 1, bg = "pink")
label6.grid(column=7,row=6)

fcourse=tk.StringVar(window)
filtercourse = tk.Entry(window , textvariable=fcourse, width= 10) 
filtercourse.grid(column=7,row=7)

#Start Name
label7 = tk.Label(window, text = "StartName", width = 10 , height = 1, bg = "pink")
label7.grid(column=5,row=4)

fsname=tk.StringVar(window)
filtersname = tk.Entry(window , textvariable=fsname, width= 10) 
filtersname.grid(column=5,row=5)


#Gradesssss
#prelim
label01 = tk.Label(window, text = "Prelim", width = 15 , height = 1, bg = "pink")
label01.grid(column=4,row=1)

prelim=tk.StringVar()
preL = tk.Entry(window , textvariable=prelim) 
preL.grid(column=4,row=2)

#midterm
label02 = tk.Label(window, text = "Midterm", width = 15 , height = 1, bg = "pink")
label02.grid(column=5,row=1)

midterm=tk.StringVar()
mid = tk.Entry(window , textvariable=midterm) 
mid.grid(column=5,row=2)

#prefinal
label03 = tk.Label(window, text = "Prefinal", width = 15 , height = 1, bg = "pink")
label03.grid(column=6,row=1)

prefinal=tk.StringVar()
preF = tk.Entry(window , textvariable=prefinal) 
preF.grid(column=6,row=2)

#final
label04 = tk.Label(window, text = "Final", width = 15 , height = 1, bg = "pink")
label04.grid(column=7,row=1)

final=tk.StringVar()
ff = tk.Entry(window , textvariable=final) 
ff.grid(column=7,row=2)



window.mainloop()