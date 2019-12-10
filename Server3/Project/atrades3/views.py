# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.http import JsonResponse
import requests
import datetime
from django import template
import json
from django.shortcuts import render_to_response
import random
from django.db.models import Avg, Max, Min
API_KEY = "P2TM31A3L0RTIWQB"

def index(request):
    return HttpResponse("Hello, world. Welcome to our web app.")


def get_current_data(request, company_id):
    fun_type = "GLOBAL_QUOTE"
    param = {
        "function": fun_type,
        "symbol": str(company_id),
        "apikey": API_KEY
    }
    response = requests.get('https://www.alphavantage.co/query',params=param)
    s = response.json()
    c = {
        "open": s['Global Quote']['02. open'],
        "high": s['Global Quote']['03. high'],
        "low": s['Global Quote']['04. low'],
        "price": s['Global Quote']['05. price'],
        "volume": s['Global Quote']['06. volume'],
        "ltd": s['Global Quote']['07. latest trading day'],
        "pc": s['Global Quote']['08. previous close'],
        "change": s['Global Quote']['09. change'],
        "cp": s['Global Quote']['10. change percent']
    }

    return HttpResponse(json.dumps(c), content_type='application/json; charset=utf-8')



def get_data(request, company_id, data_type):
    fun_type = "TIME_SERIES_"+str(data_type).upper()
    param = {
        "function": fun_type,
        "symbol": str(company_id),
        "apikey": API_KEY,
        "interval": "5min",

    }
    response = requests.get('https://www.alphavantage.co/query',params=param)
    s = response.json()
    if data_type == "INTRADAY":
        mkey = "Time Series (5min)"
    elif data_type in ("Weekly", "Monthly"):
        mkey = str(data_type) + " Time Series"
    else:
        mkey = "Time Series (Daily)"
    lst = []
    k = 20
    for key in sorted(s[mkey], reverse=True):
        lst.append(
            {"date": str(key), "open": float(s[mkey][key]["1. open"]), "high": float(s[mkey][key]["2. high"]),
             "low": float(s[mkey][key]["3. low"]), "close": float(s[mkey][key]["4. close"])})
        k -= 1
        if k == 0:
            break
    lst.reverse()
    return JsonResponse(lst, safe=False)


def get_custom_data(request, company_id, data_type, start_date, end_date):
    fun_type = "TIME_SERIES_"+str(data_type).upper()
    param = {
        "function": fun_type,
        "symbol": str(company_id),
        "apikey": API_KEY
    }
    response = requests.get('https://www.alphavantage.co/query',params=param)
    s = response.json()
    if data_type in ("Weekly", "Monthly"):
        mkey = str(data_type) + " Time Series"
    else:
        mkey = "Time Series (Daily)"
    lst = []
    start_date = str(start_date)
    start_date = start_date[:4] + "-" + start_date[4:6] + "-" + start_date[6:]
    end_date = str(end_date)
    end_date = end_date[:4] + "-" + end_date[4:6] + "-" + end_date[6:]

    for key in sorted(s[mkey], reverse=True):
        if str(key) >= start_date and str(key) <= end_date:
            lst.append(
                {"date": str(key), "open": float(s[mkey][key]["1. open"]), "high": float(s[mkey][key]["2. high"]),
                 "low": float(s[mkey][key]["3. low"]), "close": float(s[mkey][key]["4. close"])})
    lst.reverse()
    return JsonResponse(lst, safe=False)




def custom_graph_template(request):
    c = {
        "data": "getting data"
    }
    t = template.loader.get_template('atrade/custom_graph_test.html')
    html = t.render(c)
    return HttpResponse(html)


def company_page(request, company_id):

    response = requests.get('http://34.66.96.167/Project/get_current/'+str(company_id)+'/')
    s = response.json()


    response = requests.get('http://34.66.96.167/Project/get_history/'+str(company_id)+'/Daily/')
    t = response.json()
    c = {
        "company_id": str(company_id),
        "company_name": "name of Company from database",
        "current_details": s,
        "current_history": json.dumps(t)
    }
    return render_to_response('atrade/company_home.html', c)


"""
def test_template(request):
    clist = ['AAA', 'ABC', 'AMN', 'PQC', 'LPT']
    cvalue = [10.3, 200.4, 182.0, 635.8, 22.0]
    count = 0
    cur = datetime.datetime(2018, 01, 01, hour=10, minute=0, second=0)
    urs = []
    for i in range(1, 31):
        for j in range(0, 5):
            st = Stocktest(company_id=clist[j],date=cur.strftime("%Y-%m-%d"), time=cur.strftime("%H:%M:%S"), value=324.45)
            st.save()
        cur = cur + datetime.timedelta(0, 120)

    return HttpResponse("testing : %s"%(cur.strftime("%Y-%m-%d-%Z")))
"""





