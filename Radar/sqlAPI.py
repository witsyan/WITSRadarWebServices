#!/usr/bin/env python
#coding=utf-8

import sqlite3
import os,sys
import json
import time
import string
import datetime
reload(sys)
sys.setdefaultencoding('utf8')

# 设置数据库路径
# dbpath="/Volumes/Storage/1010/admin/Documents/mysite/db.sqlite3"
dbpath = os.path.dirname(__file__)[:-5] + '_LocProjScanner/_Projects/activeDataBase.db'

scriptPath = os.path.dirname(__file__)[:-5] + '_LocProjScanner/Script/_Python'
sys.path.append(scriptPath)
from RadarArgs import RadarArgs 
coveredProj = RadarArgs.coveredProj # Loc:Proj:OSX Updates

# 功能：获得表所有的project
# table：数据库表名
# 返回：proj数组
def getProjName():
	global dbpath
	result = []
	for aa in coveredProj:
		if isinstance(aa,dict):
			result.append(str(aa.keys()[0])) 
		else:
			result.append(str(aa))
	result=sortArr(result)
	return result

def sortArr(arr):
	for i in range(0,len(arr)):
		for j in range(1,len(arr)):
			if arr[j].capitalize()< arr[j-1].capitalize():
				temp = arr[j]
				arr[j] = arr[j-1]
				arr[j-1] = temp
	return arr

# print getProjName()

def getSqlComponentCommand(project):
	result = ""
	for aa in coveredProj:
		if isinstance(aa,dict):
			if project == aa.keys()[0]:
				temp = ','.join(map(lambda x:'\'Loc:Proj:%s\''%x, aa.values()[0]))
				result = "Component in(%s)"%temp
		else:
			if project == aa:
				result = "Component='%s'"%("Loc:Proj:"+project)
	return result

# print getSqlComponentCommand("OSX")

def checkDate(fromdate,todate):
	fromtemp = ""
	totemp = ""
	if fromdate == "all" or todate == "all":
		fromtemp = "all"
		totemp = "all"
	else:
		ff = fromdate.split("-")
		fdate = ''.join(ff)
		tt = todate.split("-")
		tdate = ''.join(tt)
		if fdate > tdate:
			fromtemp = todate
			totemp = fromdate
		else:
			fromtemp = fromdate
			totemp = todate
	return fromtemp,totemp


# 功能：获得日期列表
# table：数据库表名
# project：component的名字
# 返回：日期的列表
# eg:[2015-01-02...]
def getDateList(project,table="DailyActive",type="needhandle"):
	global dbpath
	result = []
	projs=getProjName()
	if project not in projs:
		return result
	else:
		db = sqlite3.connect(dbpath)
		cursor = db.cursor()
		command = getSqlComponentCommand(project)
		if type == "needhandle":
			sql = "select distinct LastModifiedAt from %s where %s order by LastModifiedAt asc"%(table,command)
		if type == "nohandle":
			sql = "select distinct LastModifiedAt from %s where Component='%s' order by LastModifiedAt asc"%(table,project)
		cursor.execute(sql)
		arr = cursor.fetchall()
		db.close()
		for aa in arr:
			result.append(str(aa[0]))
		return result

# print getDateList("OSX","WitsAssignee","needhandle")


def getProjDict(arr):
	proj={}
	for aa in arr:
		Id = str(aa[0])
		lang = str(aa[1])
		kind = aa[2]
		if lang in proj.keys():
			proj[lang][kind]["count"] += 1
			if Id in proj[lang][kind]["id"]:
				pass
			else:
				proj[lang][kind]["id"].append(Id)
		else:
			proj[lang] = {}
			proj[lang]["New"] = {}
			proj[lang]["BounceBack"] = {}
			proj[lang]["Submit"] = {}
			proj[lang]["LocQA"] = {}
			proj[lang]["MisComponent"] = {}
			proj[lang]["Closed"] = {}
			proj[lang]["New"]["count"] = 0
			proj[lang]["BounceBack"]["count"] = 0
			proj[lang]["Submit"]["count"] = 0
			proj[lang]["LocQA"]["count"] = 0
			proj[lang]["MisComponent"]["count"] = 0
			proj[lang]["Closed"]["count"] = 0
			proj[lang]["New"]["id"] = []
			proj[lang]["BounceBack"]["id"] = []
			proj[lang]["Submit"]["id"] = []
			proj[lang]["LocQA"]["id"] = []
			proj[lang]["MisComponent"]["id"] = []
			proj[lang]["Closed"]["id"] = []
			proj[lang][kind]["count"] = 1
			proj[lang][kind]["id"].append(Id)
	return proj

