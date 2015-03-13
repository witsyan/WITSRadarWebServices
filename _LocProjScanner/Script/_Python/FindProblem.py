#!/usr/bin/env python
#coding=utf-8

__author__ = 'Tinyliu@wistronits.com, tinyliu@me.com'

import subprocess, re, simplejson, os, sys, time, datetime, requests, smtplib
reload(sys) 
sys.setdefaultencoding('utf-8')
sys.path.append(os.path.dirname(__file__))
import bodyRequest, handledata
from RadarArgs import RadarArgs
from email.mime.text import MIMEText

pyScript = os.path.dirname(__file__)
projectFolder = pyScript[:pyScript.find('Script/_Python')] + '_Projects'
shScript = pyScript[:pyScript.find('_Python')] + '_sh'

FindProblem = '%s/FindProblem.sh'%shScript
errorLogsFile = '%s/_errors.txt'%projectFolder

activeDB = '%s/activeDataBase.db'%projectFolder
try:
	os.makedirs(projectFolder)
except:
	pass
handledata.createtable(activeDB, 0, table='DailyActive')
handledata.createtable(activeDB, 2, table='DailyCount')
handledata.createtable(activeDB, -1, table='WitsAssignee')

coveredProj = RadarArgs.coveredProj # Loc:Proj:OSX Updates
languages = RadarArgs.languages # For multiProcess when more than 2000 bugs in single process
witsMembers = RadarArgs.witsMembers
keywords = RadarArgs.keywords

def mailtoLeaders(leaders, subject, content):
	msg = MIMEText(content)
	sender = 'tinyliu@wistronits.com'
	msg['Subject'] = subject
	msg['From'] = sender
	msg['To'] = leaders
	try:
		s = smtplib.SMTP('10.1.100.47')
		s.sendmail(sender, [leaders], msg.as_string())
		s.quit()
	except:
		pass

def useAPI(command, RequestBody='', ids=''): # use sh script to capture bugs from Radar web service
	response = subprocess.Popen('%s %s %s'%(command, RequestBody, ids), shell=True, stdout=subprocess.PIPE).stdout.read()
	if -1 < response.find('[') < response.find('{') or response.find('{') == -1:
		try:
			json = re.findall('\[[\w\W]+\]', response)[-1]
		except:
			t = ''
			if RequestBody:
				t = open(RequestBody).read()
			if re.findall('\[[\w\W]+\]', response):
				open(errorLogsFile, 'a').write('Date: %s\nRequestBody: %s\nids: %s\nContents(0): %s\n\n'%(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), t, ids, response))
			return []
	else:
		try:
			json = re.findall('\{[\w\W]+\}', response)[-1]
			if '409 Conflict' in json:
				open(errorLogsFile, 'a').write('Date: %s\nRequestBody: %s\nids: %s\nContents(1): %s\n\n'%(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), RequestBody, ids, json))
				return 'overflow'
			elif '401 Unauthorized' in json:
				print '\nRadar is unable to authenticate your account because IdMS has experienced an error.\n'
				print 'Please try to reset the password in %s.'%command
				# sys.exit()
				# return []
			print '## Dict Model:\n%s\n'%json
			mailtoLeaders('tinyliu@me.com', 'nRadar is unable to authenticate your account because IdMS has experienced an error.', '%s - %s\n%s'%(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), RequestBody, response))
			return []
		except IndexError, e:
			print '%s\n%s'%(e, response)
			t = ''
			if RequestBody:
				t = open(RequestBody).read()
			open(errorLogsFile, 'a').write('Date: %s\nRequestBody: %s\nids: %s\nContents(2): %s\n\n'%(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), t, ids, response))
			return []
	try:
		result = simplejson.loads(json)
	except:
		t = ''
		if RequestBody:
			t = open(RequestBody).read()
		open(errorLogsFile, 'a').write('Date: %s\nRequestBody: %s\nids: %s\nContents(3): %s\n\n'%(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), t, ids, json))
		return []
	if len(result) == 2000:
		return 'overflow'
	return result

def creatLocDir(locDir): # create forder if need
	try:
		os.makedirs(locDir)
	except:
		pass

def projectFrame(project): # singal proj frame
	if isinstance(project, dict):
		project = project.keys()[0]
	project = project.replace(' ', '_')
	projFolder = '%s/%s'%(projectFolder, project)
	creatLocDir(projFolder)
	dbFile = '%s/%s/%s.db'%(projectFolder, project, project)
	Logs = '%s/%s/_Logs.txt'%(projectFolder, project)
	return dbFile, projFolder, Logs

def creatRequestBodyFiles(Folder, contents=list): # requestBody.txt file for sh script
	fileList = []
	for n in range(len(contents)):
		requestBody = os.path.join(Folder, 'RequestBody_%s.txt'%n)
		open(requestBody, 'w').write(contents[n])
		fileList.append(requestBody)
	return fileList

