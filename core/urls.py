"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, include, re_path  # add this
from app import views, mnoviews, insuranceviews
from app.views import login_view, register_user
from app.mnoviews import login_view, register_user
from app.insuranceviews import login_view, register_user
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('admin/', admin.site.urls),
    
    re_path(r'^.*\.html', views.pages, name='pages'),
    re_path(r'^.*\.html', mnoviews.pages, name='pages'),
    re_path(r'^.*\.html', insuranceviews.pages, name='pages'),

  
    path('', views.index, name='home'),
    path('', mnoviews.index, name='home'),
    path('', insuranceviews.index, name='home'),
    path('user-tables/',views.usertables,name="user-tables"),
    path('kyc/',views.kyc,name="kyc"),
    path('export_csv_user/',views.export_csv_user,name="export_csv_user"),
    path('pie-chart/', views.pie_chart, name='pie-chart'),
    path('pie-chart2/', views.pie_chart2, name='pie-chart2'),
    path('login/', views.login_view, name="login"),
    path('register/', views.register_user, name="register"),
    path('loginMno/', mnoviews.login_view, name="loginMno"),
    path('registerMno/', mnoviews.register_user, name="registerMno"),
    path('logininsurance/', insuranceviews.login_view, name="logininsurance"),
    path('registerinsurance/', insuranceviews.register_user, name="registerinsurance"),
    path("logout/", LogoutView.as_view(), name="logout")
]