def getProjDict2(arr,fromdate,todate):
	proj={}
	for aa in arr:
		Id = str(aa[0])
		lang = str(aa[1])
		kind = aa[2]
		time = aa[3]
		if time >= fromdate and time <= todate:
			if lang in proj.keys():
				proj[lang][kind]["count"] += 1
				if Id in proj[lang][kind]["id"]:
					pass
				else:
					proj[lang][kind]["id"].append(Id)
			else:
				proj[lang] = {}
				proj[lang]["New"] = {}
				proj[lang]["BounceBack"] = {}
				proj[lang]["Submit"] = {}
				proj[lang]["LocQA"] = {}
				proj[lang]["MisComponent"] = {}
				proj[lang]["Closed"] = {}
				proj[lang]["New"]["count"] = 0
				proj[lang]["BounceBack"]["count"] = 0
				proj[lang]["Submit"]["count"] = 0
				proj[lang]["LocQA"]["count"] = 0
				proj[lang]["MisComponent"]["count"] = 0
				proj[lang]["Closed"]["count"] = 0
				proj[lang]["New"]["id"] = []
				proj[lang]["BounceBack"]["id"] = []
				proj[lang]["Submit"]["id"] = []
				proj[lang]["LocQA"]["id"] = []
				proj[lang]["MisComponent"]["id"] = []
				proj[lang]["Closed"]["id"] = []
				proj[lang][kind]["count"] = 1
				proj[lang][kind]["id"].append(Id)
	return proj

