"""Project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.views.debug import default_urlconf
from django.urls import path, re_path, include
from atrades2 import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'bank_accounts', views.BankAccountViewSet)
router.register(r'companies', views.CompanyViewSet)
router.register(r'recurring_buy', views.RecurringBuyViewSet)
router.register(r'transactions', views.TransactionViewSet)
router.register(r'stocks', views.StocksViewSet)



urlpatterns = [
    re_path(r'^api/', include(router.urls)),
    re_path(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^create_user/', views.create_user, name="create_user"),
    re_path(r'^check_login/', views.check_login, name="check_login"),
    re_path(r'^google_login/', views.google_login, name="google_login"),
    re_path(r'^get_current/(?P<company_id>[A-Za-z0-9]+)/$', views.get_current_data, name='get current'),
    re_path(r'^get_recent/(?P<company_id>[A-Za-z0-9]+)/(?P<data_type>[A-Za-z0-9]+)/$', views.get_recent_data, name='get'),
    re_path(r'^get_custom/(?P<company_id>[A-Za-z0-9]+)/(?P<data_type>[A-Za-z0-9]+)/(?P<start_date>[A-Za-z0-9]+)/(?P<end_date>[A-Za-z0-9]+)/$', views.get_custom_data, name='get custom'),
    re_path(r'^buy_stock/', views.buy_stock, name="buy_stock"),
    re_path(r'^buy_queue_stocks/', views.buy_queue_stocks, name="buy_queue_stocks"),
    re_path(r'^view_queue/', views.view_queue, name="view_queue"),
    re_path(r'^generate_password/', views.generate_password, name="generate_password"),
    re_path(r'^set_up_rec/', views.set_up_rec, name="set_up_rec"),
    re_path(r'^delete_rec/', views.delete_rec, name="delete_rec"),

    re_path(r'^sell_stock/', views.sell_stock, name="sell_stock"),
    re_path(r'^transfer_funds/', views.transfer_funds, name="transfer_funds"),
    re_path(r'^view_count/', views.view_count, name="view_count"),
    re_path(r'^update_user_profile/', views.update_user_profile, name="update_user_profile"),
    re_path(r'^delete_bank_account/(?P<acc_id>[0-9]+)/', views.delete_bank_account, name="delete_bank_account"),
    re_path(r'^create_bank_account/', views.create_bank_account, name="create_bank_account"),
    re_path(r'^get_stock_details/', views.get_stock_details, name="get_stock_details"),
    re_path(r'^get_stock_analysis/', views.get_stock_analysis, name="get_stock_analysis"),

]
