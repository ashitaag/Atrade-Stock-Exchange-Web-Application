from django.contrib import admin
from django.urls import path
from django.conf.urls import url, handler404, handler500
from atrades1 import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'signup/$', views.signup, name='signup'),
    url(r'check_login/$', views.check_login, name='check_login'),
    url(r'google_login/$', views.google_login, name='google_login'),
    url(r'logout/$', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('companies/', views.companies, name='companies'),
    path('bank_accounts/', views.bank_accounts, name='bank_accounts'),
    path('statastics/', views.statastics, name='statastics'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('delete_from_cart/', views.delete_from_cart, name='delete_from_cart'),
    path('get_cart/', views.get_cart, name='get_cart'),
    path('clear_cart/', views.clear_cart, name='clear_cart'),
    path('cart/', views.cart, name='cart'),
    path('delete_rec/', views.delete_rec, name='delete_rec'),
    path('send_otp/', views.send_otp, name='send_otp'),
    path('company/<str:company_symbol>/', views.company, name='company'),
    url(r'edit_profile/$', views.edit_profile, name='edit_profile'),
    path('remove_bank_account/<int:acc_id>/<int:user_id>/', views.remove_bank_account, name='remove_bank_account'),
]

handler404 = views.error_404
handler500 = views.error_500