# 返回字典，带有语言，数量，bugID等的集合
def getCountAndDetailFromDaily(project,fromdate="all",todate="all",table="DailyActive"):
	db = sqlite3.connect(dbpath)
	cursor = db.cursor()
	proj = {}
	command = getSqlComponentCommand(project)
	sql = "select RadarID,Version,Kind,LastModifiedAt from %s where %s"%(table,command)
	cursor.execute(sql)
	arr = cursor.fetchall()
	if fromdate == "all" or todate == "all":
		proj = getProjDict(arr)
	else:
		proj = getProjDict2(arr,fromdate,todate)
	db.close()
	langlist = sorted(proj.keys())
	newcount = []
	bouncebackcount = []
	submitcount = []
	closecount = []
	locQAcount = []
	miscomponentcount = []
	newlist = []
	bouncebacklist = []
	submitlist = []
	closelist = []
	locQAlist = []
	miscomponentlist = []
	newtotal = 0
	bouncebacktotal= 0 
	submittotal = 0
	closetotal = 0
	locQAtotal = 0
	miscomponenttotal = 0
	newbugs = ""
	bouncebackbugs = ""
	submitbugs = ""
	closebugs = ""
	locQAbugs = ""
	miscomponentbugs = ""
	for aa in langlist:
		newcount.append(proj[aa]["New"]["count"])
		bouncebackcount.append(proj[aa]["BounceBack"]["count"])
		submitcount.append(proj[aa]["Submit"]["count"])
		closecount.append(proj[aa]["Closed"]["count"])
		locQAcount.append(proj[aa]["LocQA"]["count"])
		miscomponentcount.append(proj[aa]["MisComponent"]["count"])
		if len(proj[aa]["New"]["id"]) != 0:
			newlist.append("radar://problem/"+"&".join(proj[aa]["New"]["id"]))
		else:
			newlist.append("")
		if len(proj[aa]["BounceBack"]["id"]) != 0:
			bouncebacklist.append("radar://problem/"+"&".join(proj[aa]["BounceBack"]["id"]))
		else:
			bouncebacklist.append("")
		if len(proj[aa]["Submit"]["id"]) != 0:
			submitlist.append("radar://problem/"+"&".join(proj[aa]["Submit"]["id"]))
		else:
			submitlist.append("")
		if len(proj[aa]["Closed"]["id"]) != 0:
			closelist.append("radar://problem/"+"&".join(proj[aa]["Closed"]["id"]))
		else:
			closelist.append("")
		if len(proj[aa]["LocQA"]["id"]) != 0:
			locQAlist.append("radar://problem/"+"&".join(proj[aa]["LocQA"]["id"]))
		else:
			locQAlist.append("")
		if len(proj[aa]["MisComponent"]["id"]) != 0:
			miscomponentlist.append("radar://problem/"+"&".join(proj[aa]["MisComponent"]["id"]))
		else:
			miscomponentlist.append("")
		newtotal += proj[aa]["New"]["count"]
		bouncebacktotal += proj[aa]["BounceBack"]["count"]
		submittotal += proj[aa]["Submit"]["count"]
		closetotal += proj[aa]["Closed"]["count"]
		locQAtotal += proj[aa]["LocQA"]["count"]
		miscomponenttotal += proj[aa]["MisComponent"]["count"]
		if len(proj[aa]["New"]["id"])!=0:
			if newbugs == "":
				newbugs = "radar://problem/" + "&".join(proj[aa]["New"]["id"])
			else:
				newbugs = newbugs + "&" + "&".join(proj[aa]["New"]["id"])
		if len(proj[aa]["BounceBack"]["id"])!=0:
			if bouncebackbugs == "":
				bouncebackbugs = "radar://problem/" + "&".join(proj[aa]["BounceBack"]["id"])
			else:
				bouncebackbugs = bouncebackbugs + "&" + "&".join(proj[aa]["BounceBack"]["id"])
		if len(proj[aa]["Submit"]["id"])!=0:
			if submitbugs == "":
				submitbugs = "radar://problem/" + "&".join(proj[aa]["Submit"]["id"])
			else:
				submitbugs = submitbugs + "&" + "&".join(proj[aa]["Submit"]["id"])
		if len(proj[aa]["Closed"]["id"])!=0:
			if closebugs == "":
				closebugs = "radar://problem/" + "&".join(proj[aa]["Closed"]["id"])
			else:
				closebugs = closebugs + "&" + "&".join(proj[aa]["Closed"]["id"])
		if len(proj[aa]["LocQA"]["id"])!=0:
			if locQAbugs == "":
				locQAbugs = "radar://problem/" + "&".join(proj[aa]["LocQA"]["id"])
			else:
				locQAbugs = locQAbugs + "&" + "&".join(proj[aa]["LocQA"]["id"])
		if len(proj[aa]["MisComponent"]["id"])!=0:
			if miscomponentbugs == "":
				miscomponentbugs = "radar://problem/" + "&".join(proj[aa]["MisComponent"]["id"])
			else:
				miscomponentbugs = miscomponentbugs + "&" + "&".join(proj[aa]["MisComponent"]["id"])

	projectdetialsstr = ""
	#0 的不显示
	for i in range(len(langlist)):
		detials = getbc(newlist[i], 'New') + getbc(bouncebacklist[i], 'BounceBack') + getbc(submitlist[i], 'Submit') + getbc(locQAlist[i], 'LocQA') + getbc(miscomponentlist[i], 'MisComponent') + getbc(closelist[i], 'Close')
		if detials != '':
		    if(i == (len(langlist) - 1)):
				projectdetialsstr = projectdetialsstr + '<details open><summary>' + langlist[i] + '</summary>' + detials + '</details>'
		    else:
				projectdetialsstr = projectdetialsstr + '<details open><summary>' + langlist[i] + '</summary>' + detials + '</details><br>'
	#print projectdetialsstr
	dailyactive = "<details open><summary><font size=2 face=\"Helvetica\">Daily Activity</summary>New - <a href=\"%s\">%s</a> BounceBack - <a href=\"%s\">%s</a> Submit - <a href=\"%s\">%s</a> LocQA - <a href=\"%s\">%s</a> MisComponent - <a href=\"%s\">%s</a> Closed - <a href=\"%s\">%s</a>"%(newbugs,newtotal,bouncebackbugs,bouncebacktotal,submitbugs,submittotal,locQAbugs,locQAtotal,miscomponentbugs,miscomponenttotal,closebugs,closetotal)
	miscomponentbugslist = "MisComponent&nbsp;Bugs：<a href=\"%s\">%s</a><br/>"%(miscomponentbugs,miscomponentbugs)
	return {"langlist":langlist,'newlist':newcount, 'bouncebacklist':bouncebackcount, 'submitlist':submitcount, 'locQAlist':locQAcount, 'miscomponentlist':miscomponentcount, 'closelist':closecount},miscomponentbugslist,{"langlist":langlist,'newlist':newlist, 'bouncebacklist':bouncebacklist, 'submitlist':submitlist, 'locQAlist':locQAlist, 'miscomponentlist':miscomponentlist, 'closelist':closelist,'projectdetialsstr':projectdetialsstr},dailyactive