def creatLogs(logFile, data, state='New'): # logs, obsolete
	try:
		currentTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
		f = open(logFile, 'a')
		f.write('%s - %s\n%s\n\n'%(currentTime, state, str(data)))
		f.close()
	except:
		print '## Log Faild!'

def multiProcess(proj, langs=[], ids=[], process=0): # to catpure bugs when more than 2000 in one proj
	splited = []; s = 0
	if langs:
		l = len(langs)
		splited = [langs[::4], langs[1::4], langs[2::4], langs[3::4]]
	if ids:
		s = 1
	while len(ids) > 1900:
		splited.append(ids[:1900])
		ids = ids[1900:]
	if ids:
		splited.append(ids)
	total = []; date = []
	projDB, projFolder, logs = projectFrame(proj)
	for list in splited:
		if s:
			date.append(bodyRequest.creatIDBodyRequest(proj, radarIDs=list))
		else:
			if process == 0:
				date.append(bodyRequest.creatBodyRequest(proj, langs=list)[0])
			else:
				stateList=['Analyze', 'Integrate', 'Build', 'Verify', 'Closed']
				date.append(bodyRequest.creatBodyRequest(proj, langs=list, stateList=stateList)[1])
	bodyFiles = creatRequestBodyFiles(projFolder, date)
	for file in bodyFiles:
		print '\n## MultiProcess: %s ...'%os.path.basename(projFolder)
		tmp = useAPI(FindProblem, RequestBody=file)
		if tmp:
			total += tmp
		else:
			print '\n\n## Empty content.\n'
			return []
		if os.path.isfile(file):
			os.remove(file)
	return total

def captureBugs(proj, ids=[], process=0): # bug list for each proj
	projDB, projFolder, logs = projectFrame(proj)
	handledata.createtable(projDB, 1)
	if ids:
		bodyModel = bodyRequest.creatIDBodyRequest(proj, radarIDs=ids)
		bodyFiles = creatRequestBodyFiles(projFolder, [bodyModel])
		print '\n## processing %s ...'%os.path.basename(projFolder)
		total = useAPI(FindProblem, bodyFiles[0])
		if total == 'overflow':
			total = multiProcess(proj, ids=ids)
	else:
		if process == 0:
			bodyModel = bodyRequest.creatBodyRequest(proj)[0]
		else:
			stateList=['Analyze', 'Integrate', 'Build', 'Verify', 'Closed']
			bodyModel = bodyRequest.creatBodyRequest(proj, stateList=stateList)[1]
		bodyFiles = creatRequestBodyFiles(projFolder, [bodyModel])
		print '\n## processing %s ...'%os.path.basename(projFolder)
		total = useAPI(FindProblem, bodyFiles[0])
		if total == 'overflow':
			total = multiProcess(proj, langs=languages, process=process)
	if os.path.isfile(bodyFiles[0]):
		os.remove(bodyFiles[0])
	return total, projDB

def activeCountDetial(projDB, DailyActiveDB, bugList, milestone='', firstRun=False):
	print '\nactiveCountDetial ...'
	if firstRun:
		for bug in bugList:
			handledata.handleDataToAllTable(projDB, bug)
		return
	for bug in bugList:
		new, org = handledata.handleDataToAllTable(projDB, bug)
		PMList = ['Paul Xie', 'Nancy Chen', 'Match Zeng', 'Jason Wu', 'Emily Wang', 'Asu2 Su', 'Chao Wu', 'Tiny Liu']
		for member in PMList:
			if member in new['assignee'] and new != org:
				handledata.handleDataToDailyTable(DailyActiveDB, new, 'Pending', table='WitsAssignee', firstKey='')
		if not org:
			if new['state'] != 'Closed':
				handledata.handleDataToDailyTable(DailyActiveDB, new, 'New')
				print 'New: %s'%new['id']
			else:
				handledata.deleteDataFromSql(projDB, new['id'])
		elif new['state'] != org['state']:
			if new['state'] == 'Analyze':
				handledata.handleDataToDailyTable(DailyActiveDB, new, 'BounceBack')
				print 'BounceBack: %s'%new['id']
			elif new['state'] == 'Verify':
				handledata.handleDataToDailyTable(DailyActiveDB, new, 'LocQA')
				print 'LocQA: %s'%new['id']
			elif new['state'] == 'Integrate' or new['state'] == 'Build':
				handledata.handleDataToDailyTable(DailyActiveDB, new, 'Submit')
				print 'Submit: %s'%new['id']
			elif new['state'] == 'Closed':
				handledata.handleDataToDailyTable(DailyActiveDB, new, 'Closed')
				handledata.deleteDataFromSql(projDB, new['id'])
				print 'Closed: %s'%new['id']
		elif new['state'] == 'Closed':
			handledata.deleteDataFromSql(projDB, new['id'])
	print 'Finished.'

