#!/usr/bin/env python
#coding=utf-8

__author__ = 'Tinyliu@wistronits.com, tinyliu@me.com'

import simplejson, datetime

def lastModifiedAt(advance=3):
	today = datetime.date.today()
	lastDays = today - datetime.timedelta(days=advance)
	return lastDays.isoformat()

def creatPersonalBodyRequest(bugID, keywords=[], idsOnly=True):
	bodyFileList = []
	bodyRequestModel = {
		'idsOnly':idsOnly,
		'id':bugID}
	for keyword in keywords:
		bodyRequestModel['keyword'] = keyword
		bodyFileList.append(simplejson.dumps(bodyRequestModel))
	return bodyFileList

def creatBodyRequest(proj, langs=[], stateList=['Analyze', 'Integrate', 'Build', 'Verify'], idsOnly=False):
	bodyRequestModel = {'component':[],
		'state':stateList,
		'idsOnly':idsOnly,
		'lastModifiedAt':{'gt':'2010-01-01T16:00:00'}}
	if isinstance(proj, dict):
		for p in proj.values()[0]:
			if langs:
				for language in langs:
					projDetials = {'name':'Loc:Proj:%s'%p, 'version':language}
					bodyRequestModel['component'].append(projDetials)
			else:
				for p in proj.values()[0]:
					projDetials = {'name':'Loc:Proj:%s'%p}
					bodyRequestModel['component'].append(projDetials)
	else:
		if langs:
			for language in langs:
					projDetials = {'name':'Loc:Proj:%s'%proj, 'version':language}
					bodyRequestModel['component'].append(projDetials)
		else:
			bodyRequestModel['component'] = {'name':'Loc:Proj:%s'%proj}
	original = simplejson.dumps(bodyRequestModel)
	bodyRequestModel['lastModifiedAt']['gt'] = '%sT16:00:00'%lastModifiedAt()
	current = simplejson.dumps(bodyRequestModel)
	return original, current

def creatIDBodyRequest(proj, langs=[], radarIDs=[], idsOnly=True):
	bodyRequestModel = {'id':radarIDs,
		'component':[],
		'idsOnly':idsOnly,}
	if isinstance(proj, dict):
		for p in proj.values()[0]:
			if langs:
				for language in langs:
					projDetials = {'name':'Loc:Proj:%s'%p, 'version':language}
					bodyRequestModel['component'].append(projDetials)
			else:
				for p in proj.values()[0]:
					projDetials = {'name':'Loc:Proj:%s'%p}
					bodyRequestModel['component'].append(projDetials)
	else:
		if langs:
			for language in langs:
					projDetials = {'name':'Loc:Proj:%s'%proj, 'version':language}
					bodyRequestModel['component'].append(projDetials)
		else:
			bodyRequestModel['component'] = {'name':'Loc:Proj:%s'%proj}
	return simplejson.dumps(bodyRequestModel)

# print creatIDBodyRequest('OSX', radarIDs=[12314])
# coveredProj = ['OSX', 'OSX Updates', 'ARD', {'FCP':['Final Cut Pro', 'Compressor', 'Motion']}]
# n = 0
# for proj in coveredProj:
# 	a, s = creatBodyRequest(proj, idsOnly=True)
# 	open('/Users/admin/Desktop/1/%s.txt'%n, 'w').write(s)
# 	n += 1

# a, s = creatBodyRequest('OSX', idsOnly=True, langs=['CH', 'TA'])
# open('/Users/admin/Desktop/1/1.txt', 'w').write(s)