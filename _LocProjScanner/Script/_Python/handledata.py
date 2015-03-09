#!/usr/bin/env python
#coding=utf-8

import sqlite3
import os,sys
import json
import time
import datetime

def createtable(dbpath, flag, table='LocBugs'):#创建表
	db = sqlite3.connect(dbpath)
	cursor = db.cursor()
	sql = ""
	if flag == 2:
		sql = '''create table if not exists %s(
		id integer primary key autoincrement,
		Component varchar(100),
		AnalyzeCount int,
		VerifyCount int,
		BuildCount int,
		IntegrateCount int,
		LastModifiedAt date
		)
		'''%table
	elif flag == 1:
		sql = '''create table if not exists %s(
		RadarID int primary key,
		Component varchar(100),
		Title varchar(300),
		Version varchar(50),
		Priority int,
		Substate varchar(50),
		Classification varchar(50),
		Assignee varchar(100),
		State varchar(50),
		Milestone varchar(50),
		FixOrder int,
		Fingerprint varchar(50),
		LastModifiedAt datetime
		)
		''' % table
	elif flag == 0:
		sql = '''create table if not exists %s(
		id integer primary key autoincrement,
		RadarID int,
		Component varchar(100),
		Title varchar(300),
		Version varchar(50),
		Priority int,
		State varchar(50),
		Milestone varchar(100),
		Kind varchar(100),
		LastModifiedAt date
		)
		''' % table
	elif flag == -1:
		sql = '''create table if not exists %s(
		RadarID int primary key,
		Component varchar(100),
		Title varchar(300),
		Version varchar(50),
		Priority int,
		State varchar(50),
		Milestone varchar(100),
		Keyword varchar(100),
		LastModifiedAt date
		)
		''' % table
	cursor.execute(sql)
	db.commit()
	db.close()

def insertdata(dbpath, bugdict, table='LocBugs'):
	try:
		db = sqlite3.connect(dbpath)
		cursor = db.cursor()
		bugdict["title"] = bugdict["title"].replace("\'","\'\'")
		sql = "insert into %s values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(
			table,
			bugdict["id"],
			bugdict["component"],
			bugdict["title"],
			bugdict["version"],
			bugdict["priority"],
			bugdict["substate"],
			bugdict["classification"],
			bugdict["assignee"],
			bugdict["state"],
			bugdict["milestone"],
			bugdict["fixOrder"],
			bugdict["fingerprint"],
			bugdict["lastModifiedAt"])
		cursor.execute(sql)
		db.commit()
		db.close()
	except:
		print '## Already exists: %s'%(bugdict["id"])

def updatedata(dbpath, bugdict, table='LocBugs'):
	db = sqlite3.connect(dbpath)
	cursor = db.cursor()
	bugdict["title"] = bugdict["title"].replace("\'","\'\'")
	sql = "update %s set Component='%s',Title='%s',Version='%s',Priority='%s',Substate='%s',Classification='%s',Assignee='%s',State='%s',Milestone='%s',FixOrder='%s',Fingerprint='%s',LastModifiedAt='%s' where RadarID='%s'"%(
		table,
		bugdict["component"],
		bugdict["title"],
		bugdict["version"],
		bugdict["priority"],
		bugdict["substate"],
		bugdict["classification"],
		bugdict["assignee"],
		bugdict["state"],
		bugdict["milestone"],
		bugdict["fixOrder"],
		bugdict["fingerprint"],
		bugdict["lastModifiedAt"],
		bugdict["id"])
	cursor.execute(sql)
	db.commit()
	db.close()
	# print "update %s success"%bugdict["id"]

def updatedata2(dbpath, bugid, keyword, table='WitsAssignee'):
	db = sqlite3.connect(dbpath)
	cursor = db.cursor()
	sql = "update %s set Keyword='%s' where RadarID='%s'"%(
		table,
		keyword,
		bugid)
	cursor.execute(sql)
	db.commit()
	db.close()

def getDetailFromSql(dbpath, bugId, table='LocBugs'):
	db = sqlite3.connect(dbpath)
	cursor = db.cursor()
	try:
		getDataDict = {}
		sql = "select * from %s where RadarID=%s"%(table, bugId)
		cursor.execute(sql)
		dataArr = cursor.fetchall()
		getDataDict["id"] = dataArr[0][0]
		getDataDict["component"] = str(dataArr[0][1])
		getDataDict["title"] = str(dataArr[0][2])
		getDataDict["version"] = str(dataArr[0][3])
		getDataDict["priority"] = dataArr[0][4]
		getDataDict["substate"] = str(dataArr[0][5])
		getDataDict["classification"] = str(dataArr[0][6])
		getDataDict["assignee"] = str(dataArr[0][7])
		getDataDict["state"] = str(dataArr[0][8])
		getDataDict["milestone"] = str(dataArr[0][9])
		getDataDict["fixOrder"] = dataArr[0][10]
		getDataDict["fingerprint"] = str(dataArr[0][11])
		getDataDict["lastModifiedAt"] = str(dataArr[0][12])
		return getDataDict
	except:
		return