def dailyCount(projDB, DailyActiveDB, proj):
	print '\ndailyCount ...'
	if isinstance(proj, dict):
		proj = proj.keys()[0]
	dateDict = {'component':proj}
	stateList = ['Analyze', 'Integrate', 'Build', 'Verify']
	for state in stateList:
		dateDict[state] = len(handledata.getAllID(projDB, state=state))
	print dateDict['component']
	for key in stateList:
		print '%s: %s'%(key, dateDict[key])
	handledata.handleDataToCounttable(DailyActiveDB, dateDict)
	print 'Finished.'

def activeCountIDs(projDB, DailyActiveDB, milestone=''):
	print '\nactiveCountIDs ...'
	currentRadarIDs = handledata.getAllID(projDB)
	activeRadarIDs, projDB = captureBugs(proj, ids=currentRadarIDs)
	if not activeRadarIDs:
		activeRadarIDs, projDB = captureBugs(proj, ids=currentRadarIDs)
	if not activeRadarIDs:
		mailtoLeaders('tinyliu@me.com', 'Radar Web Services Process Broken', '%s - %s'%(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), projDB))
		return
	print 'currentRadarIDs: %s, activeRadarIDs: %s'%(len(currentRadarIDs), len(activeRadarIDs))
	for ids in currentRadarIDs:
		if ids not in activeRadarIDs:
			bug = handledata.getDetailFromSql(projDB, ids)
			handledata.handleDataToDailyTable(DailyActiveDB, bug, 'MisComponent')
			handledata.deleteDataFromSql(projDB, bug['id'])
			print 'MisComponent: %s'%bug['id']
	print 'Finished.'

def witsActive(DailyActiveDB, proj, projKeyword):
	if proj != 'OSX':
		return
	try:
		totalRadarIDs = handledata.getallIDfromSql2(DailyActiveDB)
		htmlContent = requests.get('http://10.4.2.6/autolayout')
		ALbugs = re.findall('[0-9]{8,10}', htmlContent.content)
		for bug in totalRadarIDs:
			if str(bug) in ALbugs:
				handledata.updatedata2(DailyActiveDB, bug, 'AutoLoc [Investigate]')
	except:
		print '## Error Found when process Keywords classifcation!'

	currentRadarIDs = handledata.getallIDfromSql2(DailyActiveDB, state='Pending')
	if currentRadarIDs:
		bodyModel = bodyRequest.creatPersonalBodyRequest(currentRadarIDs, keywords=projKeyword)
		bodyFiles = creatRequestBodyFiles(os.path.dirname(DailyActiveDB), bodyModel)
		for n in range(len(projKeyword)):
			total = useAPI(FindProblem, bodyFiles[n])
			if os.path.isfile(bodyFiles[n]):
				os.remove(bodyFiles[n])
			for bug in total:
				handledata.updatedata2(DailyActiveDB, bug, projKeyword[n])
				if bug in currentRadarIDs:
					currentRadarIDs.remove(bug)
	for bug in currentRadarIDs:
		handledata.updatedata2(DailyActiveDB, bug, 'Others')

# witsActive(activeDB, 'OSX', keywords)

for proj in coveredProj:
	projDB, projFolder, logs = projectFrame(proj)
	if not os.path.isfile(projDB):
		print 'Creating Proj ...'
		allbugs, projDataBase = captureBugs(proj)
		print proj, len(allbugs)
		activeCountDetial(projDataBase, activeDB, allbugs, firstRun=True)
	else:
		print '\nPassing %s ...'%os.path.basename(projFolder)
		time.sleep(1)
		
today = datetime.date.today(); times = 1
sunday = today + datetime.timedelta(days=6-today.weekday())
while True:
	currentDay = datetime.date.today(); p = 0
	if  today == currentDay:
		p = 1
	if currentDay == sunday:
		sunday = currentDay + datetime.timedelta(days=7)
		witsActive(activeDB, 'OSX', keywords)

	for proj in coveredProj:
		print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
		projDB, projFolder, logs = projectFrame(proj)
		allbugs, projDataBase = captureBugs(proj, process=p)
		print proj, len(allbugs)
		activeCountDetial(projDataBase, activeDB, allbugs)
		if not p:
			print 'Processing DailyCount ...(0)'
			activeCountIDs(projDB, activeDB)
			dailyCount(projDB, activeDB, proj)
		elif times % 20 == 0:
			print 'Processing DailyCount ...(1)'
			activeCountIDs(projDB, activeDB)
			dailyCount(projDB, activeDB, proj)
		time.sleep(5)
	today = currentDay
	times += 1
	print '\n%s\nFinished, process will restart after 1 minutes.\n'%time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
	time.sleep(60)

# if not os.path.isfile(activeDB):
# 	creatLocDir(projectFolder)
# print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
# while True:
# 	runTest(coveredProj, activeDB)