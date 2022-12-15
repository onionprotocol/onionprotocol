from django.contrib import messages
from django.shortcuts import (HttpResponse, HttpResponseRedirect,
                              get_object_or_404, redirect, render)
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse, reverse_lazy
from django.contrib.auth import login, logout, authenticate


from .models import *
from django.contrib.auth.decorators import login_required




from django.core.mail import send_mail

from datetime import datetime
import datetime as dt
import requests

#from .forms import UserForm

from datetime import datetime
from requests import Request, Session
import json
import time
from datetime import datetime, timedelta


				
		
def ConnectMetamaskManualCantoView(request):
	if request.method == "POST":
		wallet = request.POST.get("wallet")
		request.session["wallet"] = wallet
		
		return HttpResponseRedirect(reverse("portfolio:wcanto_portfolio"))
		

	else:

		context = {}
		return render(request, "portfolio/connect_metamask_manual.html", context)
		
		
		
		
def CantoConnectMetamaskView(request):
	if request.method == "POST":
		wallet = request.POST.get("wallet")
		request.session["wallet"] = wallet
		
		return HttpResponseRedirect(reverse("portfolio:wcanto_portfolio"))
		

	else:

		context = {}
		return render(request, "portfolio/connect_metamask.html", context)

			
			
def WCantoPortfolioView(request):
	if request.method == "POST":
		pass

	else:
		try:
			total = 0
			wallet = request.session["wallet"]
			
			resp = requests.get("https://api.iotexchartapp.com/canto-get-balance/%s/" % str(wallet)).json()
			data = resp["data"]
			#return HttpResponse(str(data))
			response = requests.get("https://api.iotexchartapp.com/canto/get-nft/%s/" % str(wallet)).json()
			nfts = response["data"]
			
			for item in data:
				total += float(item['total_price'])

			#return HttpResponse(str(nfts))
			print(nfts)
			context = {"data": data, "total": total, "wallet": wallet, "nfts": nfts}
			return render(request, "portfolio/canto_portfolio.html", context)
			
		except:
			return HttpResponseRedirect(reverse("portfolio:canto_portfolio"))








        
        


        
        
        
        
        

        
        
def error_404(request, exception):
	return render(request,'app_user/400.html')
	
def error_500(request):
	return render(request,'app_user/500.html')

        
        
