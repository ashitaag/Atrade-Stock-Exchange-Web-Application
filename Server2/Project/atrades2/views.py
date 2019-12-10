from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from rest_framework import viewsets, generics, filters
from .models import User, Transaction, BankAccount, Company, Stocks, RecurringBuy, Queue
from .serializers import UserSerializer, BankAccountSerializer, CompanySerializer, StocksSerializer, TransactionSerializer, RecurringBuySerializer
import django_filters.rest_framework
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
import requests
from datetime import datetime, timedelta
import random, string
from collections import defaultdict
from django.core.cache import cache
import time
import schedule
from django.db import connection


SERVER_REQ_COUNT = 0

FORBIDDEN_RESPONSE = JsonResponse({
    "response_code": 9,
    "response_message": "access forbidden"
    })

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        """ allow rest api to filter by submissions """
        queryset = User.objects.all()
        submission = self.request.query_params.get('user_fname', None)
        if submission is not None:
            queryset = queryset.filter(user_fname=submission)
        return queryset


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all().order_by('transaction_id')
    serializer_class = TransactionSerializer

    def get_queryset(self):
        """ allow rest api to filter by submissions """
        queryset = Transaction.objects.all()
        userid = self.request.query_params.get('user_id', None)
        if userid is not None:
            queryset = queryset.filter(transaction_user=userid)
        return queryset


class StocksViewSet(viewsets.ModelViewSet):
    queryset = Stocks.objects.all().order_by('-stock_id')
    serializer_class = StocksSerializer
    
    def get_queryset(self):
        """ allow rest api to filter by submissions """
        queryset = Stocks.objects.all()
        userid = self.request.query_params.get('user_id', None)
        if userid is not None:
            queryset = queryset.filter(stock_user=userid)
        return queryset


class RecurringBuyViewSet(viewsets.ModelViewSet):
    queryset = RecurringBuy.objects.all().order_by('-rec_id')
    serializer_class = RecurringBuySerializer

    def get_queryset(self):
        """ allow rest api to filter by submissions """
        queryset = RecurringBuy.objects.all()
        userid = self.request.query_params.get('user_id', None)
        if userid is not None:
            queryset = queryset.filter(rec_user_id=userid)
        return queryset


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all().order_by('-company_id')
    serializer_class = CompanySerializer
    def get_queryset(self):
        """ allow rest api to filter by submissions """
        queryset = Company.objects.all()
        submission = self.request.query_params.get('company_symbol', None)
        if submission is not None:
            queryset = queryset.filter(company_symbol=submission)
        return queryset

class BankAccountViewSet(viewsets.ModelViewSet):
    queryset = BankAccount.objects.all().order_by('-acc_id')
    serializer_class = BankAccountSerializer

    def get_queryset(self):
        """ allow rest api to filter by submissions """
        queryset = BankAccount.objects.all()
        submission = self.request.query_params.get('acc_owner', None)
        if submission is not None:
            queryset = queryset.filter(acc_owner=submission)
        return queryset


def index(request):
    return HttpResponse("hellow")



def verify_token(request):
    try:
        u = User.objects.get(user_token=request.GET.get('user_token'))
        return True
    except Exception as e:
        return False


@csrf_exempt
def create_user(request):
    try:
        us = User(
            user_fname= request.POST.get('user_fname'), 
            user_lname= request.POST.get('user_lname'), 
            user_ssn= request.POST.get('user_ssn'), 
            user_address= request.POST.get('user_address'), 
            user_password= request.POST.get('user_password'), 
            user_phone= request.POST.get('user_phone'),
            user_email = request.POST.get('user_email'),
            user_token = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(20)]),
            )
        
        us.save()
        res = {
            "response_code" : 0
        }
    except Exception as e:
        res = {
            "response_code": 1,
            "response_message": str(e)
        }
    return JsonResponse(res)


@csrf_exempt
def check_login(request):
   email= request.POST.get("email")
   pwd= request.POST.get("password")

   try:
      u = User.objects.get(user_email=str(email))
      if u.user_password != pwd:
         response = {
            "response_code": 2,
            "response_message": "The password is incorrect"
         }
      else:
         response = {
            "response_code": 0,
            "user_id": u.user_id,
            "user_name": str(u.user_fname + " " + u.user_lname),
            "user_token": u.user_token,
         }
   except Exception as e:
      response = {
         "response_code": 1,
         "response_message": "The email doesnot exist",
         "error_msg": str(e)
      }
   return JsonResponse(response)   