def getcurrent():
	curtime = time.strftime('%Y-%m-%d',time.localtime(time.time()))
	return curtime

def returnKeyValues(dicts, key1='', key2='', key3=''):
	try:
		if key3:
			return dicts[key1][key2][key3]
		elif key2:
			return dicts[key1][key2]
		else:
			return dicts[key1]
	except:
		return 'null'

def handleOneData(radarDict):#将数据格式化
	dataDict = {}
	# if isinstance(radarDict, int):
	# 	return {'id':radarDict}
	dataDict['id'] = returnKeyValues(radarDict, key1='id')
	dataDict['title'] = returnKeyValues(radarDict, key1='title').replace('\'', '"')
	dataDict['state'] = returnKeyValues(radarDict, key1='state')
	dataDict['substate'] = str(returnKeyValues(radarDict, key1='substate'))
	dataDict['component'] = returnKeyValues(radarDict, key1='component', key2='name')
	dataDict['version'] = returnKeyValues(radarDict, key1='component', key2='version')
	dataDict['milestone'] = returnKeyValues(radarDict, key1='milestone', key2='name')
	dataDict['assignee'] = '%s %s'%(returnKeyValues(radarDict, key1='assignee', key2='firstName'),
		returnKeyValues(radarDict, key1='assignee', key2='lastName'))
	dataDict['priority'] = returnKeyValues(radarDict, key1='priority')
	dataDict['fixOrder'] = returnKeyValues(radarDict, key1='fixOrder')
	dataDict['classification'] = returnKeyValues(radarDict, key1='classification')
	dataDict['fingerprint'] = returnKeyValues(radarDict, key1='fingerprint')
	dataDict['lastModifiedAt'] = returnKeyValues(radarDict, key1='lastModifiedAt')
	dataDict['assignee'] = dataDict['assignee'].replace('\'', '\'\'')
	return dataDict

def handleDataToAllTable(dbpath, nowdict, table='LocBugs'):
	now = handleOneData(nowdict)
	org = getDetailFromSql(dbpath, now['id'], table)
	if now['id'] == 'Closed':
		return now, org
	if org:
		if now != org:
			updatedata(dbpath, now, table)
		return now, org
	else:
		insertdata(dbpath, now, table)
		return now, {}

def getallIDfromSql(dbpath, project='OSX', state="all", table='LocBugs'):
	idArr = []
	components = "Loc:Proj:"+project
	db = sqlite3.connect(dbpath)
	cursor = db.cursor()
	sql=""
	if state=="all":
		sql = "select distinct RadarID from %s where Component='%s'" % (table, components)
	else:
		sql="select distinct RadarID from %s where Component='%s' and State='%s'"%(table, components, state)
	cursor.execute(sql)
	ids = cursor.fetchall()
	for aa in ids:
		idArr.append(aa[0])
	db.close()
	return idArr

def getallIDfromSql2(dbpath, project='OSX', state="all", table='WitsAssignee'):
	idArr = []
	components = "Loc:Proj:"+project
	db = sqlite3.connect(dbpath)
	cursor = db.cursor()
	sql=""
	if state=="all":
		sql = "select distinct RadarID from %s where Component='%s'" % (table, components)
	else:
		sql="select distinct RadarID from %s where Component='%s' and Keyword='%s'"%(table, components, state)
	cursor.execute(sql)
	ids = cursor.fetchall()
	for aa in ids:
		idArr.append(aa[0])
	db.close()
	return idArr

def getAllID(dbpath, state="all", table='LocBugs'):
	idArr = []
	db = sqlite3.connect(dbpath)
	cursor = db.cursor()
	if state=="all":
		sql = "select distinct RadarID from %s"%table
	else:
		sql="select distinct RadarID from %s where State='%s'"%(table, state)
	cursor.execute(sql)
	ids = cursor.fetchall()
	for aa in ids:
		idArr.append(aa[0])
	db.close()
	return idArr

def deleteDataFromSql(dbpath, bugID, table='LocBugs'):
	try:
		db = sqlite3.connect(dbpath)
		cursor = db.cursor()
		sql = "delete from %s where RadarID='%s'"%(table, bugID)
		cursor.execute(sql)
		db.commit()
		db.close()
		return bugID
	except:
		return '## Delete Faild: %s'%bugID

def checkIfExistsInDaily(dbpath, data, kind, time, table='DailyActive'):
	db = sqlite3.connect(dbpath)
	cursor = db.cursor()
	sql = "select count(*) from %s where RadarID='%s' and Kind='%s' and LastModifiedAt='%s'"%(table,data["id"],kind,time)
	cursor.execute(sql)
	arr = cursor.fetchall()
	result = arr[0][0]
	db.close()
	if result == 0:
		return 0
	else:
		return 1

