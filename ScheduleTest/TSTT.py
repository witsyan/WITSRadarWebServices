#!/usr/bin/env python
#coding=utf-8

__author__ = 'Tinyliu@wistronits.com, tinyliu@me.com'

import subprocess, re, simplejson, os, sys, time, datetime
reload(sys) 
sys.setdefaultencoding('utf-8')

class TSTT:
	sDate = ''
	eDate = ''
	project = ''
	QACycle = ''
	def __init__(self, TSTTFolder):
		self.schedules = {}
		self.id = os.path.basename(TSTTFolder)
		for file in os.listdir(TSTTFolder):
			if file.isdigit():
				scheduleDict = self.readLocFilebyID(os.path.join(TSTTFolder, file))
				schedule = self.scheduleAnalyze(scheduleDict)
				lang = schedule[-1]
				if lang not in self.schedules:
					self.schedules[lang] = ', '.join(schedule[-4:-1])
				if not self.sDate:
					self.sDate, self.eDate, self.project, self.QACycle = schedule[:4]
		self.percentage = self.totalPercentage()
		if scheduleDict['status'] == 'Complete':
			self.percentage += 'C'

	def readLocFilebyID(self, locFile):
		contents = open(locFile).read()
		return simplejson.loads(contents)

	def formatToMins(self, expectedTime):
		h, m, s = expectedTime.split(':')
		return int(h) * 60 + int(m) + int(s)/60

	def scheduleAnalyze(self, scheduleDict):
		sDate = scheduleDict['scheduledStartDate']
		eDate = scheduleDict['scheduledStartDate']
		# if sDate < '2014-11-10':
		# 	return ('0', '0', '0', '0', '0', '0', '0', '0')
		lang = scheduleDict['component']['version']
		projectInfo = re.findall('\[[\w\W]*?\]', scheduleDict['title'])
		if len(projectInfo) == 2:
			project, locQACycle = projectInfo
		else:
			project = '[%s]'%scheduleDict['component']['name'][9:]
			locQACycle = scheduleDict['title'][scheduleDict['title'].lower().rfind('locqa'):]
			locQACycle = locQACycle if len(locQACycle) > 1 else '[Undefined]'
		PassedPercentage, relatedProblems = self.casesCalculater(scheduleDict['cases'])
		status = scheduleDict['status']
		return sDate, eDate, project, locQACycle, PassedPercentage, status, relatedProblems, lang

	def casesCalculater(self, casesList):
		totalTimes = 0.0; PassTimes = 0.0; NoVauleTime = 0.0
		totalCases = len(casesList); PassCases = 0.0
		relatedProblems = ''
		for case in casesList:
			totalTimes += self.formatToMins(case['expectedTime'])
			if case['status'] == 'Pass' or case['status'] == 'N/A':
				PassTimes += self.formatToMins(case['expectedTime'])
				PassCases += 1

			if case['relatedProblems']:
				for bug in case['relatedProblems']:
					relatedProblems += '%s&'%bug['id']
		PassedPercentage = '%.2f%% Passed'%(PassCases/totalCases * 100)
		if relatedProblems:
			return PassedPercentage, 'rdar://problem/%s'%relatedProblems[:-1]
		return PassedPercentage, 'None'

	def totalPercentage(self):
		p = []; total = 0.0
		for i in self.schedules.values():
			total += float(i.split('%')[0])
		return '%.2f%%'%(total/len(self.schedules.values()))

def getTSTTList(folder):
	TSTTList = []
	for projFolder in os.listdir(folder):
		_TestSuite = '%s/%s/_TestSuite'%(folder, projFolder)
		if os.path.isdir(_TestSuite):
			for file in os.listdir(_TestSuite):
				if file.isdigit():
					TSTTList.append(os.path.join(_TestSuite, file))
	return TSTTList

def weekToDate(week=0): #0 表示本周 ，－1 表示上一周，会根据输入的数字返回对应星期周一到周日的日期（2015-03-12）
	today = today = datetime.date.today()
	Mon = today + datetime.timedelta(days=7*week-today.weekday())
	Tue = Mon + datetime.timedelta(days=1)
	Wed = Mon + datetime.timedelta(days=2)
	Thurs = Mon + datetime.timedelta(days=3)
	Fri = Mon + datetime.timedelta(days=4)
	Sat = Mon + datetime.timedelta(days=5)
	Sun = Mon + datetime.timedelta(days=6)
	return Mon.isoformat(), Tue.isoformat(), Wed.isoformat(), Thurs.isoformat(), Fri.isoformat(), Sat.isoformat(), Sun.isoformat()

def dateToWeek(date, weekly=0): # 0: this week, 1: 1 week later, -1: 1 week early
	today = datetime.date.today() + datetime.timedelta(days=7*weekly)
	for n in range(7):
		week = today + datetime.timedelta(days=n-today.weekday())
		if date[:10] == week.isoformat():
			return n
	# Monday = today + datetime.timedelta(days=0-today.weekday())

def TSTTDetial(scheduleDict):
	r = ''
	for key in scheduleDict:
		r += '%s %s\n'%(key, scheduleDict[key])
	return r

TSTTpath = os.path.dirname(__file__)[:-12] + '_LocProjScanner/_ScheduleProjects'

def projList(folder=TSTTpath, weekly=0): # weekly 与 weekToDate() 中的 week 值对应，返回所选星期的 TSTT 项目，按照 0-6 排列
	listToDjango = []; tmpList = []
	TSTTs = getTSTTList(folder)
	for i in TSTTs:
		testSuite = TSTT(i)
		start = dateToWeek(testSuite.sDate, weekly)
		end = dateToWeek(testSuite.eDate, weekly)

		if testSuite.project not in tmpList and start != None:
			tmpList.append(testSuite.project)
			listToDjango.append([[0, 6, 1, testSuite.project]])
			listToDjango[-1].append([start,
						end,
						0,
						testSuite.QACycle,
						testSuite.percentage,
						testSuite.id,
						TSTTDetial(testSuite.schedules)])
		elif start != None:
			locate = tmpList.index(testSuite.project)
			listToDjango[locate][0][2] += 1
			listToDjango[locate].append([start,
						end,
						len(listToDjango[locate]) - 1,
						testSuite.QACycle,
						testSuite.percentage,
						testSuite.id,
						TSTTDetial(testSuite.schedules)])
	return listToDjango

def singleTestSuite(TSTTid, folder=TSTTpath):
	for dir in os.listdir(folder):
		if os.path.isdir('%s/%s/_TestSuite/%s'%(folder, dir, TSTTid)):
			testSuite = TSTT('%s/%s/_TestSuite/%s'%(folder, dir, TSTTid))
			return testSuite.project, testSuite.QACycle, testSuite.id, TSTTDetial(testSuite.schedules)

# s = TSTT('/Volumes/ProjectsHD/TinyTools/RadarWebService/newMethod_6_Append/_ScheduleProjects/OSX/_TestSuite/778363')

# print s.project, s.QACycle, s.sDate[:10], s.eDate[:10], s.percentage
# print TSTTDetial(s.schedules)