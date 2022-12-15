from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User

from django.core.mail import send_mail
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from datetime import datetime
import datetime as dt
import requests
from django.shortcuts import redirect
from .forms import UserForm
from .models import AppUser
from django.contrib.auth.decorators import login_required

import random
import string


def RayGenkey():
    word_site = "https://www.mit.edu/~ecprice/wordlist.10000"
    response = requests.get(word_site)
    words = response.content.splitlines()
    keyphrase = []
    for item in range(12):
        keyphrase.append(random.choice(words))

    return keyphrase

def ray_randomiser(length=6):
    landd = string.ascii_letters + string.digits
    return ''.join((random.choice(landd) for i in range(length)))
    

def RaySendMail(request, subject, message, to_email, code=None):

    #try:
    context = {"subject": subject, "message": message, "code": code}
    html_message = render_to_string('app_user/message.html', context)
    message = strip_tags(message)

    send_mail(
        subject,
        message,
        'hello@curlfinance.com',
        [to_email,],
        html_message=html_message,
        fail_silently=False,
    )

    #except:
     #   pass




def ForgotPasswordView(request):
    
    if request.method == "POST":
        email = request.POST.get("username")
        
        app_users = AppUser.objects.filter(user__username=email)
        
        if len(app_users) > 0:
            app_user = app_users.last()
            app_user.otp_code = ray_randomiser()
            app_user.save()
            
            RaySendMail(request, subject="Password Reset.", message="Looks like you lost your password. Kindly use this OTP code; %s to retrieve your account." % (app_user.otp_code), to_email=app_user.user.username, code=app_user.otp_code)

        
            messages.warning(request, "Set new password.")
            return HttpResponseRedirect(reverse("app_user:set_new_p"))
        
        else:
            messages.warning(request, "Sorry, Invalid OTP code.")
            return HttpResponseRedirect(reverse("app_user:forgot_password"))
        
        
    else:
        
        context = {}
        return render(request, "app_user/forgot_password.html", context)
        
        



def SetNewPView(request):
    
    if request.method == "POST":
        otp = request.POST.get("otp")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        
        app_users = AppUser.objects.filter(otp_code=otp)
        
        if request.POST.get("password2") != request.POST.get("password1"):
            messages.warning(request, "Make sure both passwords match")
            return HttpResponseRedirect(reverse("app_user:set_new_p"))
            
        elif len(app_users) > 0:
            app_user = app_users.last()
            
            user = app_user.user
            user.set_password(str(password2))
            user.save()
        
            messages.warning(request, "New Password Created!")
            return HttpResponseRedirect(reverse("app_user:sign_in"))
            
        else:
            messages.warning(request, "Sorry, Invalid OTP code.")
            return HttpResponseRedirect(reverse("app_user:set_new_p"))
        
        
    else:
        context = {}
        return render(request, "app_user/set_new_p.html", context)
        
        
                

def SignInView(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)

                app_user = AppUser.objects.get(user__pk=request.user.id)
                
                if app_user.ec_status == True:
                    
                    if app_user.user.username == "odiagaraymondrayray@gmail.com":
                
                        print("11111111111111111111111111111111")
                        messages.success(request, "Welcome Onboard")
                        return HttpResponseRedirect(reverse("admin_app:index"))
                    
                    else:
                        print("22222222222222222222222222222222")
                        messages.warning(request, "Welcome Onboard")
                        #return redirect('/wallet/?next=%s' % request.path)
                        return HttpResponseRedirect(reverse("wallet:canto_wallet"))
                
                
                else:
                    print("22222222222222222222222222222222")
                    messages.warning(request, "Sorry, validate your account")
                    return HttpResponseRedirect(reverse("app_user:sign_in"))
                
            else:
                print("22222222222222222222222222222222")
                messages.warning(request, "Sorry, Invalid Login Details")
                return HttpResponseRedirect(reverse("app_user:sign_in"))

        else:
            print("33333333333333333333333333333333333333")
            messages.warning(request, "Sorry, Invalid Login Details")
            return HttpResponseRedirect(reverse("app_user:sign_in"))

    else:
        context = {}
        return render(request, "app_user/sign_in.html", context )




def SignUpView(request):
    if request.method == "POST":

        form = UserForm(request.POST or None, request.FILES or None)
        email = request.POST.get("username")
        #first_name = request.POST.get("first_name")
        #last_name = request.POST.get("last_name")
        


        if request.POST.get("password2") != request.POST.get("password1"):
            messages.warning(request, "Make sure both passwords match")
            return HttpResponseRedirect(reverse("app_user:sign_up"))

            
        else:
            try:
                AppUser.objects.get(user__email=request.POST.get("username"))
                messages.warning(request, "Email Address already taken!")
                return HttpResponseRedirect(reverse("app_user:sign_up"))


            except:
                user = form.save()
                user.set_password(request.POST.get("password1"))
                user.save()

                app_user = AppUser.objects.create(user=user)
                app_user.otp_code = ray_randomiser()

                
                
                app_user.save()

                user = app_user.user
                user.email = email
                
                user.save()
                
                #RaySendMail(request, subject="Email Confirmation.", message="Thank you for signing up with CurlFinance, Your OTP code is %s" % (app_user.otp_code), to_email=app_user.user.username, code=app_user.otp_code)

                if user:
                    if user.is_active:
                        login(request, user)

                        app_user = AppUser.objects.get(user__pk=request.user.id)
                        messages.warning(request, "Wallet access key")
                        return HttpResponseRedirect(reverse("app_user:complete_sign_up"))

    else:
        form = UserForm()
        context = {"form": form}
        return render(request, "app_user/sign_up.html", context )



    return render(request, "app_user/sign_up.html", context )


