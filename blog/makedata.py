import datetime
import matplotlib.pyplot as plt
import os
import numpy as np
from oauth2client.service_account import ServiceAccountCredentials
import time
import gspread
global Student_logs
global Grades
global Schools
global Wiseman
Grades = {}
Schools = {}
Wiseman = {"totalworking":datetime.timedelta(seconds= 0),
            "totaltime" : datetime.timedelta(seconds= 0)}
grade_list=["고1","고2","고3"]
from matplotlib import font_manager, rc

def secondtotime(seconds):
    num = int(seconds)
    sec = num % 60
    num /= 60
    minu = int(num) % 60
    num /= 60
    hour = int(num)
    re_str = str(hour) + ":"+ str(minu) + ":"+ str(sec)
    return re_str
class Dailydata(object):
    data = {}
    def __init__(self):
        self.data = {}
    def adddata(self,alist):
        self.data["visit"] = alist[1]
        self.data["total"] = alist[2]
        self.data["working"] = alist[3]
        self.data["break1"] = alist[5]
        self.data["break2"] = alist[4]
        self.data["Nobreak"] = alist[6]
        self.data["concenttime"] = alist[7]
        
def waterfallchart(seat,data):
    studentname = Student_logs[seat-1].name
    schoolname = Student_logs[seat-1].school
    studentgrade = Student_logs[seat-1].grade
    totaltime = data[8]
    breaking1 = data[6].total_seconds()
    breaking2 = data[7].total_seconds()
    working = data[1].total_seconds()
    y=[totaltime,0, breaking1,0, breaking2,0, working]
    xlabel = ["total"," ","break1"," ","break2"," ","studying"]
    xpos= np.arange(7)
    plt.figure(1)
    plt.bar(xpos, y)
    plt.xticks(xpos,xlabel)
    plt.savefig('img/{0}.png'.format("Study"), dpi=200)

def focuschart(seat,data):

    studentname = Student_logs[seat-1].name
    schoolname = Student_logs[seat-1].school
    studentgrade = Student_logs[seat-1].grade
    focustime = data[2].total_seconds()
    breakingtime = data[3].total_seconds()
    xlabel=['AVE.Con.','AVE.Breaking']
    y=[focustime, breakingtime]
    xpos= np.arange(2)
    plt.figure(2)
    plt.bar(xpos, y)
    plt.xticks(xpos,xlabel)
    plt.savefig('img/{0}.png'.format("Focus"), dpi=200)
    
    test =1

def patternchart(seat,data):
    pass

def monthpatternchart(seat,data):
    pass
class Student_log(object):
    name = ""
    school = ""
    grade = 0
    log = {}
    average = {}
    totaldays = 0
    totalworking = datetime.timedelta(seconds= 0)
    totaltime = datetime.timedelta(seconds= 0)
    def __init__(self,name,school,grade):
        self.name = name
        self.school = school
        self.grade = grade
        self.log = {}
        self.average = {}
        self.totaldays = 0
        self.totalworking = datetime.timedelta(seconds= 0)
        self.totaltime = datetime.timedelta(seconds= 0)
        
    def adddata(self,adata,day):
        if day in self.log.keys():
            for x in self.log[day].keys():
                self.log[day][x] += adata[x]
            if x == "total":
                self.totaltime += adata[x]
            if x == "working":
                self.totalworking +=adata[x]


        else:
            self.log[day]=adata
            self.totaltime += adata["total"]
            self.totalworking += adata["working"]
            self.totaldays += 1
            
    def calculateaverage(self):
        
        for i in self.log:
            for x in self.log[i].keys():
                if x in self.average.keys():
                    if x == "visit" or x == "total":
                        self.average[x] += self.log[i][x]
                    else:
                        self.average[x] += self.log[i][x]/self.totaldays
                else:
                    if x == "visit" or x == "total":
                        self.average[x] = self.log[i][x]
                    else:
                        self.average[x] = self.log[i][x]/self.totaldays

def datagatheringfromgss(seat,afirstday,alastday):

    day_duration = alastday-afirstday
    #firstday = afirstday.strftime("%Y-%m-%d")
    #lastday = alastday.strftime("%Y-%m-%d")
    daylist= []
    daylist_str = []
    for i in range(0,day_duration.days+1):
        temp_day = afirstday+datetime.timedelta(days = i)
        daylist.append(temp_day)
        daylist_str.append(temp_day.strftime("%Y-%m-%d"))


    
    filename = "착석 Log"
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('/Users/adonisysk/Desktop/conalog/programing/onewise/test_id.json', scope)
    #credentials = ServiceAccountCredentials.from_json_keyfile_name('/home/onewise/test_id.json', scope)
    gc = gspread.authorize(credentials)
    gs = gc.open(filename)
    
    for i in range(1,11):
        seat = i
        sheetname = "seat"+str(seat)
        wks = gs.worksheet(sheetname)
        k = 0
        while True:
            
            if wks.find(daylist_str[k]).row > 0:
                firstcell = wks.find(daylist_str[k])
                break
            else:
                k += 1  
        data_from_gss = wks.get_all_values()
        k= firstcell.row-1
        
        while True:
            result = Dailydata()
            temp = data_from_gss[k]
            temp = temp[4:11]
            if temp[0] in daylist_str:    
                temp[1] = 1
                day = temp[0].split("-")
                temp[0] =datetime.date(int(day[0]),int(day[1]),int(day[2]))
                for j in range(2,6):
                    time = temp[j].split(":")
                    time = int(time[0])*3600+int(time[1])*60+int(time[2])
                    temp[j] = datetime.timedelta(seconds=time)
                temp[6]= int(temp[6])
                temp.append(temp[3]/(temp[6]+1))
                result.adddata(temp)
                Student_logs[i-1].adddata(result.data,temp[0])
                k +=1
            else:
                break
        
