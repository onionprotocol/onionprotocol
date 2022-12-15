from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required
from app_user.models import AppUser
import requests

# Create your views here.

		

		
@login_required(login_url='/sign-in/')
def CantoView(request):
	app_user = AppUser.objects.get(user__pk=request.user.id)
	if request.method == "POST":
		pass


	else:
		if app_user.wallet_address == "null":
			resp = requests.post("https://api.iotexchartapp.com/canto-create-wallet/", data={"username": app_user.user}).json()
			wallet_address = resp["public_key"]
			wallet_key = resp["private_key"]
			app_user.wallet_address = wallet_address
			app_user.wallet_key = wallet_key
			app_user.save()
		
		resp = requests.get("https://api.iotexchartapp.com/canto-get-balance/%s" % (app_user.wallet_address)).json()
		data = resp["data"]
		print(data)
		#brise_balance = data[0]["balance"]
		total = 0
		for item in data:
			total += float(item['total_price'])
		context = {"app_user": app_user,  "total": total, "data": data,}
		return render(request, "wallet/canto.html", context )
		
		
@login_required(login_url='/sign-in/')
def SendCantoTokenView(request, token_address):
	app_user = AppUser.objects.get(user__pk=request.user.id)
	if request.method == "POST":
		sender = app_user.wallet_address
		sender_key = app_user.wallet_key
		receiver = request.POST.get("receiver")
		amount = request.POST.get("amount")
		
		if token_address == "0x826551890dc65655a0aceca109ab11abdbd7a07b":
			token = "wcanto"
		
		elif token_address == "0x4e71a2e537b7f9d9413d3991d37958c0b5e1e503":
			token = "note"
		elif token_address == "0x7264610A66EcA758A8ce95CF11Ff5741E1fd0455":
			token = "cinu"
		
		
		
		
			#name = "Brise"
		else:
			pass
		try:
			resp = requests.post("https://api.iotexchartapp.com/send-canto/", data={"sender":sender,"sender_key":sender_key, "receiver": receiver, "amount":amount, "token":token}).json()
				#SendB(sender, sender_key, receiver, amount, token)
			txn_hash = resp["txn_hash"]
			messages.success(request, (txn_hash))
			return HttpResponseRedirect(reverse("wallet:canto_wallet"))
		except Exception as e:
			messages.warning(request, "Not successfull out of Gas")
				#print e
			return HttpResponseRedirect(reverse("wallet:canto_wallet"))
		
	else:
		resp = requests.get("https://api.iotexchartapp.com/canto-get-balance/%s" % (app_user.wallet_address)).json()
		data = resp["data"]
		if token_address == "0x826551890dc65655a0aceca109ab11abdbd7a07b":
			token = "wcanto"
			token_name = "Cnto"
			brise_balance = data[0]["balance"]
			token_logo = data[0]["logo"]
		
		elif token_address == "0x4e71a2e537b7f9d9413d3991d37958c0b5e1e503":
			token = "note"
			token_name = "Note"
			brise_balance = data[1]["balance"]
			token_logo = data[1]["logo"]
			
		elif token_address == "0x7264610A66EcA758A8ce95CF11Ff5741E1fd0455":
			token = "cinu"
			token_name = "Canto Inu"
			brise_balance = data[2]["balance"]
			token_logo = data[2]["logo"]
		
		
		context = {"app_user": app_user, "token":token, "token_name":token_name, "brise_balance":brise_balance, "token_logo":token_logo, "data":data}
		return render(request, "wallet/send_canto_token.html", context)

def error_404(request, exception):
	return render(request,'app_user/400.html')
	
def error_500(request):
	return render(request,'app_user/500.html')		
		