def getbc(bugs, kind):
	bugs = str(bugs)
	c = 0 
	if bugs == '':
	    c = 0    
	    return ''
	else:
	    c = bugs.count('&') + 1
	    return '%s(%s)：<a href="%s">%s</a><br>'%(kind, c, bugs, bugs)

# print getCountAndDetailFromDaily("OSX","2011-02-27","2016-01-01")


# 功能：获得count表的数量信息
# table：数据库表名
# project：component的名字
# 返回：数据字典
def getCountFromCount(project,table="DailyCount"):
	db = sqlite3.connect(dbpath)
	cursor = db.cursor()
	sql = "select AnalyzeCount,VerifyCount,BuildCount,IntegrateCount,LastModifiedAt from %s where Component='%s'"%(table,project)
	cursor.execute(sql)
	arr = cursor.fetchall()
	dataDict = {}
	for aa in arr:
		analyze = aa[0]
		verify = aa[1]
		build = aa[2]
		integrate = aa[3]
		total = analyze + verify + build +integrate
		time = str(aa[4])
		if time in dataDict.keys():
			dataDict[time]["analyze"] += analyze
			dataDict[time]["verify"] += verify
			dataDict[time]["build"] += build
			dataDict[time]["integrate"] += integrate
			dataDict[time]["total"] += total
		else:
			dataDict[time] = {}
			dataDict[time]["analyze"] = analyze
			dataDict[time]["verify"] = verify
			dataDict[time]["build"] = build
			dataDict[time]["integrate"] = integrate
			dataDict[time]["total"] = total

	timelist = sorted(dataDict.keys())
	analyzecount = []
	verifycount = []
	buildcount = []
	integratecount = []
	totalcount = []
	for bb in timelist:
		analyzecount.append(dataDict[bb]["analyze"])
		verifycount.append(dataDict[bb]["verify"])
		buildcount.append(dataDict[bb]["build"])
		integratecount.append(dataDict[bb]["integrate"])
		totalcount.append(dataDict[bb]["total"])
	db.close()
	return {'timelist':timelist,'analyze':analyzecount,'verify':verifycount,'build':buildcount,'integrate':integratecount,'total':totalcount,}

# print getCountFromCount("OSX")

def getKeyWordsFromAssignee(table="WitsAssignee"):
	return RadarArgs.keywords + ['Others']


def getMaxAndMinDayFromAssignee(project,table="WitsAssignee"):
	langlist = getDateList(project,table)
	if len(langlist) >= 1:
		max = langlist[len(langlist)-1]
		min = langlist[0]
		return max,min
	else:
		return "",""

# print getMaxAndMinDayFromAssignee("OSX")

def getWeekList(project,table="WitsAssignee"):
	max,min = getMaxAndMinDayFromAssignee(project,table)
	if max == "" or min == "":
		return
	else:
		maxday = datetime.datetime.strptime(max,"%Y-%m-%d").date()
		minday = datetime.datetime.strptime(min,"%Y-%m-%d").date()
		first = minday.weekday()
		last = maxday.weekday()
		weeks = []
		start = minday-datetime.timedelta(days=first)
		end = maxday+datetime.timedelta(days=6-last)
		temp = str(end - start)[0:str(end-start).find(" ")]
		if int(temp) == 6:
			weeks.append(str(start)+"~"+str(end))
			return weeks
		else:
			startday = start
			endday = startday + datetime.timedelta(days=6)
			while str(endday)!=str(end + datetime.timedelta(days=7)):
				# print startday,endday
				weeks.append(str(startday)+"~"+str(endday))
				startday = endday + datetime.timedelta(days=1)
				endday = startday + datetime.timedelta(days=6)
			return weeks

# print getWeekList("OSX")

def getCurrentWeek():
	curtime = time.strftime('%Y-%m-%d',time.localtime(time.time()))
	curdate = datetime.datetime.strptime(curtime,"%Y-%m-%d").date()
	whichdate = curdate.weekday()
	startday = curdate - datetime.timedelta(days=whichdate)
	endday = curdate +datetime.timedelta(days=6-whichdate)
	current = str(startday) + "~" +str(endday)
	return current

# getCurrentWeek()