def getaverage():
    
    for x in Student_logs:
        x.calculateaverage()
        if Wiseman["totaltime"]<x.totaltime:
            Wiseman["totaltime"]=x.totaltime
        else:
            pass
        if Wiseman["totalworking"] < x.totalworking:
            Wiseman["totalworking"] =x.totalworking
        else:
            pass
        for y in x.average:
            if y in Wiseman.keys():
                if y == "break1" or y == "break2" or y=="Nobreak":

                    if Wiseman[y]>x.average[y]:
                        Wiseman[y]=x.average[y]
                    else:
                        pass
                else:
                    if Wiseman[y]<x.average[y]:
                        Wiseman[y]=x.average[y]
                    else:
                        pass
            else:
                Wiseman[y]=x.average[y]
            if y in Schools[x.school].keys():
                Schools[x.school][y] += x.average[y]/Schools[x.school]["Nostudent"]
            else:
                Schools[x.school][y] = x.average[y]/Schools[x.school]["Nostudent"]
            if y in Grades[x.grade].keys():
                Grades[x.grade][y] += x.average[y]/Grades[x.grade]["Nostudent"]
            else:
                Grades[x.grade][y] = x.average[y]/Grades[x.grade]["Nostudent"]
            
            
    
    return True

def getresult(seat,weakormonth):
    #result = [[0 for rows in range(6)]for cols in range(9)]
    student = Student_logs[seat -1]
    grade= grade_list[student.grade -1]
    school = student.school
    if weakormonth == "week":
        days = 7
    else:
        days = 30
    student_result = []
    student_result.append(student.totaltime.total_seconds())
    student_result.append(student.average["working"])
    student_result.append(student.average["concenttime"])
    student_result.append(student.average["break1"]/student.average["Nobreak"])
    student_result.append(round(student.average["Nobreak"],1))
    student_result.append(round(student.totaldays/days*100,1))
    student_result.append(student.average["break1"])
    student_result.append(student.average["break2"])
    student_result.append(student.totaltime.total_seconds()/student.totaldays)
    if weakormonth == "week": 
        patternchart(seat,student)
    else:
        monthpatternchart(seat,student)
    waterfallchart(seat,student_result)
    focuschart(seat,student_result)

    table =  [
                ["","등급","result",grade+"평균","차이",school+"평균","차이","Wiseman","차이"],
                ["총순공시간"],
                ["평균순공시간/일"],
                ["평균집중시간/일"],
                ["평균자리비움시간/회"],
                ["자리비움횟수/일"],
                ["출석률"]
                ]

    result ={}
    result["table"] = table
    return True

def getdata(seat,startdate,weekormonth):
    #firstday = startdate.strftime("%Y-%m-%d")    

    if weekormonth == "week":
        enddate = startdate + datetime.timedelta(days=6)
        #lastday = enddate.strftime("%Y-%m-%d")
            
    elif weekormonth =="month":
        enddate = startdate + datetime.timedelta(days=30)
    datagatheringfromgss(seat,startdate,enddate)
    getaverage()
    



    return True
Student_logs =[ Student_log("곽남주","동덕여고",3),
                Student_log("이정안","동덕여고",3),
                Student_log("전윤경","숙명여고",3),
                Student_log("구태윤","동북고",3),
                Student_log("김재현","상문고",3),
                Student_log("강준서","서울고",3),
                Student_log("박태준","서울고",3),
                Student_log("이상재","서울고",3),
                Student_log("김주호","상문고",3),
                Student_log("김형민","상문고",3),]
for x in Student_logs:
    if x.school in Schools:
        Schools[x.school]["Nostudent"] += 1
    else:
        Schools[x.school] = {"Nostudent":1,}
    if x.grade in Grades:
        Grades[x.grade]["Nostudent"] += 1
    else:
        Grades[x.grade]={"Nostudent" : 1}   



    
startdate = datetime.date(2018,10,12)
getdata(1,startdate,"week")
result = getresult(1,"week")

test =1

