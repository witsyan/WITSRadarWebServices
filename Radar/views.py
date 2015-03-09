#coding=utf8
from django.template import loader, Context
from django.http import HttpResponse,response, request
from django.shortcuts import render_to_response, HttpResponseRedirect
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.sessions.models import Session
from django.template import RequestContext
from django.http import HttpResponse
from django import forms
from django.db.models import Q
from django.forms import forms
from Radar.models import *
from django import template, shortcuts
from Radar.sqlAPI import *

import json
import os, sys, datetime, calendar
from datetime import timedelta
from datetime import *
reload(sys)
sys.setdefaultencoding("utf-8")


#所有 project 名
projects = []
#保存用户选中的 project
project = ''
#得所有日期
dailys = []
startday = ''
endday =''

columnbasic = {}
containerline ={}
projectdetials = {}

#网页信息
webinfo = {
    'title':'Radar Web Services',
    'copyright':'Copyright Wistronits',
    'base':'Data Based on Radar API.',
    'welcometitle':'Welcome',
    'welcomecontent':'Select the projects in the left side to view radar detials.',
    'noprojecttitle':'Error',
    'noprojectcontent':'Can\'t find the project: ',
    }
def getweekslist2(s = "2015-2-8", e = "2015-03-18"):
    if s > e:
        s, e = e, s
    #print calendar.monthcalendar(2015,2)
    sdt = datetime.strptime(s, '%Y-%m-%d')#2014-12-31
    edt = datetime.strptime(e, '%Y-%m-%d')#2015-12-31
    syear = int(sdt.strftime('%Y'))#取出开始年
    smonth = int(sdt.strftime('%m'))#取出开始月
    sday = int(sdt.strftime('%d'))#取出开始日
    
    eyear = int(edt.strftime('%Y'))#取出结束年
    emonth = int(edt.strftime('%m'))#取出结束月
    eday = int(edt.strftime('%d'))#取出结束日
    
    sweek = ""#星期开始日期
    sw = calendar.weekday(syear, smonth, sday)
    print 'bbbb', sw, syear, smonth, sday
    if sw != 0:
        star = sdt + timedelta(days = -sw)
        sweek = star.strftime('%Y-%m-%d')
        print 'ssssweek', sweek, sw
    else:
        star = sdt
        sweek = sdt.strftime('%Y-%m-%d')
        print 'xxxxsweek', sweek, sw
    print 'sweek', sweek, sw
    #星期结束日期
    eweek = ""
    sw = calendar.weekday(eyear, emonth, eday)
    if sw < 6:
        end = edt + timedelta(days = 6 - sw)
        eweek = end.strftime('%Y-%m-%d')
    else:
        end = edt
        eweek = edt.strftime('%Y-%m-%d')
    print 'eweek', eweek, sw
    
    www = []
    sstar = star
    eend = star + timedelta(days = 6)
    if end == eend:
        www.append('%s~%s'%(star.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d')))
    i = 0
    while end != eend:
        i = i + 1
     #   print ""
        www.append('%s~%s'%(sstar.strftime('%Y-%m-%d'), eend.strftime('%Y-%m-%d')))
        print '%s~%s'%(sstar.strftime('%Y-%m-%d'), eend.strftime('%Y-%m-%d')), end, eend, i
        sstar = eend + timedelta(days = 1)
        eend = sstar + timedelta(days = 6)
        if end == eend:
            www.append('%s~%s'%(sstar.strftime('%Y-%m-%d'), eend.strftime('%Y-%m-%d')))
            

    print www, sstar, eend
    return www    




def getweekslist(s = "2015-1-15", e = "2016-3-22"):
    if s > e:
        s, e = e, s
    #calendar.monthcalendar(2015,1)
    sdt = datetime.strptime(s, '%Y-%m-%d')#2014-12-31
    edt = datetime.strptime(e, '%Y-%m-%d')#2015-12-31
    syear = int(sdt.strftime('%Y'))#取出开始年
    smonth = int(sdt.strftime('%m'))#取出开始月
    sday = int(sdt.strftime('%d'))#取出开始日

    eyear = int(edt.strftime('%Y'))#取出结束年
    emonth = int(edt.strftime('%m'))#取出结束月
    eday = int(edt.strftime('%d'))#取出结束日
    
    sweek = ""#星期开始日期
    sw = calendar.weekday(syear, smonth, sday)
    if sw != 0:
        ed = sdt + timedelta(days = -sw)
        sweek = ed.strftime('%Y-%m-%d')
    else:
        sweek = sdt.strftime('%Y-%m-%d')
    print 'sweek', sweek
    #星期结束日期
    eweek = ""
    sw = calendar.weekday(eyear, emonth, eday)
    if sw < 6:
        ed = edt + timedelta(days = 6 - sw)
        eweek = ed.strftime('%Y-%m-%d')
    else:
        eweek = edt.strftime('%Y-%m-%d')
    print 'eweek', eweek, sw

    
    yearlist = range(syear, eyear + 1)#年列表
    print 'yearlist', yearlist
    weekslist = []#星期列表
    monthslist = []#取得月列表
    for y in range(len(yearlist)):
        if yearlist[y] == syear and yearlist[y] == eyear:
            monthslist.append(range(smonth, emonth + 1))#月列表
        elif yearlist[y] == syear:
            monthslist.append(range(smonth, 12 + 1))#月列表
        elif yearlist[y] == eyear:
            monthslist.append(range(1, emonth + 1))#月列表
        else:
            monthslist.append(range(1, 13))#月列表
    print 'monthslist', monthslist
        
    for y in range(len(yearlist)):
        mlist = monthslist[y]#月列表
        for m in mlist:
            wlist = calendar.monthcalendar(yearlist[y], m)
            for w in wlist:
                if int(w[0]) != 0:
                    wd = datetime.strptime("%s-%s-%s"%(yearlist[y], m, w[0]), '%Y-%m-%d')
                    sss = wd.strftime('%Y-%m-%d')
                    if sss not in weekslist:
                        weekslist.append(sss)
                        #print '0', wd.strftime('%Y-%m-%d')
                else:
                    for i in range(len(w)):
                        if int(w[i]) > 0:
                            eee = datetime.strptime('%s-%s-%s'%(yearlist[y], m, w[i]), '%Y-%m-%d') + timedelta(days = -i)
                            sss = eee.strftime('%Y-%m-%d')
                            if sss not in weekslist:
                                weekslist.append(sss)
                                print 'SSSSSSSSS', sss
                            break
                if int(w[-1]) != 0:
                    wd = datetime.strptime("%s-%s-%s"%(yearlist[y], m, w[-1]), '%Y-%m-%d')
                    sss = wd.strftime('%Y-%m-%d')
                    if sss not in weekslist:
                        weekslist.append(sss)
                        print '-1', wd.strftime('%Y-%m-%d')
                else:
                    for i in range(len(w)):
                        if int(w[i]) == 0:
                            ddd = datetime.strptime('%s-%s-%s'%(yearlist[y], m, w[i-1]), '%Y-%m-%d') + timedelta(days = 7 - i)
                            sss = ddd.strftime('%Y-%m-%d')
                            if sss not in weekslist:
                                weekslist.append(sss)
                                print 'XXXXXXX', sss
                            break            
    sw = 0
    ew = 0
    print weekslist
    for w in range(len(weekslist)):
        if weekslist[w] == sweek:
            sw = w
        if weekslist[w] == eweek:
            ew = w
    weekslist = weekslist[sw:ew + 1]   
    print weekslist, sweek, eweek
    return weekslist
    
    

def RadarWebServiceskeywords(request):
    #获取数据
    project = "OSX"
    kcolumnbasic = {}
    radarurls = {}
    dateformto = ""
    startweek = request.GET.get('startweek','')
    endweek = request.GET.get('endweek','')
    print startweek, endweek
    if(startweek.split("~")[0] > endweek.split("~")[0]):
        #print startday, endday
        startweek, endweek = endweek, startweek
    print startweek, endweek
    if startweek != '' and endweek != '':
        dateformto = "%s~%s"%(startweek.split("~")[0], endweek.split("~")[-1])
    if dateformto != "":
        kcolumnbasic,radarurls=getCountAndDetailFromAssignee(project,dateformto)
    else:
        kcolumnbasic,radarurls=getCountAndDetailFromAssignee(project)
    weeksList = getWeekList(project)
    #print radarurls
    x, y = getMaxAndMinDayFromAssignee(project,table="WitsAssignee")
    print "xxx", x, y
    xx = getweekslist2(x,y)
    ii = getweekslist(x,y)
    print "VvvvVVV", xx
    print "VvvvVVV", ii
    #print kcolumnbasic
    return render_to_response('RadarWebServiceskeywords.html',{"project":project, "dailys":dailys, 'webinfo':webinfo, 'kcolumnbasic':kcolumnbasic, 'radarurls':radarurls, 'weeksList':weeksList, 'startweek':startweek, 'endweek':endweek,})


def RadarWebServices(request):
    projects = getProjName()
    startday = request.GET.get('startday','null')
    endday = request.GET.get('endday','null')
    if(startday > endday):
        #print startday, endday
        startday, endday = endday, startday
    #用户选中的 project
    project = request.GET.get('Project','null')
    #点击返回
    if(project == 'null'):# or startday != 'null' or endday != 'null'
        if('Project' in request.session):
            project = request.session['Project']
            if project != 'null' and project in projects:
                dailys = getDateList(project)
                #默认设为最后一天
                if(startday == 'null' or endday == 'null'):
                    if(len(dailys) > 0):
                        startday = dailys[-1]
                        endday = dailys[-1]
                else:
                    request.session['endday'] = endday
                    request.session['startday'] = startday
            #print 'session', project
        #else:
            #print 'null', project     
        return render_to_response('RadarWebServices.html',{"projects":projects, "project":project, 'webinfo':webinfo, },)

def RadarWebServiceswelcome(req):
    return shortcuts.render_to_response('welcome.html',{'webinfo':webinfo, },)

def RadarWebServicesprojectselect(request):
    projects = getProjName()
    #用户选中的 project
    project = request.GET.get('Project','null')
    if(project != 'null'):
        if('Project' in request.session):
            oldproject = request.session['Project']
            if(project != oldproject):
                if('startday' in request.session):
                    del request.session['startday']
                if('endday' in request.session):
                    del request.session['endday']
        if(project in projects):
            request.session['Project'] = project
        else:
            return shortcuts.render_to_response('noproject.html',{'webinfo':webinfo, "project":project, },)            
    else:
        if('Project' in request.session):
            project = request.session['Project']
            if(not (project in projects)):
                del request.session['Project']
                return shortcuts.render_to_response('welcome.html',{'webinfo':webinfo, },)           
            
    startday = request.GET.get('startday','null')
    endday = request.GET.get('endday','null')
    if(startday > endday):
        #print startday, endday
        startday, endday = endday, startday
    if(startday == 'null' or endday == 'null'):
        if('startday' in request.session):
             startday = request.session['startday']
        else:
            startday = 'null'
        if('endday' in request.session):
            endday = request.session['endday']
        else:
            endday = 'null'

    if(project == 'null' or not(project in projects)):
        return shortcuts.render_to_response('noproject.html',{'webinfo':webinfo, "project":project, },)
    dailys = getDateList(project)
    #默认设为最后一天
    if(startday == 'null' or endday == 'null'):
        if(len(dailys) > 0):
            startday = dailys[-1]
            endday = dailys[-1]
    else:
        request.session['endday'] = endday
        request.session['startday'] = startday
        
    #获取数据
    columnbasic,usbugdetail,projectdetials,projectdaily = getCountAndDetailFromDaily(project,startday,endday)
    containerline = getCountFromCount(project)
    #print projectdetials['newlist']
    #print 'RadarWebServicesprojectselect', project
    return render_to_response('RadarWebServicesproject.html',{"projects":projects, "project":project, "dailys":dailys, 'webinfo':webinfo, 'startday':startday, 'endday':endday, 'columnbasic':columnbasic ,'containerline':containerline, 'projectdetials':projectdetials, 'projectdaily':projectdaily, 'usbugdetail':usbugdetail })