@csrf_exempt
def google_login(request):
	email= request.POST.get("email")

	try:
		u = User.objects.get(user_email=str(email))
		response = {
			"response_code": 0,
			"user_id": u.user_id,
			"user_name": str(u.user_fname + " " + u.user_lname),
			"user_token": u.user_token,
		}
	except Exception as e:
		response = {
			"response_code": 1,
			"response_message": "You haven't registered yet, Please register first to login using google"
		}
	return JsonResponse(response) 


def get_current_data(request, company_id):
    if not verify_token(request):
        return FORBIDDEN_RESPONSE
    global SERVER_REQ_COUNT
    response = requests.get('http://34.66.96.167/Project/get_current/'+str(company_id)+'/')
    s = response.json()
    SERVER_REQ_COUNT += 1
    return JsonResponse(s)


def get_custom_data(request, company_id, data_type, start_date, end_date):
    if not verify_token(request):
        return FORBIDDEN_RESPONSE
    global SERVER_REQ_COUNT
    response = requests.get('http://34.66.96.167/Project/get_custom/'+str(company_id)+'/'+str(data_type)+'/'+str(start_date)+'/'+str(end_date)+'/')
    t = response.json()
    SERVER_REQ_COUNT += 1
    return JsonResponse(t, safe=False)





def view_count(request):
    data = {
        "view_count": SERVER_REQ_COUNT
    }
    return JsonResponse(data)


@csrf_exempt
def update_user_profile(request):
    if not verify_token(request):
        return FORBIDDEN_RESPONSE
    u = User.objects.get(user_id = int(request.POST.get("user_id")))
    u.user_fname = str(request.POST["user_fname"])
    u.user_lname = str(request.POST.get("user_lname"))
    u.user_address = str(request.POST.get("user_address"))
    u.user_phone = str(request.POST.get("user_phone"))
    u.user_email = str(request.POST.get("user_email"))
    u.user_password = str(request.POST.get("user_password"))

    try:
        u.save()
        res = {
            "response_code" : 0
        }
    except Exception as e:
        res = {
            "response_code" : 1,
            "response_message" : str(e)
        }

    return JsonResponse(res)


def delete_bank_account(request, acc_id):
    if not verify_token(request):
        return FORBIDDEN_RESPONSE
    BankAccount.objects.get(acc_id=acc_id).delete()
    data = {
        "response_code": 0
    }
    return JsonResponse(data)


@csrf_exempt
def create_bank_account(request):
    if not verify_token(request):
        return FORBIDDEN_RESPONSE
    try:
        ba = BankAccount(
            acc_number=request.POST.get('acc_number'),
            acc_type = request.POST.get('acc_type'),
            acc_owner = request.POST.get('acc_owner'),
            acc_routing_number = request.POST.get('acc_routing_number'),
            acc_balance = round(random.uniform(100,5000), 2)
        )
        ba.save()
        res = {
            "response_code": 0
        }
    except Exception as e:
        res = {
            "response_code": 1,
            "response_message": str(e)
        }

    return JsonResponse(res)



@csrf_exempt
def get_stock_details(request):
    if not verify_token(request):
        return FORBIDDEN_RESPONSE

    cache_key = 'stocks_details_key'+request.GET.get('user_id')
    cache_time = 1800 # time to live in seconds
    dct = cache.get(cache_key)
    cached = True

    if not dct:
        user_id = request.GET.get('user_id')
        stocks = Stocks.objects.filter(stock_user=user_id)
        ans = []
        res = defaultdict(int)
        tot = defaultdict(int)
        for a in stocks:
            ans.append(model_to_dict(a))
            res[a.stock_symbol] = round(res[a.stock_symbol] + (a.stock_buy_price * a.stock_count), 2)
            tot[a.stock_symbol] += a.stock_count
        #return HttpResponse(res.keys().__str__())
        dct = []
        for key in res.keys():
            if tot[key] > 0:
                company = Company.objects.get(company_symbol= key)
                dct.append({
                    "company_name": company.company_name,
                    "total_stocks": tot[key],
                    "total_price": res[key],
                    "company_symbol": key
                })
        cache.set(cache_key, dct, cache_time)
        cached = False

    data = {
        "cached": cached,
        "data": dct
    }

    return JsonResponse(data, safe=False)


@csrf_exempt
def get_stock_analysis(request):
    if not verify_token(request):
        return FORBIDDEN_RESPONSE
    try:
        company_symbol = request.POST.get('company_symbol')
        res = requests.get('http://34.66.96.167/Project/get_current/'+str(company_symbol)+'/')
        resp = res.json()
        company = Company.objects.get(company_symbol = company_symbol)
        data = {
            "response_code": 0,
            "current_price": resp["price"],
            "company": model_to_dict(company)
        }
    except Exception as e:
        data = {
            "response_code": 1,
            "response_message": str(e)
        }
    return JsonResponse(data)


