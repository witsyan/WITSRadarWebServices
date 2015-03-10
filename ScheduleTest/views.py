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

import json
import os, sys, datetime
from datetime import *
reload(sys)
sys.setdefaultencoding("utf-8")

def ScheduleTest(request):
    projects = [
      [
        [0, 6, 2, "OS X 10.10.2 SW", ],
        [0, 0, 0, 'LocQA OTR,', '93.94%', ],
        [1, 1, 1, 'LocQA OTR1,', '100%', ],
      ],
      [
        [0, 6, 2, "OS X 10.10.3 SW", ],
        [0, 0, 0, 'LocQA 1,', '100%', ],
        [1, 3, 1, 'LocQA 2', '77%', ]
      ],
      [
        [0, 6, 2, "ARD", ],
        [0, 1, 0, 'External,', '100%', ],
        [1, 3, 1, 'PkgData LocQA4', '77%', ]
      ],
    ];
    return render_to_response('ScheduleTest.html',{"projects":projects, "CHeight":getHseight(projects), "BHeight":getHseight(projects) + 4,},)

#参照 ScheduleTest.js function getHseight()
def getHseight(ps):
    Height = 0
    for p in ps:
        h = p[0][2] * 25 + 20;
        Height = Height + h;
    return Height + len(ps) * 4 + 4;
   
   
   
   
   
   