def handleDataToDailyTable(dbpath, dataDict, kind, table='DailyActive', firstKey='null,'):
	curtime = getcurrent()
	# flag = checkIfExistsInDaily(dbpath, dataDict, kind, curtime, table)
	try:
		db = sqlite3.connect(dbpath)
		cursor = db.cursor()
		sql = "insert into %s values(%s'%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(
			table,
			firstKey,
			dataDict["id"],
			dataDict["component"],
			dataDict["title"],
			dataDict["version"],
			dataDict["priority"],
			dataDict["state"],
			dataDict["milestone"],
			kind,
			curtime)
		cursor.execute(sql)
		db.commit()
		db.close()
	except:
		# print '## Already exists: %s'%dataDict["id"]
		pass

def checkIfExistsInCount(dbpath, data, date, table='DailyCount'):
	db = sqlite3.connect(dbpath)
	cursor = db.cursor()
	sql = "select count(*) from %s where Component='%s' and LastModifiedAt='%s'"%(
		table,
		data["component"],
		date)
	cursor.execute(sql)
	arr = cursor.fetchall()
	result = arr[0][0]
	db.close()
	if result == 0:
		return 0
	else:
		return 1

def lastModifiedAt(advance=7):
	today = datetime.date.today()
	lastDays = today - datetime.timedelta(days=advance)
	return lastDays.isoformat()

def handleDataToCounttable(dbpath, dataDict, table='DailyCount'):
	curtime = lastModifiedAt(advance=1)
	flag = checkIfExistsInCount(dbpath, dataDict, curtime, table)
	if not flag:
		db = sqlite3.connect(dbpath)
		cursor = db.cursor()
		sql = "insert into %s values(null,'%s','%s','%s','%s','%s','%s')"%(
			table,
			dataDict["component"],
			dataDict["Analyze"],
			dataDict["Verify"],
			dataDict["Build"],
			dataDict["Integrate"],
			curtime)
		cursor.execute(sql)
		db.commit()
		db.close()
	else:
		print '## Already exists: %s'%dataDict["component"]

def getDbDate(dbpath):
	dailyArr = []
	countArr = []
	db = sqlite3.connect(dbpath)
	cursor = db.cursor()
	sql = "select RadarID,Component,Title,Version,Priority,State,Milestone,Kind,LastModifiedAt from DailyActive"
	cursor.execute(sql)
	dailyArr = cursor.fetchall()
	sql1 = "select Component,AnalyzeCount,VerifyCount,BuildCount,IntegrateCount,LastModifiedAt from DailyCount"
	cursor.execute(sql1)
	countArr = cursor.fetchall()
	db.close()
	return dailyArr,countArr

def exportOneToAnother(sourcedb,targetdb):
	db = sqlite3.connect(targetdb)
	cursor = db.cursor()
	sql1 = "drop table if exists DailyActive"
	cursor.execute(sql1)
	db.commit()
	sql2 = "drop table if exists DailyCount"
	cursor.execute(sql2)
	db.commit()
	createtable(targetdb,2,"DailyCount")
	createtable(targetdb,0,"DailyActive")
	dailyArr,countArr = getDbDate(sourcedb)
	for aa in countArr:
		sql3 = "insert into DailyCount values(null,'%s','%s','%s','%s','%s','%s')"%(aa[0],aa[1],aa[2],aa[3],aa[4],aa[5])
		cursor.execute(sql3)
		db.commit()
	for bb in dailyArr:
		bb[2] = bb[2].replace("\'","\'\'")
		sql4 = "insert into DailyActive values(null,'%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(bb[0],bb[1],bb[2],bb[3],bb[4],bb[5],bb[6],bb[7],bb[8])
		cursor.execute(sql4)
		db.commit()
	db.close()

# exportOneToAnother(sys.argv[1],sys.argv[2])
# createtable(sys.argv[1],"Radar_count",2)
# print len(getallIDfromSql(sys.argv[1],"Radar_allbug","OSX Updates","Verify"))
# print getDetailFromSql(sys.argv[1],"Radar_allbug",19348726)
# nowdict='{"lastModifiedAt": "2014-12-11T02:06:32+0000", "substate": "hehe", "classification": "Other Bug", "title": "[SUZin_PackageData]? TA:SUZinDisco12D76: Translation for string \'includes features and fixes that improve the...\' need to be improved.", "milestone": {"component": {"version": "TA", "name": "Loc:Proj:OSX Updates"}, "name": "LocDome"}, "component": {"version": "TA", "name": "Loc:Proj:OSX Updates"}, "priority": 3, "assignee": {"lastName": "Chen", "type": null, "email": null, "firstName": "Ryan", "dsid": 236393}, "state": "Analyze", "fingerprint": "b478e00d", "fixOrder": 6, "id": 133672081}'
# now=json.loads(nowdict)
# print handleDataToAllTable(sys.argv[1],"Radar_allbug",now)
# deleteDataFromSql(sys.argv[1],"Radar_allbug",19348726)
# dataDict={"id":"111","component":"222","title":"333","version":"444","priority":"555","state":"666","milestone":"777"}
# handleDataToDailyTable(sys.argv[1],"Radar_dailybug",dataDict,"NNN")
# dataDict={"component":"111","analyze":"222","verify":"333","build":"444","integrate":"555"}
# handleDataToCounttable(sys.argv[1],"Radar_count",dataDict)

