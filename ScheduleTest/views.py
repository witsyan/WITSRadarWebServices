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
      [0, 6, 13, "OS X 10.10.2OS X 10.10.2OS X 10.10.2OS X 10.10.2", ],
      [0, 0, 0, '1234567890qwertyuiopasdfghjklzxvbnm,', '100%', ],
      [1, 1, 0, '1234567890qwertyuiopasdfghjklzxvbnm,', '100%', ],
      [2, 2, 0, '1234567890qwertyuiopasdfghjklzxvbnm,', '100%', ],
      [3, 3, 0, '1234567890qwertyuiopasdfghjklzxvbnm,', '100%', ],
      [4, 4, 0, '1234567890qwertyuiopasdfghjklzxvbnm,', '100%', ],
      [5, 5, 0, '1234567890qwertyuiopasdfghjklzxvbnm,', '100%', ],
      [6, 6, 0, '1234567890qwertyuiopasdfghjklzxvbnm,', '100%', ],
      [0, 1, 1, 'sfsdfsadfdsfsdfsdfsdfsdfsdf', '1%', ],
      [0, 2, 2, 'sfsdfsadfdsfsdfsdfsdfsdfsdf', '11%', ],
      [0, 3, 3, 'sfsdfsadfdsfsdfsdfsdfsdfsdfsfsdfsadfdsfsdfsdfsdfsdfsdfsfsdfsadfdsfsdfsdfsdfsdfsdfsfsdfsadfdsfsdfsdfsdfsdfsdfsfsdfsadfdsfsdfsdfsdfsdfsdf', '88%', ],
      [0, 4, 4, '1234567890qwertyuiopasdfghjklzxvbnm,', '100%', ],
      [0, 5, 5, 'sfsdfsadfdsfsdfsdfsdfsdfsdf', '22%', ],
      [0, 6, 6, 'sfsdfsadfdsfsdfsdfsdfsdfsdf', '33%', ],
      [1, 6, 7, 'sfsdfsadfdsfsdfsdfsdfsdfsdf', '44%', ],
      [2, 6, 8, 'sfsdfsadfdsfsdfsdfsdfsdfsdf', '55%', ],
      [3, 6, 9, 'sfsdfsadfdsfsdfsdfsdfsdfsdfsfsdfsadfdsfsdfsdfsdfsdfsdfsfsdfsadfdsfsdfsdfsdfsdfsdfsfsdfsadfdsfsdfsdfsdfsdfsdfsfsdfsadfdsfsdfsdfsdfsdfsdf', '99%', ],
      [4, 6, 10, '1234567890qwertyuiopasdfghjklzxvbnm,', '100%', ],
      [5, 6, 11, 'sfsdfsadfdsfsdfsdfsdfsdfsdf', '66%', ],
      [6, 6, 12, 'sfsdfsadfdsfsdfsdfsdfsdfsdf', '77%', ],],
    [
      [0, 6, 13, "OS X 10.10.2OS X 10.10.2OS X 10.10.2OS X 10.10.2", ],
      [0, 0, 0, '1234567890qwertyuiopasdfghjklzxvbnm,', '100%', ],
      [1, 1, 0, '1234567890qwertyuiopasdfghjklzxvbnm,', '100%', ],
      [2, 2, 0, '1234567890qwertyuiopasdfghjklzxvbnm,', '100%', ],
      [3, 3, 0, '1234567890qwertyuiopasdfghjklzxvbnm,', '100%', ],
      [4, 4, 0, '1234567890qwertyuiopasdfghjklzxvbnm,', '100%', ],
      [5, 5, 0, '1234567890qwertyuiopasdfghjklzxvbnm,', '100%', ],
      [6, 6, 0, '1234567890qwertyuiopasdfghjklzxvbnm,', '100%', ],
      [0, 1, 1, 'sfsdfsadfdsfsdfsdfsdfsdfsdf', '1%', ],
      [0, 2, 2, 'sfsdfsadfdsfsdfsdfsdfsdfsdf', '11%', ],
      [0, 3, 3, 'sfsdfsadfdsfsdfsdfsdfsdfsdfsfsdfsadfdsfsdfsdfsdfsdfsdfsfsdfsadfdsfsdfsdfsdfsdfsdfsfsdfsadfdsfsdfsdfsdfsdfsdfsfsdfsadfdsfsdfsdfsdfsdfsdf', '88%', ],
      [0, 4, 4, '1234567890qwertyuiopasdfghjklzxvbnm,', '100%', ],
      [0, 5, 5, 'sfsdfsadfdsfsdfsdfsdfsdfsdf', '22%', ],
      [0, 6, 6, 'sfsdfsadfdsfsdfsdfsdfsdfsdf', '33%', ],
      [1, 6, 7, 'sfsdfsadfdsfsdfsdfsdfsdfsdf', '44%', ],
      [2, 6, 8, 'sfsdfsadfdsfsdfsdfsdfsdfsdf', '55%', ],
      [3, 6, 9, 'sfsdfsadfdsfsdfsdfsdfsdfsdfsfsdfsadfdsfsdfsdfsdfsdfsdfsfsdfsadfdsfsdfsdfsdfsdfsdfsfsdfsadfdsfsdfsdfsdfsdfsdfsfsdfsadfdsfsdfsdfsdfsdfsdf', '99%', ],
      [4, 6, 10, '1234567890qwertyuiopasdfghjklzxvbnm,', '100%', ],
      [5, 6, 11, 'sfsdfsadfdsfsdfsdfsdfsdfsdf', '66%', ],
      [6, 6, 12, 'sfsdfsadfdsfsdfsdfsdfsdfsdf', '77%', ],],
    ];
    print projects
    print getHseight(projects)
    return render_to_response('ScheduleTest.html',{"projects":projects, "CHeight":getHseight(projects), "BHeight":getHseight(projects) + 4,},)

#参照 ScheduleTest.js function getHseight()
def getHseight(ps):
    Height = 0
    for p in ps:
        h = p[0][2] * 25 + 20;
        Height = Height + h;
    return Height + len(ps) * 4 + 4;
   
   
   
   
   
   