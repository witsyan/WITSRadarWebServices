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
from django import template, shortcuts
from ScheduleTest.TSTT import *

import json
import os, sys, datetime
from datetime import *
reload(sys)
sys.setdefaultencoding("utf-8")

#网页信息
webinfo = {
    'title':'TSTT',
    'copyright':'Copyright Wistronits',
    'base':'Data Based on Radar API.',
    'welcometitle':'Welcome',
    'welcomecontent':'请单击选择要显示的内容！',
    'noprojecttitle':'Error',
    'noprojectcontent':'Can\'t find the project: ',
    }

def sssScheduleTest(request):
    select_weeks = 0
    request.session['select_weeks'] = select_weeks
    projects = projList(weekly=select_weeks)
    weekly = weekToDate(select_weeks)
    print weekly
    print projects
    return render_to_response('ScheduleTest.html',{"projects":projects, "CHeight":getHseight(projects), "BHeight":getHseight(projects) + 4, "weekly":weekly, "webinfo":webinfo},)

def ScheduleTest(request):
    seleckweekly = request.GET.get('seleckweekly','0')
    if('select_weeks' in request.session):
        select_weeks = request.session['select_weeks']
    else:
        select_weeks = 0
    if seleckweekly == '0':
        select_weeks = 0
    else:
        select_weeks = int(select_weeks) + int(seleckweekly)
    request.session['select_weeks'] = select_weeks
    projects = projList(weekly=select_weeks)
    weekly = weekToDate(select_weeks)
    #print weekly
    #print projects
    print 'ScheduleTest select_weeks', select_weeks
    return render_to_response('ScheduleTest.html',{"projects":projects, "CHeight":getHseight(projects), "BHeight":getHseight(projects) + 4, "weekly":weekly, "webinfo":webinfo, "select_weeks":select_weeks},)


def ScheduleTestselect(request):
    return render_to_response('ScheduleTestwelcome.html',{ "webinfo":webinfo},)

def ScheduleTestseleckweekly(request):
    seleckweekly = request.GET.get('seleckweekly','0')
    if('select_weeks' in request.session):
        select_weeks = request.session['select_weeks']
    else:
        select_weeks = 0
    if seleckweekly == '0':
        select_weeks = 0
    else:
        select_weeks = int(select_weeks) + int(seleckweekly)
    request.session['select_weeks'] = select_weeks
    projects = projList(weekly=select_weeks)
    weekly = weekToDate(select_weeks)
    print 'ScheduleTestseleckweekly select_weeks', select_weeks
    return render_to_response('ScheduleTestDetail.html',{"projects":projects, "CHeight":getHseight(projects), "BHeight":getHseight(projects) + 4, "weekly":weekly, "webinfo":webinfo},)

#参照 ScheduleTest.js function getHseight()
def getHseight(ps):
    Height = 0
    for p in ps:
        h = p[0][2] * 25 + 20;
        Height = Height + h;
    return Height + len(ps) * 4 + 4;
   
   
   
   
   
   