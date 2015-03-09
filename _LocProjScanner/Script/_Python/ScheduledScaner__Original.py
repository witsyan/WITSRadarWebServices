#!/usr/bin/env python
#coding=utf-8

__author__ = 'Tinyliu@wistronits.com, tinyliu@me.com'

import subprocess, re, simplejson, os, sys, time, datetime
reload(sys) 
sys.setdefaultencoding('utf-8')

pyScript = os.path.dirname(__file__)

projectFolder = pyScript[:pyScript.find('Script/_Python')] + '_ScheduleProjects'

shScript = pyScript[:pyScript.find('_Python')] + '_sh'

FindScheduledTest = '%s/FindScheduledTest.sh'%shScript
GetScheduleTestDataCase = '%s/GetScheduleTestData.sh'%shScript

def creatLocDirs(locDirs):
	try:
		os.makedirs(locDirs)
	except:
		pass

def projectFrame(project):
	TestSuiteFolder = '%s/%s/_TestSuite'%(projectFolder, project)
	RequestBody = '%s/%s/_RequestBody'%(projectFolder, project)
	Logs = '%s/%s/_Logs'%(projectFolder, project)
	creatLocDirs(TestSuiteFolder)
	creatLocDirs(RequestBody)
	creatLocDirs(Logs)
	return TestSuiteFolder, RequestBody, Logs

def creatAsiaRequestBodyFiles(Folder, contents=list):
	fileList = []
	for n in range(len(contents)):
		requestBody = os.path.join(Folder, 'RequestBody_%s.txt'%n)
		open(requestBody, 'w').write(contents[n])
		fileList.append(requestBody)
	return fileList

def useAPI(command, requestBoday='', ScheduleID=''):
	response = subprocess.Popen('%s %s %s'%(command, requestBoday, ScheduleID), shell=True, stdout=subprocess.PIPE).stdout.read()
	if response.strip()[-1] == ']':
		try:
			json = re.findall('\[[\w\W]+\]', response)[-1]
		except:
			return []
	else:
		try:
			json = re.findall('\{[\w\W]+\}', response)[-1]
		except IndexError, e:
			print '%s\n%s'%(e, response)
			return
	return simplejson.loads(json)

def creatLocFilesbyID(ScheduledTest, targetFolder):
	TestSuite = os.path.join(targetFolder, str(ScheduledTest['suiteID']))
	if not os.path.isdir(TestSuite):
		os.mkdir(TestSuite)
		os.chdir(TestSuite)
	os.chdir(TestSuite)
	open(str(ScheduledTest['scheduledID']), 'w').write(simplejson.dumps(ScheduledTest))

def TestSuiteInfos(testSuiteFolder):
	ScheduleDetails = {}
	for file in os.listdir(testSuiteFolder):
		if file.isdigit():
			ScheduleContents = open(os.path.join(testSuiteFolder, file)).read()
			ScheduleDetails[file] = simplejson.loads(ScheduleContents)

def lastModifiedAt(advance=7):
	today = datetime.date.today()
	lastWeek = today - datetime.timedelta(days=advance)
	return lastWeek.isoformat()

times = 0
projList = ['ARD', 'OSX Updates', 'CPU', 'Final Cut Pro', 'Compressor', 'Motion', 'Spark',
	'Server OSX', 'iWork', 'Pages', 'Numbers', 'Keynote']

coveredProj = ['ARD', 'OSX', 'OSX Updates', 'Final Cut Pro', 'Compressor', 'Motion',
	'Pages', 'Numbers', 'Keynote', 'iWork', 'Spark', 'Server OSX', 'CPU', 'Logic',
	'iTunes Mac', 'iTunes Win', 'Aperture', 'iMovie', 'iBooks Author', 'iCloud CP Win', 'iPhoto',
	'ACUtil', 'MainStage', 'Safari Mac', 'iTunesProducer', 'QuickTime Mac', 'QuickTime Windows',
	'AirPort Mac', 'AirPort Win', 'Java'] # Loc:Proj:OSX Updates

