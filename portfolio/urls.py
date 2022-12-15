from django.urls import path
from . import views

app_name = "portfolio"

urlpatterns = [
    path("your-portfolio/canto/", views.ConnectMetamaskManualCantoView, name="your_portfolio_canto"),
    path("canto-portfolio/", views.CantoConnectMetamaskView, name="canto_portfolio"),
    path("wcanto-portfolio/", views.WCantoPortfolioView, name="wcanto_portfolio"),
]