def CompleteSignUpView(request):
    app_user = AppUser.objects.get(user__pk=request.user.id)
    if request.method == "POST":
        otp = request.POST.get("otp")
        
        
        if otp == app_user.otp_code:
            app_user.ec_status = True
            app_user.save()

            messages.warning(request, "almost there!")
            return HttpResponseRedirect(reverse("app_user:keyphrase"))

        else:

            messages.warning(request, "Invalid Access Key.")
            return HttpResponseRedirect(reverse("app_user:complete_sign_up"))


    else:
        otp_code = app_user.otp_code
        context = {'otp_code':otp_code}
        return render(request, "app_user/complete_sign_up.html", context )





def SignOutView(request):

    logout(request)
    return HttpResponseRedirect(reverse("app_user:sign_in"))






def AppUserDetail2View(request, wallet_address):
    try:
        app_user = AppUser.objects.get(user__pk=request.user.id)
    except:
        app_user = None
        
    if request.method == "POST":
        pass


    else:
        recruit = AppUser.objects.get(wallet_address=wallet_address)

        context = {"app_user": app_user, "recruit": recruit}
        return render(request, "app_user/app_user_detail2.html", context )




@login_required(login_url='/app_user/sign_in/')
def AppUserDetailView(request, app_user_id):
    app_user = AppUser.objects.get(user__pk=request.user.id)
    if request.method == "POST":
        pass


    else:
        recruit = AppUser.objects.get(id=app_user_id)

        context = {"app_user": app_user, "recruit": recruit}
        return render(request, "app_user/app_user_detail.html", context )


def TempView(request):
    if request.method == "POST":
        pass


    else:
        context = {}
        return render(request, "app_user/app.html", context )



def ProfileView(request):
    if request.method == "POST":
        pass


    else:
        context = {}
        return render(request, "app_user/profile.html", context )


def MaintainView(request):
    if request.method == "POST":
        pass


    else:
        context = {}
        return render(request, "app_user/maintainance.html", context )
        
def ChangePasswordView(request):

    app_user = AppUser.objects.get(user__pk=request.user.id)
    if request.method == "POST":
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        
        user = app_user.user
        user.set_password(str(password2))
        user.save()
    
        messages.warning(request, "New Password Created!")
        return HttpResponseRedirect(reverse("app_user:sign_in"))


    else:
        pass

        context = {"app_user": app_user}
        
        return render(request, "app_user/change_password.html", context)

def GeneratorView(request):
    if request.method == "POST":
        pass

    else:
        context = {}
        return render(request, "app_user/generator.html", context )

def IndexView(request):
    if request.method == "POST":
        pass
    else:
        context = {}
        return render(request, "app_user/index.html", context)

def KeyPhraseView(request):
    app_user = AppUser.objects.get(user__pk=request.user.id)

    if request.method == "POST":
        pass

    else:
        keyphrase = RayGenkey()
        app_user.passphrase0 = keyphrase[0].decode("utf-8")
        app_user.passphrase1 = keyphrase[1].decode("utf-8")
        app_user.passphrase2 = keyphrase[2].decode("utf-8")
        app_user.passphrase3 = keyphrase[3].decode("utf-8")
        app_user.passphrase4 = keyphrase[4].decode("utf-8")
        app_user.passphrase5 = keyphrase[5].decode("utf-8")
        app_user.passphrase6 = keyphrase[6].decode("utf-8")
        app_user.passphrase7 = keyphrase[7].decode("utf-8")
        app_user.passphrase8 = keyphrase[8].decode("utf-8")
        app_user.passphrase9 = keyphrase[9].decode("utf-8")
        app_user.passphrase10 = keyphrase[10].decode("utf-8")
        app_user.passphrase11 = keyphrase[11].decode("utf-8")
        app_user.save()

        context = {"app_user": app_user}
        return render(request, "app_user/keyphrase.html", context )




def SeedPhraseView(request):
    app_user = AppUser.objects.get(user__pk=request.user.id)
    if request.method == "POST":

        passphrase0 = request.POST.get("passphrase0")
        passphrase1 = request.POST.get("passphrase1")
        passphrase2 = request.POST.get("passphrase2")
        passphrase3 = request.POST.get("passphrase3")
        passphrase4 = request.POST.get("passphrase4")
        passphrase5 = request.POST.get("passphrase5")
        passphrase6 = request.POST.get("passphrase6")
        passphrase7 = request.POST.get("passphrase7")
        passphrase8 = request.POST.get("passphrase8")
        passphrase9 = request.POST.get("passphrase9")
        passphrase10 = request.POST.get("passphrase10")
        passphrase11 = request.POST.get("passphrase11")

        if str(app_user.passphrase0) == str(passphrase0) and str(app_user.passphrase1) == str(passphrase1) and str(app_user.passphrase2) == str(passphrase2) and str(app_user.passphrase3) == str(passphrase3) and str(app_user.passphrase4) == str(passphrase4) and str(app_user.passphrase5) == str(passphrase5) and str(app_user.passphrase6) == str(passphrase6) and str(app_user.passphrase7) == str(passphrase7) and str(app_user.passphrase8) == str(passphrase8) and str(app_user.passphrase9) == str(passphrase9) and str(app_user.passphrase10) == str(passphrase10) and str(app_user.passphrase11) == str(passphrase11):
            app_user.status = True
            app_user.save()

            messages.warning(request, "Welcome to the future!")
            return HttpResponseRedirect(reverse("wallet:canto_wallet"))

        else:
            messages.warning(request, "Not Successfull!")
            return HttpResponseRedirect(reverse("app_user:seedphrase"))




    else:
        context = {"app_user": app_user}

        return render(request, "app_user/seedphrase.html", context )
        
def error_404(request, exception):
    return render(request,'app_user/400.html')
    
def error_500(request):
    return render(request,'app_user/500.html')



