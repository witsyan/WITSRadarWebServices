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

def RadarWebServiceskeywords(request):
    #获取数据
    project = "OSX"
    kcolumnbasic = {}
    radarurls = {}
    dateformto = ""
    startweek = request.GET.get('startweek','')
    endweek = request.GET.get('endweek','')
    if(startweek.split("~")[0] > endweek.split("~")[0]):
        #print startday, endday
        startweek, endweek = endweek, startweek
    if startweek != '' and endweek != '':
        dateformto = "%s~%s"%(startweek.split("~")[0], endweek.split("~")[-1])
    if dateformto != "":
        kcolumnbasic,radarurls=getCountAndDetailFromAssignee(project,dateformto)
    else:
        kcolumnbasic,radarurls=getCountAndDetailFromAssignee(project)
    weeksList = getWeekList(project)
    x, y = getMaxAndMinDayFromAssignee(project,table="WitsAssignee")
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
    return render_to_response('RadarWebServicesproject.html',{"projects":projects, "project":project, "dailys":dailys, 'webinfo':webinfo, 'startday':startday, 'endday':endday, 'columnbasic':columnbasic ,'containerline':containerline, 'projectdetials':projectdetials, 'projectdaily':projectdaily, 'usbugdetail':usbugdetail })