@csrf_exempt
def sell_stock(request):
    if not verify_token(request):
        return FORBIDDEN_RESPONSE
    st = Stocks(
            stock_user = request.POST.get('user_id'),
            stock_symbol = request.POST.get('company_symbol'),
            stock_buy_price = request.POST.get('current_price'),
            stock_buy_timestamp = datetime.now().__str__(),
            stock_count = -int(request.POST.get('stocks_to_sell')),
        )

    tr = Transaction(
            transaction_user = request.POST.get('user_id'),
            transaction_timestamp = datetime.now().__str__(),
            transaction_account = request.POST.get('account_number'),
            transaction_type = 'sell',
            transaction_symbol = request.POST.get('company_symbol'),
            transaction_price = round(float(request.POST.get('current_selling_price')),2),
        )

    ba = BankAccount.objects.get(acc_number = request.POST.get('account_number'))
    ba.acc_balance = round(ba.acc_balance + float(request.POST.get('current_selling_price')),2)
    cache.clear()
    try:
        st.save()
        tr.save()
        ba.save()


        res = {
            "response_code": 0
        }
    except Exception as e:
        res = {
            "response_code": 0,
            "response_message": str(e),
        }
    return JsonResponse(res)


@csrf_exempt
def transfer_funds(request):
    if not verify_token(request):
        return FORBIDDEN_RESPONSE
    try:
        user_id = request.POST.get('acc_owner')
        from_account = request.POST.get('from_account')
        to_account = request.POST.get('to_account')
        amount = float(request.POST.get('amount'))
        ba1 = BankAccount.objects.get(acc_number = from_account)
        ba2 = BankAccount.objects.get(acc_number = to_account)
        ba1.acc_balance -= amount
        ba2.acc_balance += amount

        tr = Transaction(
            transaction_user = user_id,
            transaction_type = 'transfer',
            transaction_price = amount,
            transaction_account = from_account,
            transaction_symbol = to_account,
            transaction_timestamp = datetime.now().__str__()
        )

        ba1.save()
        ba2.save()
        tr.save()
        res={
            "response_code": 0
        }
    except Exception as e:
        res={
            "response_code": 1,
            "response_message": str(e),
        }
    return JsonResponse(res)



def get_recent_data(request, company_id, data_type):
    if not verify_token(request):
        return FORBIDDEN_RESPONSE
    global SERVER_REQ_COUNT
    now = datetime.now()
    today = now.strftime("%Y%m%d")
    if data_type == "INTRADAY":
        response = requests.get('http://34.66.96.167/Project/get_history/'+str(company_id)+'/'+str(data_type)+'/')
        t = response.json()
    elif data_type == "Week":
        data_type = "Daily"
        last_day = (now - timedelta(days=7)).strftime("%Y%m%d")
        response = requests.get('http://34.66.96.167/Project/get_custom/'+str(company_id)+'/'+str(data_type)+'/'+str(last_day)+'/'+str(today)+'/')
        t = response.json()
    elif data_type == "LastWeek":
        data_type = "Daily"
        today = (now - timedelta(days=7)).strftime("%Y%m%d")
        last_day = (now - timedelta(days=14)).strftime("%Y%m%d")
        response = requests.get('http://34.66.96.167/Project/get_custom/'+str(company_id)+'/'+str(data_type)+'/'+str(last_day)+'/'+str(today)+'/')
        t = response.json()        
    elif data_type == "Month":
        data_type = "Daily"
        last_day = (now - timedelta(days=30)).strftime("%Y%m%d")
        response = requests.get('http://34.66.96.167/Project/get_custom/'+str(company_id)+'/'+str(data_type)+'/'+str(last_day)+'/'+str(today)+'/')
        t = response.json()  
    elif data_type == "LastMonth":
        data_type = "Daily"
        today = (now - timedelta(days=30)).strftime("%Y%m%d")
        last_day = (now - timedelta(days=60)).strftime("%Y%m%d")
        response = requests.get('http://34.66.96.167/Project/get_custom/'+str(company_id)+'/'+str(data_type)+'/'+str(last_day)+'/'+str(today)+'/')
        t = response.json()  
    elif data_type == "Year":
        data_type = "Weekly"
        last_day = (now - timedelta(days=365)).strftime("%Y%m%d")
        response = requests.get('http://34.66.96.167/Project/get_custom/'+str(company_id)+'/'+str(data_type)+'/'+str(last_day)+'/'+str(today)+'/')
        t = response.json() 
    elif data_type == "5Year":
        data_type = "Monthly"
        last_day = (now - timedelta(days=1825)).strftime("%Y%m%d")
        response = requests.get('http://34.66.96.167/Project/get_custom/'+str(company_id)+'/'+str(data_type)+'/'+str(last_day)+'/'+str(today)+'/')
        t = response.json() 

    SERVER_REQ_COUNT += 1
    return JsonResponse(t, safe=False)