def getDataFromAssignee(arr,fromtodate):
	fromdate = ""
	todate = ""
	Keys = getKeyWordsFromAssignee()
	if fromtodate == "current":
		temp = getCurrentWeek()
		fromdate,todate = temp.split("~")[0],temp.split("~")[1]
	else:
		fromdate,todate = fromtodate.split("~")[0],fromtodate.split("~")[1]
	dataDict = {}
	for aa in arr:
		ID = str(aa[0])
		lang = str(aa[1])
		keyword = str(aa[2])
		time = str(aa[3])
		if time >= fromdate and time <= todate:
			if lang in dataDict.keys() and keyword in Keys:
				dataDict[lang][keyword]["count"] += 1
				if ID in dataDict[lang][keyword]["id"]:
					pass
				else:
					dataDict[lang][keyword]["id"].append(ID)
			if lang not in dataDict.keys() and keyword in Keys:
				dataDict[lang] = {}
				for bb in Keys:
					dataDict[lang][bb] = {}
					dataDict[lang][bb]["count"] = 0
					dataDict[lang][bb]["id"] = []
				dataDict[lang][keyword]["count"] = 1
				dataDict[lang][keyword]["id"].append(ID)
	return dataDict

def getCountAndDetailFromAssignee(project,fromtodate="current",table="WitsAssignee"):
	db = sqlite3.connect(dbpath)
	cursor = db.cursor()
	command = getSqlComponentCommand(project)
	sql = "select RadarID,Version,Keyword,LastModifiedAt from %s where %s"%(table,command)
	cursor.execute(sql)
	arr = cursor.fetchall()
	db.close()
	dataDict = {}
	dataDict = getDataFromAssignee(arr,fromtodate)
	langlist = sorted(dataDict.keys())
	autocount = []
	translationcount = []
	layoutcount = []
	otherscount = []
	locFunccount = []
	engineercount = []
	autolist = []
	translationlist = []
	layoutlist = []
	otherslist = []
	locFunclist = []
	engineerlist = []
	for aa in langlist:
		autocount.append(dataDict[aa]["AutoLoc [Investigate]"]["count"])
		translationcount.append(dataDict[aa]["Category [Translation]"]["count"])
		layoutcount.append(dataDict[aa]["Category [HI/Layout]"]["count"])
		otherscount.append(dataDict[aa]["Others"]["count"])
		locFunccount.append(dataDict[aa]["Category [LocFunctional]"]["count"])
		engineercount.append(dataDict[aa]["Category [TransEngineering]"]["count"])
		if len(dataDict[aa]["AutoLoc [Investigate]"]["id"]) == 0:
			autolist.append("")
		else:
			temp = "radar://problem/" + "&".join(dataDict[aa]["AutoLoc [Investigate]"]["id"])
			autolist.append(temp)
		if len(dataDict[aa]["Category [Translation]"]["id"]) == 0:
			translationlist.append("")
		else:
			temp = "radar://problem/" + "&".join(dataDict[aa]["Category [Translation]"]["id"])
			translationlist.append(temp)
		if len(dataDict[aa]["Category [HI/Layout]"]["id"]) == 0:
			layoutlist.append("")
		else:
			temp = "radar://problem/" + "&".join(dataDict[aa]["Category [HI/Layout]"]["id"])
			layoutlist.append(temp)
		if len(dataDict[aa]["Others"]["id"]) == 0:
			otherslist.append("")
		else:
			temp = "radar://problem/" + "&".join(dataDict[aa]["Others"]["id"])
			otherslist.append(temp)
		if len(dataDict[aa]["Category [LocFunctional]"]["id"]) == 0:
			locFunclist.append("")
		else:
			temp = "radar://problem/" + "&".join(dataDict[aa]["Others"]["id"])
			locFunclist.append(temp)
		if len(dataDict[aa]["Category [TransEngineering]"]["id"]) == 0:
			engineerlist.append("")
		else:
			temp = "radar://problem/" + "&".join(dataDict[aa]["Others"]["id"])
			engineerlist.append(temp)
	
	return {"Language":langlist,"LocFunc":locFunccount,"AutoLoc":autocount,"Translation":translationcount,"Layout":layoutcount,"Engineer":engineercount,"Others":otherscount},{"Language":langlist,"LocFunc":locFunclist,"AutoLoc":autolist,"Translation":translationlist,"Layout":layoutlist,"Engineer":engineerlist,"Others":otherslist}


# print getCountAndDetailFromAssignee("OSX","2011-01-01~2016-01-01")

