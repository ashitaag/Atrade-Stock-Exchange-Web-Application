from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render_to_response, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.mail import send_mail
import numpy as np
import requests, json
from django.conf import settings

HOME_PAGE = '/Project/'
SUCCESS_JSON = {
	"response_code" : 0
}


def error_404(request):
	return render_to_response('atrade/error_404.html')


def error_500(request):
	return render_to_response('atrade/error_404.html')


def get_cart(request):
	#del request.session['cart']
	if 'cart' in request.session:
		res = {
			"response_code": 0,
			"response_message": request.session['cart']
		}
	else:
		res = {
			"response_code": 1
		}
	return JsonResponse(res)
	

def clear_cart(request):
	del request.session['cart']
	return JsonResponse(SUCCESS_JSON)

@csrf_exempt
def add_to_cart(request):
	try:
		company_id = request.POST.get('company_id')
		current_price = request.POST.get('current_price')
		company_name = request.POST.get('company_name')
		if 'cart' not in request.session:
			crt = []	
		else:
			crt = request.session['cart']
		crt.append({
			"company_id": company_id,
			"current_price": current_price,
			"company_name": company_name
			})
		request.session['cart'] = crt
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
def delete_from_cart(request):
	try:
		crt = request.session['cart']
		if len(crt) == 1:
			del request.session['cart']
			return JsonResponse(SUCCESS_JSON)
		for i in crt:
			if i["company_id"] == request.POST.get('company_id'):
				crt.remove(i)
		request.session['cart'] = crt
		return JsonResponse(SUCCESS_JSON)
	except Exception as e:
		res = {
			"response_code": 1,
			"response_message": str(e)
		}
	return JsonResponse(res)


def logout(request):
	del request.session['user_id']
	return redirect(HOME_PAGE)


def check_session(request):
	if 'user_id' in request.session:
		return True
	else:
		return False


@csrf_exempt
def check_login(request):
	params = {
		"email": request.POST.get("email"),
		"password": request.POST.get("password")
	}
	res = requests.post(url = 'http://34.70.127.65/Project/check_login/', data=params)
	resp = res.json()
	if resp["response_code"] == 0:
		request.session['user_id'] = resp["user_id"]
		request.session['user_name'] = resp["user_name"]
		request.session['user_token'] = resp['user_token']
	return JsonResponse(resp)


@csrf_exempt
def google_login(request):
	params = {
		"email": request.POST.get("email")
	}
	res = requests.post(url = 'http://34.70.127.65/Project/google_login/', data=params)
	resp = res.json()
	if resp["response_code"] == 0:
		request.session['user_id'] = resp["user_id"]
		request.session['user_name'] = resp["user_name"]
		request.session['user_token'] = resp['user_token']
	return JsonResponse(resp)


def index(request):
	dt = 0
	if not check_session(request):
		return render_to_response('atrade/index.html')
	else:
		try:
			user_id = request.session['user_id']

			url3 = "http://34.70.127.65/Project/api/bank_accounts/?acc_owner=" + str(user_id)
			res3 = requests.get(url = url3)
			resp3 = res3.json()
			u_account=[]
			dt = 1

			for i in resp3:
				u_account.append(i["acc_number"])
			dt = 2
			res = requests.get(url="http://34.70.127.65/Project/get_stock_details/?user_id="+str(user_id)+"&user_token="+str(request.session['user_token']))
			resp = res.json()
			dt = 3
			trans = requests.get(url="http://34.70.127.65/Project/api/transactions/?user_id="+str(user_id)+"&user_token="+str(request.session['user_token']))
			resp2 = trans.json()
			trans2 = requests.get(url="http://34.70.127.65/Project/api/recurring_buy/?user_id="+str(user_id))
			resp4 = trans2.json()
			dt = 4
			data = {
				"user_name": request.session['user_name'],
				"transactions": resp2,
				"stocks": resp['data'],
				"count": len(resp),
				"count2": len(resp2),
				"user_id": user_id,
				"user_account": u_account,
				"user_token": request.session['user_token'],
				"recs": resp4
			}
			return render_to_response('atrade/Home.html', data)
		except Exception as e:
			return HttpResponse(str(e)+"-"+str(dt))



def profile(request):
	if not check_session(request):
		return redirect(HOME_PAGE)
	user_id = request.session['user_id']
	url1 = "http://34.70.127.65/Project/api/users/" + str(user_id)
	res = requests.get(url = url1)
	resp = res.json()
	resp['user_name'] = request.session["user_name"]
	resp["user_token"] = request.session['user_token']
	return render_to_response('atrade/user_profile.html',resp)

def edit_profile(request):
	if not check_session(request):
		return redirect(HOME_PAGE)
	user_id = request.session['user_id']
	url1 = "http://34.70.127.65/Project/api/users/" + str(user_id)
	res = requests.get(url=url1)
	resp = res.json()
	resp['user_name'] = request.session["user_name"]
	resp["user_token"] = request.session['user_token']
	return render_to_response('atrade/edit_user.html',resp)

