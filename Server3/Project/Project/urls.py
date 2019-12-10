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
from django.urls import path, re_path
from atrades3 import views

urlpatterns = [
    re_path(r'^$', views.index, name='home'),
    re_path(r'^get_current/(?P<company_id>[A-Za-z0-9]+)/$', views.get_current_data, name='get current'),
    re_path(r'^get_history/(?P<company_id>[A-Za-z0-9]+)/(?P<data_type>[A-Za-z0-9]+)/$', views.get_data, name='get'),
    re_path(r'^get_custom/(?P<company_id>[A-Za-z0-9]+)/(?P<data_type>[A-Za-z0-9]+)/(?P<start_date>[A-Za-z0-9]+)/(?P<end_date>[A-Za-z0-9]+)/$', views.get_custom_data, name='get custom'),
    #re_path(r'^test', views.test_template, name='test template'),
    re_path(r'^custom_graphs', views.custom_graph_template, name='Custom Graph Template'),
    re_path(r'^company/(?P<company_id>[A-Za-z0-9]+)/$', views.company_page, name='Company Page'),
    re_path(r'^admin/', admin.site.urls),
]