while True:
	for proj in coveredProj:
		LocProj = 'Loc:Proj:%s'%proj
		RequestBodyComponents = {'component':[{'name':LocProj,'version':'CH'},
				{'name':LocProj,'version':"TA"},
				{'name':LocProj,'version':"KH"},
				{'name':LocProj,'version':"J"},
				{'name':LocProj,'version':"ID"},
				{'name':LocProj,'version':"VN"},
				{'name':LocProj,'version':"MY"}],
			'lastModifiedAt':{'gt':'2015-01-01T16:00:00'}}
		if times:
			RequestBodyComponents['lastModifiedAt']['gt'] = '%sT16:00:00'%lastModifiedAt()
		t, r, l = projectFrame(proj.replace(' ', '_'))
		b = creatAsiaRequestBodyFiles(r, [simplejson.dumps(RequestBodyComponents)])
		s = []
		for body in b:
			print '\n%s - %s ...'%(proj, os.path.basename(body))
			s += useAPI(FindScheduledTest, body)

		total = len(s)
		for unit in s:
			if total%10 == 0:
				time.sleep(5)
			scheduleFile = '%s/%s/%s'%(t, unit['suiteID'], unit['scheduledID'])
			print '\n%s left, processing %s/%s ...'%(total, unit['suiteID'], unit['scheduledID'])
			if os.path.isfile(scheduleFile):
				contents = open(scheduleFile).read()
				if '"status": "Complete"' not in contents:
					ScheduleCase = useAPI(GetScheduleTestDataCase, ScheduleID=unit['scheduledID'])
					try:
						unit["cases"] = ScheduleCase["cases"]
						creatLocFilesbyID(unit, t)
					except:
						print '\n\n## TimeOut.\n'
			else:
				ScheduleCase = useAPI(GetScheduleTestDataCase, ScheduleID=unit['scheduledID'])
				try:
					unit["cases"] = ScheduleCase["cases"]
				except:
					print ScheduleCase
				creatLocFilesbyID(unit, t)
			total -= 1
	times = 1
	print '\n%s\nFinished, process will restart after 15 minutes.\n'%time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
	sys.exit()
	time.sleep(900)


{'status': 'Complete', 
'applicationName': None, 
'scheduledEndDate': '2015-01-02T12:00:00+0000', 
'scheduledStartDate': '2014-12-24T12:00:00+0000', 
'trackName': 'Localization', 
'title': '[OS X 10.10.3 SW][LocQA 1]', 
'geography': 'Hong Kong', 
'component': {'version': 'CH', 'name': 'Loc:Proj:OSX Updates'}, 
'lastModifiedAt': '2015-01-02T03:05:55+0000', 
'currentTester': {'lastName': None, 'type': None, 'email': None, 'firstName': None, 'dsid': None}, 
'priority': 5, 
'owner': {'lastName': 'Au-Yeung', 'type': None, 'email': None, 'firstName': 'Stanley', 'dsid': 5803069}, 
'complexity': None, 
'suiteID': 750706, 
'testCycle': None, 
'keywords': [], 
'scheduledID': 2598020, 
'category': 'SW Localization QA', 
'createdAt': '2014-12-24T02:20:00+0000'}

# "cases":[{"summary":null,
# "testSuiteCaseID":13399864,
# "tester":{"lastName":"Yu","email":"lex@beyondtech.co.kr","type":"External","firstName":"Lex","dsid":1858620524},
# "reviewFlag":false,
# "keywords":[],
# "buildID":null,
# "instructions":"1. Computer restarts successfully and goes to the Welcome panel of MacBuddy.\n2. Run with MacBuddy, check these cases:\n- with Internet connection\n- without Internet connection",
# "status":"Fail",
# "actualResult":null,
# "data":null,
# "expectedTime":"0000:15:00",
# "build":null,
# "caseNumber":4,
# "title":"After installation, restart and run with MacBuddy (Only for InstallAssistant)",
# "relatedProblems":[{"id":19358090,"title":"[MacBuddyX] KH: 14D55: Account name is not generated based on Korean Username",
# 	"relationType":"related to",
# 	"component":{"name":"Loc:Proj:OSX Updates","version":"KH"},
# 	"state":"Analyze"}],
# "actualTime":"0000:15:00",
# "priority":2,
# "expectedResult":"Check different workflow with these cases.",
# "createdAt":"2014-12-24T02:21:02+0000",
# "caseID":28691127,
# "counts":{"pictureCount":0,"attchmentCount":0},
# "lastModifiedAt":"2014-12-30T03:19:18+0000"}]