@csrf_exempt
def buy_queue_stocks(request):
    if not verify_token(request):
        return FORBIDDEN_RESPONSE
    try:
        count = int(request.POST.get('count'))
        account_number = request.POST.get('account_number')
        user_id = request.POST.get('user_id')
        data = []
        for i in range(count):
            q = Queue(
                    user_id= int(user_id),
                    company_symbol= request.POST.get('stocks['+str(i)+"][company_id]"),
                    total_amount= float(request.POST.get('stocks['+str(i)+"][total_price]")),
                    stock_price = float(request.POST.get('stocks['+str(i)+"][current_price]")), 
                    stocks_count = int(request.POST.get('stocks['+str(i)+"][count]")), 
                    tr_account = account_number
                )
            data.append(q)
            q.save()
        time.sleep(20)
        buy_stocks_from_queue(data)
        cache.clear()

        res = {
            "response_code": 0
        }
    except Exception as e:
        res = {
            "response_code": 1,
            "response_message": str(e)

        }
    return JsonResponse(res)


def buy_stocks_from_queue(data):

    for q in data:
        buy_stock(q.user_id, q.company_symbol, q.total_amount, q.stock_price, q.stocks_count, q.tr_account)
        q.delete()
    return


def view_queue(request):
    q = Queue.objects.all()
    dt = []
    for Q in q:
        dt.append(model_to_dict(Q))
    return JsonResponse(dt, safe=False)


@csrf_exempt
def buy_stock(user_id, company_symbol, total_amount, stock_price, stocks_count, tr_account):

    current_timestamp = datetime.now().__str__()

    t = Transaction(
            transaction_user = user_id,
            transaction_timestamp = current_timestamp,
            transaction_account = tr_account,
            transaction_symbol = company_symbol,
            transaction_price = round(float(total_amount),2),
            transaction_type = 'buy',
        )

    s = Stocks(
            stock_user = user_id,
            stock_symbol = company_symbol,
            stock_buy_price = round(float(stock_price),2),
            stock_buy_timestamp = current_timestamp,
            stock_count = stocks_count
        )

    ba = BankAccount.objects.get(acc_number = tr_account)
    ba.acc_balance = ba.acc_balance - float(total_amount)


    try:
        if ba.acc_balance < 0:
            raise Exception("Sufficient balance is not available in this account")
        s.save()
        t.save()
        ba.save()

        res = {
            "response_code": 0 
        }
    except Exception as e:
        res = { 
            "response_code": 1,
            "response_message": "Error Occured :"+str(e)
        }



def generate_password(request):
    email = request.GET.get('email_id')
    u = User.objects.get(user_email = email)
    ps = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(8)])
    u.user_password = ps
    u.save()
    res = {
        "password": ps
    }
    return JsonResponse(res)


@csrf_exempt
def set_up_rec(request):
    r = RecurringBuy(
            rec_user_id = request.POST.get('user_id'),
            rec_symbol = request.POST.get('rec_symbol'),
            rec_interval = request.POST.get('rec_interval'),
            rec_count = request.POST.get('rec_count'),
            rec_start_timestamp = datetime.now().__str__(),
            rec_schedule = ''.join([random.choice(string.ascii_letters) for n in range(8)])
        )
    current_price = request.POST.get('current_price')

    cursor = connection.cursor()
    
    query = """CREATE EVENT """+r.rec_schedule+""" 
    ON SCHEDULE EVERY """+r.rec_interval+"""
    STARTS CURRENT_TIMESTAMP ENDS CURRENT_TIMESTAMP + INTERVAL 1 HOUR 
    DO
        INSERT INTO stocks(`stock_user`,`stock_symbol`,`stock_buy_price`,`stock_count`) VALUES('"""+str(r.rec_user_id)+"""'
        , '"""+str(r.rec_symbol)+"""', """+current_price+""", """+r.rec_count+""");"""
    cursor.execute(query)
    r.save()
    res = {
        "response_code": 0,
        "response_message": query
    }
    return JsonResponse(res)


def delete_rec(request):
    rec = RecurringBuy.objects.get(rec_id=request.GET.get('rec_id'))
    name = rec.rec_schedule
    cursor = connection.cursor()

    query = """DROP EVENT """+name
    cursor.execute(query)
    rec.delete()
    return HttpResponse("success")
