#!/usr/bin/env python
#coding=utf-8

__author__ = 'Tinyliu@wistronits.com, tinyliu@me.com'

import subprocess, re, simplejson, os, sys, time
reload(sys) 
sys.setdefaultencoding('utf-8')

pyScript = os.path.dirname(__file__)
projectFolder = pyScript[:pyScript.find('Script/_Python')] + '_ScheduleProjects'

def readLocFilebyID(locFile):
	contents = open(locFile).read()
	return simplejson.loads(contents)

def formatToMins(expectedTime):
	h, m, s = expectedTime.split(':')
	return int(h) * 60 + int(m) + int(s)/60

def casesCalculater(casesList):
	totalTimes = 0.0; PassTimes = 0.0; NoVauleTime = 0.0
	totalCases = len(casesList); PassCases = 0.0
	relatedProblems = ''
	for case in casesList:
		totalTimes += formatToMins(case['expectedTime'])
		if case['status'] == 'Pass' or case['status'] == 'N/A':
			PassTimes += formatToMins(case['expectedTime'])
			PassCases += 1

		if case['relatedProblems']:
			for bug in case['relatedProblems']:
				relatedProblems += '%s&'%bug['id']
	PassedPercentage = '%.2f%% Passed'%(PassCases/totalCases * 100)
	if relatedProblems:
		return PassedPercentage, 'rdar://problem/%s'%relatedProblems[:-1]
	return PassedPercentage, None
	# print 'Total: %s mins, finished: %s mins.'%(totalTimes, PassTimes)
	# rdar://problem/14189418&14200290&14388284

def scheduleAnalyze(scheduleDict):
	sDate = scheduleDict['scheduledStartDate']
	eDate = scheduleDict['scheduledStartDate']
	if sDate < '2014-11-10':
		return ('0', '0', '0', '0', '0', '0', '0', '0')
	lang = scheduleDict['component']['version']
	projectInfo = re.findall('\[[\w\W]*?\]', scheduleDict['title'])
	if len(projectInfo) == 2:
		project, locQACycle = projectInfo
	else:
		project = '[%s]'%scheduleDict['component']['name'][9:]
		locQACycle = scheduleDict['title'][scheduleDict['title'].lower().rfind('locqa'):]
		locQACycle = locQACycle if len(locQACycle) > 1 else '[Undefined]'
	# print scheduleDict['scheduledID']
	PassedPercentage, relatedProblems = casesCalculater(scheduleDict['cases'])
	status = scheduleDict['status']
	# print 'From %s To %s'%(sDate[:10], eDate[:10])
	# print project, locQACycle
	# print '- %s: %s, Filed Bugs: %s'%(lang, PassedPercentage, relatedProblems)
	return sDate, eDate, project, locQACycle, PassedPercentage, relatedProblems, lang, status

def suitesIntegrate(folder):
	schedules = []
	for file in os.listdir(folder):
		if file.isdigit():
			schedules.append(readLocFilebyID(os.path.join(folder, file)))
	sDate, eDate, project, locQACycle = scheduleAnalyze(schedules[0])[:4]
	if sDate == '0':
		return
	pjDetials = 'From %s To %s\n%s - %s\n'%(sDate[:10], eDate[:10], project, locQACycle)
	for dict in schedules:
		PassedPercentage, relatedProblems, lang, status = scheduleAnalyze(dict)[-4:]
		pjDetials += '- %s %s: %s, Bugs: %s\n'%(lang, status, PassedPercentage, relatedProblems)

	return pjDetials

date = ''
TestSuites = []
for file in os.listdir(projectFolder):
	projTestSuiteFolder = '%s/%s/_TestSuite'%(projectFolder, file)
	if os.path.isdir(projTestSuiteFolder):
		for file in os.listdir(projTestSuiteFolder):
			if file.isdigit():
				TestSuites.append('%s/%s'%(projTestSuiteFolder, file))

beforesort = []
for TestSuite in TestSuites:
	# print 'Processing %s ...'%os.path.basename(TestSuite)
		t = suitesIntegrate(TestSuite)
		if t:
			tmpdate = t.split('\n')[0]
			if tmpdate == date:
				beforesort.append(t[30:].replace('\n-', ' %s\n-'%os.path.basename(TestSuite), 1))
				# print t[30:].replace('\n-', ' %s\n-'%os.path.basename(TestSuite), 1)
			else:
				beforesort.append(t.replace('\n-', ' %s\n-'%os.path.basename(TestSuite), 1))
				# print t.replace('\n-', ' %s\n-'%os.path.basename(TestSuite), 1)
				date = tmpdate

beforesort.sort()
for i in beforesort:
	print i
