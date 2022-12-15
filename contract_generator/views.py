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


def IndexView(request):
	if request.method == "POST":
		pass
	else:
		context = {}
		return render(request, "contract_generator/index.html", context)

			
def GeneratorView(request):
	if request.method == "POST":
		pass

	else:
		context = {}
		return render(request, "contract_generator/contract_generator.html", context )

        
        
def error_404(request, exception):
	return render(request,'app_user/400.html')
	
def error_500(request):
	return render(request,'app_user/500.html')

        
        
