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

def ScheduleTest(request):
    select_weeks = 0
    projects = projList(weekly=select_weeks)
    weekly = weekToDate(select_weeks)
    return render_to_response('ScheduleTest.html',{"projects":projects, "CHeight":getHseight(projects), "BHeight":getHseight(projects) + 4, "weekly":weekly},)

#参照 ScheduleTest.js function getHseight()
def getHseight(ps):
    Height = 0
    for p in ps:
        h = p[0][2] * 25 + 20;
        Height = Height + h;
    return Height + len(ps) * 4 + 4;
   
   
   
   
   
   