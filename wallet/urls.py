from django.urls import path
from . import views

app_name = "wallet"

urlpatterns = [

	path("canto-wallet/", views.CantoView, name="canto_wallet"),

	path("send-canto-token/<str:token_address>/", views.SendCantoTokenView, name="send_canto_token"),
	
	
	
]