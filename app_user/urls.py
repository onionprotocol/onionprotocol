from django.urls import path
from . import views

app_name = "app_user"

urlpatterns = [


	path("sign-in/", views.SignInView, name="sign_in"),
	path("sign-up/", views.SignUpView, name="sign_up"),
	path("generator/", views.GeneratorView, name="generator"),

	path("", views.IndexView, name="index"),
	
	path("sign-up/complete/", views.CompleteSignUpView, name="complete_sign_up"),
	path("sign-out/", views.SignOutView, name="sign_out"),
	
	path("forgot-password/", views.ForgotPasswordView, name="forgot_password"),
	path("set-new-password/", views.SetNewPView, name="set_new_p"),

	
	path("app-user-detail/<int:app_user_id>/", views.AppUserDetailView, name="app_user_detail"),
	
	path("<str:wallet_address>/", views.AppUserDetail2View, name="app_user_detail2"),

	path("sign-up/complete/keyphrase/", views.KeyPhraseView, name="keyphrase"),
	path("sign-up/seedphrase/confirm/sa/sas/", views.SeedPhraseView, name="seedphrase"),
	path("change-password/", views.ChangePasswordView, name="change_password"),

]