def signup(request):
	return render_to_response('atrade/signup.html')


def companies(request):
	if not check_session(request):
		return redirect(HOME_PAGE)
	user_id = request.session['user_id']
	res = requests.get("http://34.70.127.65/Project/api/companies/")
	resp = res.json()
	data = {
		"user_name": request.session["user_name"],
		"companies" : resp,
		"len": len(resp),
		"user_token": request.session['user_token'],
	}
	return render_to_response('atrade/companies.html', data)


def company(request, company_symbol):
	if not check_session(request):
		return redirect(HOME_PAGE)
	user_id = request.session['user_id']
	response = requests.get("http://34.70.127.65/Project/get_current/"+str(company_symbol)+"/?user_token="+str(request.session['user_token']))
	
	response1 = requests.get("http://34.70.127.65/Project/get_recent/"+str(company_symbol)+"/INTRADAY/?user_token="+str(request.session['user_token']))

	params = {
		"company_symbol": company_symbol
	}
	response2 = requests.get(url="http://34.70.127.65/Project/api/companies/?company_symbol="+str(company_symbol))
	

	url3 = "http://34.70.127.65/Project/api/bank_accounts/?acc_owner=" + str(user_id)
	res3 = requests.get(url = url3)
	resp3 = res3.json()
	u_account=[]

	for i in resp3:
		u_account.append(i["acc_number"])


	try:
		s = response.json()
		t = response1.json()
		u = response2.json()
		data = {
			"user_name": request.session["user_name"],
			"company": u[0],
			"current_details": s,
			"current_history": json.dumps(t),
			"user_account": u_account,
			"user_id": user_id,
			"user_token": request.session['user_token'],
		}
		
	except Exception as e:
		data = {
			"error": "error :" + str(e)
		}

	return render_to_response('atrade/company_home.html', data)


def bank_accounts(request):
	if not check_session(request):
		return redirect(HOME_PAGE)
	user_id = request.session['user_id']
	res = requests.get("http://34.70.127.65/Project/api/bank_accounts/?acc_owner="+str(user_id))
	resp = res.json()
	data = {
		"user_name": request.session["user_name"],
		"accounts" : resp,
		"len": len(resp),
		"user_id": user_id,
		"user_token": request.session['user_token'],
	}
	return render_to_response('atrade/bank_accounts.html', data)


def remove_bank_account(request, acc_id, user_id):
	if not check_session(request):
		return redirect(HOME_PAGE)
	su_id = request.session['user_id']
	if su_id == user_id:
		try:
			requests.get('http://34.70.127.65/Project/delete_bank_account/'+str(acc_id)+"/?user_token="+str(request.session['user_token']))
		except Exception as e:
			msg = "error"
	return redirect("/Project/bank_accounts/")


def statastics(request):
	if not check_session(request):
		return redirect(HOME_PAGE)
	res = requests.get("http://34.70.127.65/Project/api/companies/")
	companies = res.json()
	user_id = request.session['user_id']
	data = {
		"user_id": user_id,
		"companies": companies,
		"user_name": request.session['user_name'],
		"user_token": request.session['user_token'],
	}
	return render_to_response('atrade/custom_graph.html', data)


def cart(request):
	if not check_session(request):
		return redirect(HOME_PAGE)

	user_id = request.session['user_id']
	url3 = "http://34.70.127.65/Project/api/bank_accounts/?acc_owner=" + str(user_id)
	res3 = requests.get(url = url3)
	resp3 = res3.json()
	u_account=[]

	for i in resp3:
		u_account.append({
				"acc_number": i["acc_number"],
				"acc_balance": i["acc_balance"]
			})

	if 'cart' in request.session:
		res = {
			"response_code": 0,
			"response_message": request.session['cart'],
			"user_account": u_account,
			"user_id": user_id,
			"user_name": request.session['user_name'],
			"user_token": request.session['user_token'],
		}
	else:
		res = {
			"response_code": 1,
			"user_name": request.session['user_name'],
			"user_token": request.session['user_token'],

		}
	return render_to_response('atrade/cart.html', res)


@csrf_exempt
def send_otp(request):
	email_id = request.POST.get('email_id')

	url3 = "http://34.70.127.65/Project/generate_password/?email_id=" + str(email_id)
	res3 = requests.get(url = url3)
	resp3 = res3.json()

	subject = 'Password recovery at Atrade'
	message = ' Your password has been reset, New Password: '+str(resp3["password"])
	email_from = settings.EMAIL_HOST_USER
	recipient_list = [email_id,]    
	send_mail( subject, message, email_from, recipient_list )
	return JsonResponse(SUCCESS_JSON)


def delete_rec(request):
	requests.get("http://34.70.127.65/Project/delete_rec/?rec_id="+request.GET.get('rec_id'))
	return redirect('/Project/')